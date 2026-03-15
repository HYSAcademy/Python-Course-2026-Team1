from pydantic import BaseModel
from typing import List

class FileBase(BaseModel):
    """Base schema for file metadata."""
    path: str
    size: int
    extension: str

class FileCreate(FileBase):
    """Schema for creating a new file record, including extracted text."""
    content: str

class ArchiveResponse(BaseModel):
    """Schema for the final response after processing an archive."""
    id: int
    filename: str
    files_count: int
    files: List[FileCreate]

    class Config:
        from_attributes = True