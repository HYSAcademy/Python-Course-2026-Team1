from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Archive Processor API"
    environment: str = "production"
    debug: bool = False

    database_url: str

    redis_host: str = "redis"
    redis_port: int = 6379
    tfidf_queue_name: str = "tfidf_tasks"

    upload_temp_dir: str = "/app/data/uploads"
    tfidf_index_dir: str = "/app/data/indices"

    max_upload_size: int = 50 * 1024 * 1024
    chunk_size: int = 1024 * 1024

    allowed_content_types: List[str] = [
        "application/zip",
        "application/x-zip-compressed",
        "application/octet-stream",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("database_url")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError(
                "DATABASE_URL must be a valid PostgreSQL connection string"
            )
        return v


settings = Settings()
