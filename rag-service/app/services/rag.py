from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.rag import RagQueryResponse, RagSource
from app.services.search import VectorSearchService

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions based solely on the "
    "provided document excerpts. If the context is insufficient, say so clearly."
)


class RAGService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.llm_model

    async def query(self, archive_id: int, query: str, limit: int) -> RagQueryResponse:
        results = await VectorSearchService.search(archive_id, query, limit)

        if not results:
            return RagQueryResponse(
                archive_id=archive_id,
                query=query,
                answer="No relevant documents found for this query.",
                sources=[],
            )

        context = "\n\n---\n\n".join(
            f"[Source {i + 1}]\n{r.content}" for i, r in enumerate(results)
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
            ],
            temperature=0.2,
        )

        return RagQueryResponse(
            archive_id=archive_id,
            query=query,
            answer=response.choices[0].message.content or "No answer generated.",
            sources=[
                RagSource(
                    chunk_id=r.chunk_id,
                    file_id=r.file_id,
                    extension=r.extension,
                    content=r.content,
                    distance=r.distance,
                )
                for r in results
            ],
        )


rag_service = RAGService()
