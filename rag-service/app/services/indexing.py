import logging

from sqlalchemy import delete, text

from app.db.models import DocumentChunk
from app.db.session import AsyncSessionLocal
from app.services.chunking import chunking_service
from app.services.embedding import embedding_service

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


class IndexingService:
    @staticmethod
    async def index_archive(archive_id: int) -> int:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                text(
                    "SELECT id, extension, content FROM files "
                    "WHERE archive_id = :archive_id AND content IS NOT NULL"
                ),
                {"archive_id": archive_id},
            )
            files = result.fetchall()

            if not files:
                logger.warning(f"No files found for archive_id={archive_id}")
                return 0

            await db.execute(
                delete(DocumentChunk).where(DocumentChunk.archive_id == archive_id)
            )
            await db.commit()

            all_chunks = []
            for file_id, extension, content in files:
                if not content or not content.strip():
                    continue
                for chunk_text in chunking_service.chunk_text(content):
                    all_chunks.append({
                        "archive_id": archive_id,
                        "file_id": file_id,
                        "extension": extension,
                        "content": chunk_text,
                    })

            if not all_chunks:
                return 0

            total = 0
            for i in range(0, len(all_chunks), BATCH_SIZE):
                batch = all_chunks[i:i + BATCH_SIZE]
                embeddings = await embedding_service.embed_batch(
                    [c["content"] for c in batch]
                )
                db_chunks = [
                    DocumentChunk(
                        archive_id=chunk["archive_id"],
                        file_id=chunk["file_id"],
                        extension=chunk["extension"],
                        content=chunk["content"],
                        embedding=embedding,
                    )
                    for chunk, embedding in zip(batch, embeddings)
                ]
                db.add_all(db_chunks)
                await db.commit()
                total += len(db_chunks)

            logger.info(f"Indexed {total} chunks for archive_id={archive_id}")
            return total
