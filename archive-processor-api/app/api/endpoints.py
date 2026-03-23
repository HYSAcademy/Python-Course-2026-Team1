from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    UploadFile as FastAPIUploadFile,
)
from pydantic import WithJsonSchema
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Archive
from app.db.session import get_db
from app.middleware.exception_handler import InvalidFileException
from app.schemas.archive import QueuedArchiveResult, UploadArchivesResponse
from app.services.storage import FileStorageService
from app.services.validation import FileValidationService
from app.workers.tasks import process_archive_task

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
    background_tasks: BackgroundTasks,
    files: Annotated[list[UploadFile], File(...)],
    db: AsyncSession = Depends(get_db),
) -> UploadArchivesResponse:
    results: list[QueuedArchiveResult] = []

    for file in files:
        FileValidationService.validate_before_save(file)

        temp_file_path = ""
        task_scheduled = False
        archive = None

        try:
            temp_file_path, _ = await FileStorageService.save_upload_to_temp(file)

            archive = Archive(
                filename=file.filename,
                status="queued",
            )
            db.add(archive)
            await db.commit()
            await db.refresh(archive)

            process_archive_task.delay(archive.id, temp_file_path)
            task_scheduled = True

            results.append(
                QueuedArchiveResult(
                    archive_id=archive.id,
                    filename=archive.filename,
                    status=archive.status,
                )
            )

        except InvalidFileException:
            if temp_file_path and not task_scheduled:
                await FileStorageService.remove_temp_file(temp_file_path)
            raise

        except Exception as e:
            if archive:
                archive.status = "failed"
                await db.commit()

            if temp_file_path and not task_scheduled:
                await FileStorageService.remove_temp_file(temp_file_path)

            raise InvalidFileException(
                f"Failed to queue archive {file.filename}: {str(e)}"
            ) from e

    return UploadArchivesResponse(queued_archives=results)