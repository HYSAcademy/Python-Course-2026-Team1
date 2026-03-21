import os
import joblib
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from app.core.config import settings
from app.services.extractor import ArchiveProcessor


class TFIDFIndexingService:
    def __init__(self):
        # Configuration for the vectorizer
        # max_df=0.95: Ignore terms that appear in more than 95% of documents
        # min_df=2: Ignore terms that appear in only 1 document (typos/noise)
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            max_df=0.95,
            min_df=2,
            use_idf=True,
            smooth_idf=True,
        )

    def run_pipeline(self, archive_path: str, index_output_path: str) -> Dict[str, Any]:
        """
        The main pipeline: Extract -> Clean -> Vectorize -> Save
        """
        #  Extraction
        archive_data = ArchiveProcessor.process_archive(archive_path)

        # Pre-processing & filtering
        documents = []
        filenames = []

        for file in archive_data["files"]:
            content = file["content"]
            if content and content != "[Binary or non-UTF8 content]":
                documents.append(content)
                filenames.append(file["path"])

        if not documents:
            raise ValueError("No valid text content found in archive for indexing")

        # Vectorization
        # tfidf_matrix is a scipy sparse matrix
        tfidf_matrix = self.vectorizer.fit_transform(documents)

        # Packaging the Index
        index_artifact = {
            "matrix": tfidf_matrix,
            "filenames": filenames,
            "vectorizer": self.vectorizer,
            "metadata": {
                "archive_name": archive_data["filename"],
                "total_files_indexed": len(filenames),
            },
        }

        # Persistence
        os.makedirs(os.path.dirname(index_output_path), exist_ok=True)
        joblib.dump(index_artifact, index_output_path)

        return index_artifact["metadata"]
