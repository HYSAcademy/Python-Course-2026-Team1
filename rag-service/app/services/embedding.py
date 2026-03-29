from openai import AsyncOpenAI

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model

    async def embed_text(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            input=text,
            model=self.model,
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = await self.client.embeddings.create(
            input=texts,
            model=self.model,
        )
        return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


embedding_service = EmbeddingService()
