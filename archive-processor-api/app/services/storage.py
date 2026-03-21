import os
import uuid

import aiofiles
import aiofiles.os
from fastapi import UploadFile

from app.core.config import settings
from app.services.validation import FileValidationService


class FileStorageService:
    @staticmethod
    async def ensure_temp_dir() -> None:
        os.makedirs(settings.upload_temp_dir, exist_ok=True)

    @staticmethod
    def build_temp_file_path(filename: str) -> str:
        unique_name = f"{uuid.uuid4()}_{filename}"
        return os.path.join(settings.upload_temp_dir, unique_name)

    @classmethod
    async def save_upload_to_temp(cls, file: UploadFile) -> tuple[str, int]:
        await cls.ensure_temp_dir()

        temp_file_path = cls.build_temp_file_path(file.filename)
        current_file_size = 0

        async with aiofiles.open(temp_file_path, "wb") as out_file:
            while chunk := await file.read(settings.chunk_size):
                current_file_size += len(chunk)

                FileValidationService.validate_file_size(
                    current_file_size,
                    file.filename,
                )

                await out_file.write(chunk)

        return temp_file_path, current_file_size

    @staticmethod
    async def remove_temp_file(path: str) -> None:
        if await aiofiles.os.path.exists(path):
            await aiofiles.os.remove(path)