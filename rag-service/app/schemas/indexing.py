from pydantic import BaseModel, Field


class IndexArchiveRequest(BaseModel):
    archive_id: int = Field(..., ge=1)


class IndexArchiveResponse(BaseModel):
    archive_id: int
    status: str
    chunks_created: int
