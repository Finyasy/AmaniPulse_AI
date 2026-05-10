from fastapi import APIRouter, Query

from app.domain.schemas import AppConfigResponse
from app.services.config_service import config_service

router = APIRouter()


@router.get("/app-config", response_model=AppConfigResponse)
async def get_app_config(
    platform: str = Query(default="ios", pattern="^ios$"),
    version: str = Query(default="1.0.0"),
    language: str = Query(default="en", pattern="^(en|sw)$"),
) -> AppConfigResponse:
    return config_service.get_app_config(platform=platform, version=version, language=language)
