import httpx
from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.schemas.vector_search import (
    RagQueryRequest,
    RagQueryResponse,
    VectorSearchRequest,
    VectorSearchResponse,
)

router = APIRouter()


@router.post(
    "/vector-search",
    response_model=VectorSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Perform vector search via RAG service",
)
async def vector_search(payload: VectorSearchRequest) -> VectorSearchResponse:
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.rag_service_url}/api/v1/search",
                json=payload.model_dump(),
            )

        response.raise_for_status()
        return VectorSearchResponse(**response.json())

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"RAG service error: {exc.response.text}",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG service is temporarily unavailable.",
        ) from exc


@router.post(
    "/rag-query",
    response_model=RagQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Perform full RAG query via RAG service",
)
async def rag_query(payload: RagQueryRequest) -> RagQueryResponse:
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{settings.rag_service_url}/api/v1/rag/query",
                json=payload.model_dump(),
            )

        response.raise_for_status()
        return RagQueryResponse(**response.json())

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"RAG service error: {exc.response.text}",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG service is temporarily unavailable.",
        ) from exc