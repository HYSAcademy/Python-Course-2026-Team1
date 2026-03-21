from fastapi import UploadFile

from app.core.config import settings
from app.middleware.exception_handler import InvalidFileException


class FileValidationService:
    @staticmethod
    def validate_content_type(file: UploadFile) -> None:
        if file.content_type not in settings.allowed_content_types:
            raise InvalidFileException(
                f"Unsupported file type: {file.content_type}"
            )

    @staticmethod
    def validate_file_size(current_size: int, filename: str) -> None:
        if current_size > settings.max_upload_size:
            raise InvalidFileException(
                f"File '{filename}' exceeds maximum allowed size "
                f"({settings.max_upload_size} bytes)."
            )

    @staticmethod
    def validate_filename(file: UploadFile) -> None:
        if not file.filename:
            raise InvalidFileException("Uploaded file must have a filename.")

    @staticmethod
    def validate_zip_extension(file: UploadFile) -> None:
        if not file.filename.lower().endswith(".zip"):
            raise InvalidFileException(
                f"File '{file.filename}' is not a .zip archive."
            )

    @classmethod
    def validate_before_save(cls, file: UploadFile) -> None:
        cls.validate_filename(file)
        cls.validate_content_type(file)
        cls.validate_zip_extension(file)