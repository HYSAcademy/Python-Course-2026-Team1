from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, Text

from app.core.config import settings
from app.db.session import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    archive_id = Column(Integer, nullable=False, index=True)
    file_id = Column(Integer, nullable=False)
    extension = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(settings.embedding_dimensions), nullable=True)
