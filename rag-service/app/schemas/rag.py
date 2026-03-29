from pydantic import BaseModel, Field


class RagQueryRequest(BaseModel):
    archive_id: int = Field(..., ge=1)
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class RagSource(BaseModel):
    chunk_id: int
    file_id: int
    extension: str | None = None
    content: str
    distance: float


class RagQueryResponse(BaseModel):
    archive_id: int
    query: str
    answer: str
    sources: list[RagSource]
