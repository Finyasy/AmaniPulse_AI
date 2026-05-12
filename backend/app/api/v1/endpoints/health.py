from typing import Any

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "amanipulse-api",
        "environment": settings.environment,
        "version": settings.app_version,
    }


@router.get("/ready")
async def readiness_check() -> dict[str, Any]:
    settings = get_settings()
    checks = {"storage": settings.storage_backend}

    if settings.storage_backend == "postgres":
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(sa.text("SELECT 1"))
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "status": "not_ready",
                    "service": "amanipulse-api",
                    "checks": checks,
                },
            ) from exc
        checks["database"] = "ok"

    return {
        "status": "ready",
        "service": "amanipulse-api",
        "environment": settings.environment,
        "version": settings.app_version,
        "checks": checks,
    }
