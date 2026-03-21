from pydantic import BaseModel


class ProcessedFileResult(BaseModel):
    filename: str
    status: str
    extracted: int


class UploadArchivesResponse(BaseModel):
    processed_files: list[ProcessedFileResult]