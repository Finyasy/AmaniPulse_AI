from fastapi import APIRouter

from app.api.v1.endpoints import app_config, health, reports, resources, review, risk, taxonomy

api_router = APIRouter(prefix="/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(taxonomy.router, tags=["taxonomy"])
api_router.include_router(reports.router, tags=["reports"])
api_router.include_router(risk.router, tags=["risk"])
api_router.include_router(app_config.router, tags=["configuration"])
api_router.include_router(resources.router, tags=["resources"])
api_router.include_router(review.router, tags=["internal-review"])
