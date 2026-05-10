from fastapi import APIRouter, Query

from app.domain.schemas import IncidentTaxonomyResponse
from app.services.taxonomy_service import taxonomy_service

router = APIRouter()


@router.get("/incident-taxonomy", response_model=IncidentTaxonomyResponse)
async def get_incident_taxonomy(
    language: str = Query(default="en", pattern="^(en|sw)$"),
) -> IncidentTaxonomyResponse:
    return taxonomy_service.get_taxonomy(language=language)
