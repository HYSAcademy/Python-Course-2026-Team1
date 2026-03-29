from pydantic import BaseModel, Field


class VectorSearchRequest(BaseModel):
    archive_id: int = Field(..., ge=1)
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class VectorSearchResult(BaseModel):
    chunk_id: int
    file_id: int
    extension: str | None = None
    content: str
    distance: float


class VectorSearchResponse(BaseModel):
    archive_id: int
    query: str
    results: list[VectorSearchResult]
