import joblib
import logging
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from app.core.config import settings

logger = logging.getLogger(__name__)


class SearchService:
    @staticmethod
    def perform_search(archive_id: int, query: str, top_n: int = 5) -> list[dict]:
        """
        Executes TF-IDF search using cosine similarity.
        """
        index_path = Path(settings.tfidf_index_dir) / f"{archive_id}.joblib"

        if not index_path.exists():
            logger.warning(f"Index not found for archive {archive_id}")
            return []

        
        data = joblib.load(index_path)
        vectorizer = data["vectorizer"]
        matrix = data["matrix"]
        metadata = data["metadata"]

        
        query_vec = vectorizer.transform([query])

        
        if query_vec.nnz == 0:
            return []

        
        similarities = cosine_similarity(query_vec, matrix).flatten()

        
        relevant_indices = similarities.argsort()[::-1]

        results = []
        for idx in relevant_indices:
            
            if similarities[idx] > 0 and len(results) < top_n:
                results.append({
                    "file_id": metadata[idx]["file_id"],
                    "score": round(float(similarities[idx]), 4),
                    "extension": metadata[idx]["extension"]
                })

        return results