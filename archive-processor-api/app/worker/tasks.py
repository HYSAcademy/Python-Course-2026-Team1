import asyncio

from app.workers.celery_app import celery_app
from app.services.archive_processing import ArchiveProcessingService


@celery_app.task(name="process_archive_task")
def process_archive_task(archive_id: int, temp_file_path: str) -> None:
    asyncio.run(
        ArchiveProcessingService.process_archive_background(
            archive_id=archive_id,
            temp_file_path=temp_file_path,
        )
    )