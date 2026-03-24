from fastapi import APIRouter, Query, status
from app.schemas.search import SearchResponse, SearchResult
from app.services.search import SearchService

router = APIRouter()


@router.get(
    "/{archive_id}",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Perform TF-IDF search",
)
async def search_archive(
        archive_id: int,
        query: str = Query(..., min_length=1),
        limit: int = Query(5, ge=1, le=50)
):
    
    results_data = SearchService.perform_search(archive_id, query, top_n=limit)

    if not results_data and query:
        
        
        return SearchResponse(
            archive_id=archive_id,
            query=query,
            results=[]
        )

    return SearchResponse(
        archive_id=archive_id,
        query=query,
        results=[SearchResult(**res) for res in results_data]
    )