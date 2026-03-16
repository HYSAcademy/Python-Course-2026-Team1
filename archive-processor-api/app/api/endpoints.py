import os
import uuid
import asyncio
import aiofiles
import aiofiles.os
from typing import List, Annotated, Dict, Any

from fastapi import APIRouter, UploadFile as FastAPIUploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import WithJsonSchema

from app.db.session import get_db
from app.db.models import Archive, File as DBFile
from app.services.extractor import ArchiveProcessor
from app.middleware.exception_handler import InvalidFileException

router = APIRouter()

# Schema fix for Swagger UI
UploadFile = Annotated[
    FastAPIUploadFile, WithJsonSchema({"type": "string", "format": "binary"})
]

# Configuration via environment variables
ALLOWED_TYPES = [
    "application/zip",
    "application/x-zip-compressed",
    "application/octet-stream",
]
TEMP_DIR = os.getenv("UPLOAD_TEMP_DIR", "/tmp/uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 52428800))  # Default 50MB limit
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for streaming

# Ensure temp directory exists inside the container
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/upload-archives/", response_model=Dict[str, List[Dict[str, Any]]])
async def upload_archives(
        files: Annotated[List[UploadFile], File(...)], db: AsyncSession = Depends(get_db)
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Uploads, validates, and extracts multiple archive files asynchronously.

    Persists archive metadata and extracted file contents to the database.
    Files are streamed to a temporary directory in chunks to prevent memory overload.
    """
    results = []

    for file in files:
        if file.content_type not in ALLOWED_TYPES:
            raise InvalidFileException(f"Unsupported type: {file.content_type}")

        temp_file_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{file.filename}")
        current_file_size = 0

        try:
            # 1. Stream the upload to disk in chunks to control memory usage
            async with aiofiles.open(temp_file_path, "wb") as out_file:
                while chunk := await file.read(CHUNK_SIZE):
                    current_file_size += len(chunk)
                    if current_file_size > MAX_FILE_SIZE:
                        raise InvalidFileException(f"File {file.filename} exceeds maximum size limit.")
                    await out_file.write(chunk)

            # 2. Process archive in a separate thread to avoid blocking the event loop
            archive_data = await asyncio.to_thread(
                ArchiveProcessor.process_archive, temp_file_path
            )

            # 3. Database Persistence
            db_archive = Archive(
                filename=file.filename,
                file_size=archive_data["file_size"],
                files_count=archive_data["files_count"],
            )
            db.add(db_archive)
            await db.flush()

            # Batch insert extracted files
            db_files = [
                DBFile(
                    archive_id=db_archive.id,
                    size=f_data["size"],
                    extension=f_data["extension"],
                    content=f_data["content"],
                )
                for f_data in archive_data["files"]
            ]
            db.add_all(db_files)

            results.append(
                {
                    "filename": file.filename,
                    "status": "Success",
                    "extracted": archive_data["files_count"],
                }
            )

        except Exception as e:
            raise InvalidFileException(f"Extraction failed for {file.filename}: {str(e)}")

        finally:
            # 4. Clean up the temp file asynchronously
            if await aiofiles.os.path.exists(temp_file_path):
                await aiofiles.os.remove(temp_file_path)

    await db.commit()
    return {"processed_files": results}