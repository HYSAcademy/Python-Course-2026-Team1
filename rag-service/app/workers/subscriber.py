import asyncio
import logging

import redis.asyncio as aioredis

from app.core.config import settings
from app.services.indexing import IndexingService

logger = logging.getLogger(__name__)


async def handle_archive_processed(archive_id: int) -> None:
    logger.info(f"archive_processed: archive_id={archive_id}")
    try:
        count = await IndexingService.index_archive(archive_id)
        logger.info(f"Indexed {count} chunks for archive_id={archive_id}")
    except Exception as e:
        logger.error(f"Indexing failed for archive_id={archive_id}: {e}")


async def start_subscriber() -> None:
    client = aioredis.from_url(settings.redis_url)

    async with client.pubsub() as pubsub:
        await pubsub.subscribe(settings.archive_processed_channel)
        logger.info(f"Subscribed to: {settings.archive_processed_channel}")

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            try:
                archive_id = int(message["data"])
                asyncio.create_task(handle_archive_processed(archive_id))
            except (ValueError, TypeError) as e:
                logger.error(f"Invalid message: {message['data']!r} — {e}")
