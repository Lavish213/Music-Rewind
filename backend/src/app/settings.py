from __future__ import annotations

from typing import List, Optional
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    This is the ONLY settings object used across the app.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
    )

    # App
    APP_NAME: str = "Music Rewind API"
    ENV: str = "dev"  # dev | staging | prod
    DEBUG: bool = False

    # API
    API_PREFIX: str = "/v1"

    # CORS
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Security / JWT
    JWT_SECRET: str = "CHANGE_ME_DEV_ONLY"
    JWT_ALG: str = "HS256"
    JWT_ACCESS_TTL_SEC: int = 60 * 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str = (
        "postgresql+psycopg://musicrewind:musicrewind@localhost:5432/musicrewind"
    )

    # OAuth / External
    PUBLIC_BASE_URL: Optional[AnyUrl] = None

    # Storage
    BLOB_BACKEND: str = "local"  # local | s3 | gcs


# ✅ singleton used everywhere
settings = Settings()