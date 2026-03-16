from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class Archive(Base):
    __tablename__ = "archives"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_size = Column(Integer)
    files_count = Column(Integer)

    files = relationship("File", back_populates="archive")


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    archive_id = Column(Integer, ForeignKey("archives.id"))
    size = Column(Integer)
    extension = Column(String)
    content = Column(Text, nullable=True)

    archive = relationship("Archive", back_populates="files")