import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import router as api_router
from app.api.indexing import router as indexing_router
from app.core.config import settings
from app.db import models
from app.db.session import engine, Base
from app.middleware.exception_handler import (
    InvalidFileException,
    general_exception_handler,
    invalid_file_handler,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    In production, Base.metadata.create_all is a fallback;
    Alembic migrations are typically preferred.
    """
    logger.info("Starting up Archive Processing API...")
    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

    yield

    logger.info("Shutting down Archive Processing API...")
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)


app.add_exception_handler(InvalidFileException, invalid_file_handler)
app.add_exception_handler(Exception, general_exception_handler)


app.include_router(indexing_router, prefix="/api/v1/archives", tags=["indexing"])
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health_check():
    """Service health check for Docker/Kubernetes probes."""
    return {"status": "healthy", "version": "1.0.0"}
