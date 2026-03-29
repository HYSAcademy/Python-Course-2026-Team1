from fastapi import APIRouter, HTTPException, status

from app.schemas.search import VectorSearchRequest, VectorSearchResponse
from app.services.search import VectorSearchService

router = APIRouter()


@router.post("/search", response_model=VectorSearchResponse, status_code=status.HTTP_200_OK)
async def vector_search(payload: VectorSearchRequest) -> VectorSearchResponse:
    try:
        results = await VectorSearchService.search(
            archive_id=payload.archive_id,
            query=payload.query,
            limit=payload.limit,
        )
        return VectorSearchResponse(
            archive_id=payload.archive_id,
            query=payload.query,
            results=results,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}") from e
