from pydantic import BaseModel


class QueuedArchiveResult(BaseModel):
    archive_id: int
    filename: str
    status: str


class UploadArchivesResponse(BaseModel):
    queued_archives: list[QueuedArchiveResult]