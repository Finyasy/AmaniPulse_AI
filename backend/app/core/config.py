from functools import lru_cache
from os import getenv

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = getenv("APP_NAME", "AmaniPulse AI API")
    app_version: str = getenv("APP_VERSION", "0.1.0")
    environment: str = getenv("ENVIRONMENT", "development")
    api_prefix: str = "/v1"
    storage_backend: str = getenv("STORAGE_BACKEND", "memory")
    database_url: str = getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://amanipulse:amanipulse@localhost:55432/amanipulse",
    )
    redis_url: str = getenv("REDIS_URL", "redis://localhost:56379/0")
    enable_ai_worker: bool = getenv("ENABLE_AI_WORKER", "true").lower() == "true"
    celery_task_always_eager: bool = getenv("CELERY_TASK_ALWAYS_EAGER", "true").lower() == "true"
    log_level: str = getenv("LOG_LEVEL", "INFO")
    log_format: str = getenv("LOG_FORMAT", "json")
    request_id_header: str = getenv("REQUEST_ID_HEADER", "X-Request-ID")
    report_encryption_key: str = getenv(
        "REPORT_ENCRYPTION_KEY",
        "YW1hbmlwdWxzZS1kZXYtcmVwb3J0LWtleS0zMmIhISE=",
    )
    internal_api_token: str = getenv("INTERNAL_API_TOKEN", "dev-internal-review-token")


@lru_cache
def get_settings() -> Settings:
    return Settings()
