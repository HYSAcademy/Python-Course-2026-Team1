import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.indexing import router as indexing_router
from app.api.rag import router as rag_router
from app.api.search import router as search_router
from app.core.config import settings
from app.db.session import Base, engine
from app.middleware.exception_handler import general_exception_handler
from app.workers.subscriber import start_subscriber

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RAG Service...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    subscriber_task = asyncio.create_task(start_subscriber())

    yield

    subscriber_task.cancel()
    try:
        await subscriber_task
    except asyncio.CancelledError:
        pass

    await engine.dispose()
    logger.info("RAG Service shut down.")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url=None,
)

app.add_exception_handler(Exception, general_exception_handler)

app.include_router(indexing_router, prefix="/api/v1", tags=["indexing"])
app.include_router(search_router, prefix="/api/v1", tags=["search"])
app.include_router(rag_router, prefix="/api/v1", tags=["rag"])


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
