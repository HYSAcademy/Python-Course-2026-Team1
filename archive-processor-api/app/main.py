from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.endpoints import router as api_router
from app.db.session import engine, Base
from app.db.models import Archive, File
from app.middleware.exception_handler import (
    InvalidFileException,
    invalid_file_handler,
    general_exception_handler
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Archive Processing API", lifespan=lifespan)

# Register the exception handlers imported from the middleware
app.add_exception_handler(InvalidFileException, invalid_file_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(api_router, prefix="/api/v1")