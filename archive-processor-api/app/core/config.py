from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    upload_temp_dir: str = "/tmp/uploads"
    max_upload_size: int = 50 * 1024 * 1024
    chunk_size: int = 1024 * 1024

    allowed_content_types: list[str] = [
        "application/zip",
        "application/x-zip-compressed",
        "application/octet-stream",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()