import json
import logging
import uuid
from typing import Annotated

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.schemas.indexing import IndexTaskResponse, IndexTriggerRequest

logger = logging.getLogger(__name__)

router = APIRouter()


async def get_redis_client():
    """
    Dependency that yields a Redis connection from the pool.
    Ensures the connection is properly closed after the request.
    """
    client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True,
        socket_timeout=5.0,
        socket_connect_timeout=5.0,
    )
    try:
        yield client
    finally:
        await client.aclose()


@router.post(
    "/trigger",
    response_model=IndexTaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger TF-IDF Indexing",
    description="Accepts an archive ID and queues a background task for TF-IDF processing.",
)
async def trigger_indexing(
    payload: IndexTriggerRequest,
    redis_conn: Annotated[redis.Redis, Depends(get_redis_client)],
):
    """
    1. Generates a unique UUID Task ID.
    2. Strings the ID for Redis/JSON storage.
    3. Pushes the task to the broker.
    4. Returns the UUID object to the response model.
    """
    task_id = uuid.uuid4()

    job_payload = {
        "task_id": str(task_id),
        "archive_id": payload.archive_id,
        "status": "queued",
    }

    try:

        await redis_conn.lpush(settings.tfidf_queue_name, json.dumps(job_payload))
        logger.info(
            f"Task {task_id} successfully queued for archive {payload.archive_id}"
        )

    except (redis.ConnectionError, redis.TimeoutError) as e:
        logger.error(f"Broker connectivity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The task queue is temporarily unavailable.",
        )

    return IndexTaskResponse(
        task_id=task_id, archive_id=payload.archive_id, status="queued"
    )
