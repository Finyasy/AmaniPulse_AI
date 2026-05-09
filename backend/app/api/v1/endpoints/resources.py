from fastapi import APIRouter, Query

from app.domain.schemas import ResourcesResponse
from app.services.resources_service import resources_service

router = APIRouter()


@router.get("/resources", response_model=ResourcesResponse)
async def get_resources(
    language: str = Query(default="en", pattern="^(en|sw)$"),
    country: str = Query(default="KE", pattern="^KE$"),
) -> ResourcesResponse:
    return resources_service.get_resources(language=language, country=country)
