from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile as FastAPIUploadFile
from pydantic import WithJsonSchema
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.exception_handler import InvalidFileException
from app.schemas.archive import UploadArchivesResponse
from app.services.archive_processing import ArchiveProcessingService
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
    results = []

    for file in files:
        FileValidationService.validate_before_save(file)
        temp_file_path = ""

        try:
            temp_file_path, _ = await FileStorageService.save_upload_to_temp(file)

            processed_result = await ArchiveProcessingService.process_archive(
                db=db,
                temp_file_path=temp_file_path,
                original_filename=file.filename,
            )
            results.append(processed_result)

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