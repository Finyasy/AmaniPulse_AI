from functools import lru_cache
from os import getenv

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = Field(default_factory=lambda: getenv("APP_NAME", "AmaniPulse AI API"))
    app_version: str = Field(default_factory=lambda: getenv("APP_VERSION", "0.1.0"))
    environment: str = Field(default_factory=lambda: getenv("ENVIRONMENT", "development"))
    api_prefix: str = "/v1"
    storage_backend: str = Field(default_factory=lambda: getenv("STORAGE_BACKEND", "memory"))
    database_url: str = Field(
        default_factory=lambda: getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://amanipulse:amanipulse@localhost:55432/amanipulse",
        )
    )
    redis_url: str = Field(default_factory=lambda: getenv("REDIS_URL", "redis://localhost:56379/0"))
    enable_ai_worker: bool = Field(
        default_factory=lambda: getenv("ENABLE_AI_WORKER", "true").lower() == "true"
    )
    celery_task_always_eager: bool = Field(
        default_factory=lambda: getenv("CELERY_TASK_ALWAYS_EAGER", "true").lower() == "true"
    )
    log_level: str = Field(default_factory=lambda: getenv("LOG_LEVEL", "INFO"))
    log_format: str = Field(default_factory=lambda: getenv("LOG_FORMAT", "json"))
    request_id_header: str = Field(
        default_factory=lambda: getenv("REQUEST_ID_HEADER", "X-Request-ID")
    )
    max_request_body_bytes: int = Field(
        default_factory=lambda: int(getenv("MAX_REQUEST_BODY_BYTES", "16000"))
    )
    report_rate_limit_count: int = Field(
        default_factory=lambda: int(getenv("REPORT_RATE_LIMIT_COUNT", "12"))
    )
    report_rate_limit_window_seconds: int = Field(
        default_factory=lambda: int(getenv("REPORT_RATE_LIMIT_WINDOW_SECONDS", "60"))
    )
    duplicate_report_window_seconds: int = Field(
        default_factory=lambda: int(getenv("DUPLICATE_REPORT_WINDOW_SECONDS", "300"))
    )
    report_encryption_key: str = Field(
        default_factory=lambda: getenv(
            "REPORT_ENCRYPTION_KEY",
            "YW1hbmlwdWxzZS1kZXYtcmVwb3J0LWtleS0zMmIhISE=",
        )
    )
    internal_api_token: str = Field(
        default_factory=lambda: getenv("INTERNAL_API_TOKEN", "dev-internal-review-token")
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
