import logging
import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas.indexing import IndexTaskResponse, IndexTriggerRequest
from app.workers.tasks import generate_tfidf_index_task

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/trigger",
    response_model=IndexTaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger TF-IDF Indexing",
)
async def trigger_indexing(payload: IndexTriggerRequest):
    """
    Pushes the TF-IDF indexing task to the Celery broker.
    """
    try:

        task = generate_tfidf_index_task.delay(payload.archive_id)

        logger.info(
            f"Task {task.id} successfully queued for archive {payload.archive_id}"
        )

        return IndexTaskResponse(
            task_id=uuid.UUID(task.id),
            archive_id=payload.archive_id,
            status="queued",
        )

    except Exception as e:
        logger.error(f"Broker connectivity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The task queue is temporarily unavailable.",
        )
