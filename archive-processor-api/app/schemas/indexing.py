from datetime import datetime, UTC
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class IndexTriggerRequest(BaseModel):
    """
    Data required to initiate a TF-IDF indexing task.
    """

    archive_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The unique identifier of the pre-validated archive file.",
        examples=["archive-id-placeholder"],
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"archive_id": "archive-id-placeholder"}}
    )


class IndexTaskResponse(BaseModel):
    """
    Immediate response sent to the client when a task is successfully queued.
    """

    task_id: UUID = Field(
        ...,
        description="Unique identifier for tracking the background job status.",
        examples=["00000000-0000-0000-0000-000000000000"],
    )
    archive_id: str = Field(
        ...,
        description="The ID of the archive being processed.",
        examples=["archive-id-placeholder"],
    )
    status: str = Field(
        default="queued",
        description="The initial state of the task in the Redis broker.",
    )
    queued_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timezone-aware UTC timestamp of the task creation.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "task_id": "00000000-0000-0000-0000-000000000000",
                "archive_id": "archive-id-placeholder",
                "status": "queued",
                "queued_at": "2026-01-01T00:00:00Z",
            }
        }
    )


class IndexingResultMetadata(BaseModel):
    """
    Detailed results produced by the worker upon successful completion.
    """

    documents_indexed: int = Field(..., ge=0, examples=[10])
    vocabulary_size: int = Field(..., ge=0, examples=[500])
    output_path: str = Field(
        ...,
        description="Storage path of the generated .joblib index.",
        examples=["/app/data/indices/archive-id.joblib"],
    )
    processing_time_seconds: float = Field(
        ..., description="Total time taken by the worker.", examples=[1.25]
    )


class IndexTaskStatus(BaseModel):
    """
    Schema for checking the current progress of an indexing task.
    """

    task_id: UUID = Field(..., examples=["00000000-0000-0000-0000-000000000000"])
    status: str = Field(
        ..., pattern="^(queued|processing|completed|failed)$", examples=["completed"]
    )
    result: Optional[IndexingResultMetadata] = None
    error: Optional[str] = None
