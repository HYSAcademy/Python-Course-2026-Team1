import asyncio
import json
import logging
import signal
import sys
from pathlib import Path

import redis.asyncio as redis
from sqlalchemy import select

from app.core.config import settings
from app.db.models import Archive
from app.db.session import AsyncSessionLocal

# branch with core is not merged yet
try:
    from app.services.indexing import TFIDFIndexingService
except ImportError:
    logger = logging.getLogger("tfidf-worker")
    logger.error(
        "TFIDFIndexingService not found. Ensure the indexing branch is merged."
    )
    raise

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("tfidf-worker")


class TFIDFWorker:
    def __init__(self):
        self.stop_event = asyncio.Event()
        self.service = TFIDFIndexingService()
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True,
        )

    def trigger_stop(self):
        """Callback for signal handlers to initiate graceful shutdown."""
        logger.info("Shutdown signal received. Setting stop event...")
        self.stop_event.set()

    async def update_archive_status(self, archive_id: str, status_msg: str):
        """Updates the archive status in the database."""
        async with AsyncSessionLocal() as db:
            try:
                stmt = select(Archive).where(Archive.filename == archive_id)
                result = await db.execute(stmt)
                archive = result.scalar_one_or_none()

                if archive:

                    logger.info(f"DB Update: {archive_id} -> {status_msg}")
                    await db.commit()
            except Exception as e:
                logger.error(f"Database update failed: {e}")

    async def process_task(self, task_data: str):
        """Executes the indexing pipeline."""
        archive_id = None
        try:
            task = json.loads(task_data)
            archive_id = task.get("archive_id")

            logger.info(f"Starting TF-IDF indexing for: {archive_id}")

            input_path = Path(settings.upload_temp_dir) / f"{archive_id}.zip"
            output_path = Path(settings.tfidf_index_dir) / f"{archive_id}.joblib"

            if not input_path.exists():
                logger.error(f"Archive not found: {input_path}")
                return

            await asyncio.to_thread(
                self.service.run_pipeline, str(input_path), str(output_path)
            )

            await self.update_archive_status(archive_id, "completed")
            logger.info(f"Successfully processed {archive_id}")

        except Exception as e:
            logger.exception(f"Processing failed for {archive_id}: {e}")

    async def run(self):
        """Main worker loop."""
        logger.info(f"Worker listening on queue: {settings.tfidf_queue_name}")

        loop = asyncio.get_running_loop()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: self.trigger_stop())

        while not self.stop_event.is_set():
            try:

                job = await self.redis_client.blpop(
                    settings.tfidf_queue_name, timeout=2
                )

                if job:
                    _, task_data = job
                    await self.process_task(task_data)

            except Exception as e:
                logger.error(f"Worker loop encountered an error: {e}")
                await asyncio.sleep(5)

        logger.info("Worker stopped gracefully.")


if __name__ == "__main__":
    worker = TFIDFWorker()
    try:
        asyncio.run(worker.run())
    except KeyboardInterrupt:
        pass
