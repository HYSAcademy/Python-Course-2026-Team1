from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Archive(Base):
    __tablename__ = "archives"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_size = Column(Integer, nullable=True)
    files_count = Column(Integer, nullable=True)
    status = Column(String, default="queued", nullable=False)

    files = relationship("File", back_populates="archive")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    archive_id = Column(Integer, ForeignKey("archives.id"))
    size = Column(Integer)
    extension = Column(String)
    content = Column(Text, nullable=True)

    archive = relationship("Archive", back_populates="files")