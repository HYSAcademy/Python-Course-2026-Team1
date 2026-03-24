from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    file_id: int
    score: float = Field(..., description="Cosine similarity score (0.0 to 1.0)")
    extension: str

class SearchResponse(BaseModel):
    archive_id: int
    query: str
    results: list[SearchResult]
    #