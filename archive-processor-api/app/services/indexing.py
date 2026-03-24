import joblib
import logging
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.db.models import File
from app.core.config import settings

logger = logging.getLogger(__name__)

class TFIDFIndexingService:
    @staticmethod
    async def run_pipeline(archive_id: int) -> None:
        """Asynchronous internal function to handle DB I/O and indexing."""
        async with AsyncSessionLocal() as db:
            stmt = select(File).where(File.archive_id == archive_id)
            result = await db.execute(stmt)
            db_files = result.scalars().all()

            if not db_files:
                logger.warning(f"No files found for archive {archive_id}")
                return

            documents = []
            metadata = []

            for f in db_files:
                if f.content and "[Binary" not in f.content:
                    documents.append(f.content)
                    metadata.append({"file_id": f.id, "extension": f.extension})

            if not documents:
                logger.warning(f"No indexable text found for archive {archive_id}")
                return

            vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)
            tfidf_matrix = vectorizer.fit_transform(documents)

            index_data = {
                "matrix": tfidf_matrix,
                "vectorizer": vectorizer,
                "metadata": metadata,
            }

            output_dir = Path(settings.tfidf_index_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{archive_id}.joblib"

            joblib.dump(index_data, output_path)
            logger.info(f"TF-IDF index saved to {output_path}")