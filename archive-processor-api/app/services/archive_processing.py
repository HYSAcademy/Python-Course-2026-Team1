import asyncio

from app.db.models import Archive, File as DBFile
from app.db.session import AsyncSessionLocal
from app.services.extractor import ArchiveProcessor
from app.services.storage import FileStorageService


class ArchiveProcessingService:
    @staticmethod
    async def process_archive_background(
        archive_id: int,
        temp_file_path: str,
    ) -> None:
        async with AsyncSessionLocal() as db:
            archive = await db.get(Archive, archive_id)

            if not archive:
                await FileStorageService.remove_temp_file(temp_file_path)
                return

            try:
                archive.status = "processing"
                await db.commit()

                archive_data = await asyncio.to_thread(
                    ArchiveProcessor.process_archive,
                    temp_file_path,
                )

                archive.file_size = archive_data["file_size"]
                archive.files_count = archive_data["files_count"]
                archive.status = "processed"

                db_files = [
                    DBFile(
                        archive_id=archive.id,
                        size=file_data["size"],
                        extension=file_data["extension"],
                        content=file_data["content"],
                    )
                    for file_data in archive_data["files"]
                ]
                db.add_all(db_files)
                await db.commit()

            except Exception:
                await db.rollback()

                archive = await db.get(Archive, archive_id)
                if archive:
                    archive.status = "failed"
                    await db.commit()

                raise

            finally:
                await FileStorageService.remove_temp_file(temp_file_path)