import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile as FastAPIUploadFile
from pydantic import WithJsonSchema
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Archive, File as DBFile
from app.db.session import get_db
from app.middleware.exception_handler import InvalidFileException
from app.schemas.archive import ProcessedFileResult, UploadArchivesResponse
from app.services.extractor import ArchiveProcessor
from app.services.storage import FileStorageService
from app.services.validation import FileValidationService

router = APIRouter()

UploadFile = Annotated[
    FastAPIUploadFile,
    WithJsonSchema({"type": "string", "format": "binary"}),
]


@router.post(
    "/upload-archives/",
    response_model=UploadArchivesResponse,
)
async def upload_archives(
    files: Annotated[list[UploadFile], File(...)],
    db: AsyncSession = Depends(get_db),
) -> UploadArchivesResponse:
    results: list[ProcessedFileResult] = []

    for file in files:
        FileValidationService.validate_before_save(file)

        temp_file_path = ""

        try:
            temp_file_path, _ = await FileStorageService.save_upload_to_temp(file)

            archive_data = await asyncio.to_thread(
                ArchiveProcessor.process_archive,
                temp_file_path,
            )

            db_archive = Archive(
                filename=file.filename,
                file_size=archive_data["file_size"],
                files_count=archive_data["files_count"],
            )
            db.add(db_archive)
            await db.flush()

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
                ProcessedFileResult(
                    filename=file.filename,
                    status="Success",
                    extracted=archive_data["files_count"],
                )
            )

        except InvalidFileException:
            raise
        except Exception as e:
            raise InvalidFileException(
                f"Extraction failed for {file.filename}: {str(e)}"
            ) from e
        finally:
            if temp_file_path:
                await FileStorageService.remove_temp_file(temp_file_path)

    await db.commit()
    return UploadArchivesResponse(processed_files=results)