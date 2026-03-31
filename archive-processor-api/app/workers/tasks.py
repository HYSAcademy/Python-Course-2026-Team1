import asyncio
import logging
import redis

from app.workers.celery_app import celery_app
from app.services.archive_processing import ArchiveProcessingService
from app.services.indexing import TFIDFIndexingService
from app.core.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(name="process_archive_task")
def process_archive_task(archive_id: int, temp_file_path: str) -> None:
    """Handles the initial extraction of the ZIP file and notifies RAG service."""
    try:

        asyncio.run(
            ArchiveProcessingService.process_archive_background(
                archive_id=archive_id,
                temp_file_path=temp_file_path,
            )
        )

        r = redis.from_url(settings.redis_url)
        r.publish(settings.archive_processed_channel, str(archive_id))
        r.close()
        logger.info(
            f"Published archive_id {archive_id} to {settings.archive_processed_channel}"
        )

    except Exception as e:
        logger.error(f"Failed to process or publish archive {archive_id}: {str(e)}")
        raise


@celery_app.task(name="generate_tfidf_index_task")
def generate_tfidf_index_task(archive_id: int) -> dict:
    """Calculates TF-IDF weights and saves the index."""
    logger.info(f"Starting TF-IDF indexing for archive_id: {archive_id}")
    try:
        asyncio.run(TFIDFIndexingService.run_pipeline(archive_id))
        return {"status": "success", "archive_id": archive_id}
    except Exception as e:
        logger.error(f"Failed to process archive {archive_id}: {str(e)}")
        raise
