from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Archive
from app.db.session import get_db
from app.middleware.exception_handler import InvalidFileException
from app.schemas.status import ArchiveStatusResponse

router = APIRouter()


@router.get(
    "/archives/{archive_id}/status",
    response_model=ArchiveStatusResponse,
)
async def get_archive_status(
    archive_id: int,
    db: AsyncSession = Depends(get_db),
) -> ArchiveStatusResponse:
    archive = await db.get(Archive, archive_id)

    if not archive:
        raise InvalidFileException(f"Archive with id={archive_id} not found")

    return ArchiveStatusResponse(
        archive_id=archive.id,
        filename=archive.filename,
        status=archive.status,
        file_size=archive.file_size,
        files_count=archive.files_count,
    )