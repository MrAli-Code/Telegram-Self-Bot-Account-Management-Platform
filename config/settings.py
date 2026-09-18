import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "Telegram Self-Bot"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "production"
    APP_DEBUG: bool = False
    APP_SECRET_KEY: str = "change-this-key"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_WORKERS: int = 4
    APP_LOG_LEVEL: str = "INFO"
    APP_LOG_FILE: str = "storage/logs/app.log"

    DATABASE_URL: str = "sqlite+aiosqlite:///./storage/database.db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_RECYCLE: int = 3600

    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: str = ""
    REDIS_MAX_CONNECTIONS: int = 20

    TELEGRAM_API_ID: int = 0
    TELEGRAM_API_HASH: str = ""
    TELEGRAM_SESSION_STRING: Optional[str] = None
    TELEGRAM_PHONE: Optional[str] = None

    JWT_SECRET_KEY: str = "change-this-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str = "change-this-key"
    CSRF_SECRET_KEY: str = "change-this-csrf-key"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    AI_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-pro"
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-chat"
    OPENROUTER_API_KEY: str = ""
    LOCAL_LLM_URL: str = ""

    MEDIA_STORAGE_PATH: str = "storage/media"
    BACKUP_STORAGE_PATH: str = "storage/backups"
    MAX_UPLOAD_SIZE: int = 52428800
    STORAGE_MAX_SIZE: int = 10737418240

    FFMPEG_PATH: str = "ffmpeg"
    FFPROBE_PATH: str = "ffprobe"
    WHISPER_MODEL: str = "base"

    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 30
    RATE_LIMIT_WINDOW: int = 60
    TELEGRAM_FLOOD_WAIT_ENABLED: bool = True

    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    SCHEDULER_ENABLED: bool = True
    SCHEDULER_TIMEZONE: str = "UTC"

    BACKUP_ENCRYPTION_ENABLED: bool = True
    BACKUP_COMPRESSION_LEVEL: int = 6

    WEBSOCKET_ENABLED: bool = True
    WEBSOCKET_PATH: str = "/ws"

    HEALTH_CHECK_ENABLED: bool = True
    HEALTH_CHECK_PATH: str = "/health"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


class PathSettings:
    """Project paths."""

    BASE_DIR = Path(__file__).resolve().parent.parent
    BACKEND_DIR = BASE_DIR / "backend"
    FRONTEND_DIR = BASE_DIR / "frontend"
    TELEGRAM_DIR = BASE_DIR / "telegram"
    STORAGE_DIR = BASE_DIR / "storage"
    LOGS_DIR = STORAGE_DIR / "logs"
    MEDIA_DIR = STORAGE_DIR / "media"
    BACKUPS_DIR = STORAGE_DIR / "backups"
    CONFIG_DIR = BASE_DIR / "config"
    PLUGINS_DIR = BASE_DIR / "plugins"
    TESTS_DIR = BASE_DIR / "tests"
    MIGRATIONS_DIR = BASE_DIR / "migrations"
    SCRIPTS_DIR = BASE_DIR / "scripts"

    @classmethod
    def ensure_dirs(cls) -> None:
        for attr in [cls.STORAGE_DIR, cls.LOGS_DIR, cls.MEDIA_DIR, cls.BACKUPS_DIR]:
            attr.mkdir(parents=True, exist_ok=True)


settings = Settings()
paths = PathSettings()
paths.ensure_dirs()
