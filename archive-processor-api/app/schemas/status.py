from pydantic import BaseModel


class ArchiveStatusResponse(BaseModel):
    archive_id: int
    filename: str
    status: str
    file_size: int | None = None
    files_count: int | None = None