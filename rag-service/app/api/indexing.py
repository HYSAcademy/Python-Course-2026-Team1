from fastapi import APIRouter, HTTPException, status

from app.schemas.indexing import IndexArchiveRequest, IndexArchiveResponse
from app.services.indexing import IndexingService

router = APIRouter()


@router.post("/index", response_model=IndexArchiveResponse, status_code=status.HTTP_200_OK)
async def trigger_indexing(payload: IndexArchiveRequest) -> IndexArchiveResponse:
    try:
        chunks_created = await IndexingService.index_archive(payload.archive_id)
        return IndexArchiveResponse(
            archive_id=payload.archive_id,
            status="indexed",
            chunks_created=chunks_created,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}") from e
