from sqlalchemy import text

from app.db.session import AsyncSessionLocal
from app.schemas.search import VectorSearchResult
from app.services.embedding import embedding_service


class VectorSearchService:
    @staticmethod
    async def search(archive_id: int, query: str, limit: int) -> list[VectorSearchResult]:
        query_embedding = await embedding_service.embed_text(query)

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                text("""
                    SELECT id, file_id, extension, content,
                           embedding <=> CAST(:embedding AS vector) AS distance
                    FROM document_chunks
                    WHERE archive_id = :archive_id
                    ORDER BY distance
                    LIMIT :limit
                """),
                {
                    "embedding": str(query_embedding),
                    "archive_id": archive_id,
                    "limit": limit,
                },
            )
            rows = result.fetchall()

        return [
            VectorSearchResult(
                chunk_id=row.id,
                file_id=row.file_id,
                extension=row.extension,
                content=row.content,
                distance=row.distance,
            )
            for row in rows
        ]
