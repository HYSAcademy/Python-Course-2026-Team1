import tiktoken

from app.core.config import settings


class ChunkingService:
    def __init__(self):
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap

    def chunk_text(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []

        tokens = self.encoder.encode(text)

        if len(tokens) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunks.append(self.encoder.decode(tokens[start:end]))

            if end == len(tokens):
                break

            start += self.chunk_size - self.chunk_overlap

        return chunks


chunking_service = ChunkingService()
