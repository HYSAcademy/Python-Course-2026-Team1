from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Archive, File as DBFile
from app.schemas.archive import ProcessedFileResult
from app.services.extractor import ArchiveProcessor


class ArchiveProcessingService:
    @staticmethod
    async def process_archive(
        db: AsyncSession,
        temp_file_path: str,
        original_filename: str,
    ) -> ProcessedFileResult:
        """
        Full archive processing pipeline:
        - extract archive data
        - create Archive record
        - create File records
        - return API response DTO
        """
        archive_data = ArchiveProcessor.process_archive(temp_file_path)

        db_archive = Archive(
            filename=original_filename,
            file_size=archive_data["file_size"],
            files_count=archive_data["files_count"],
        )
        db.add(db_archive)
        await db.flush()

        db_files = [
            DBFile(
                archive_id=db_archive.id,
                size=file_data["size"],
                extension=file_data["extension"],
                content=file_data["content"],
            )
            for file_data in archive_data["files"]
        ]
        db.add_all(db_files)

        return ProcessedFileResult(
            filename=original_filename,
            status="Success",
            extracted=archive_data["files_count"],
        )