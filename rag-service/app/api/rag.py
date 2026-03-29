from fastapi import APIRouter, HTTPException, status

from app.schemas.rag import RagQueryRequest, RagQueryResponse
from app.services.rag import rag_service

router = APIRouter()


@router.post("/rag/query", response_model=RagQueryResponse, status_code=status.HTTP_200_OK)
async def rag_query(payload: RagQueryRequest) -> RagQueryResponse:
    try:
        return await rag_service.query(
            archive_id=payload.archive_id,
            query=payload.query,
            limit=payload.limit,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query failed: {e}") from e
