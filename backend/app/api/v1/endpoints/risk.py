from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_risk_store
from app.domain.schemas import CountyRiskResponse
from app.repositories.protocols import RiskStore
from app.services.risk_service import risk_service

router = APIRouter()
RiskStoreDep = Annotated[RiskStore, Depends(get_risk_store)]


@router.get("/risk/county/{county_code}", response_model=CountyRiskResponse)
async def get_county_risk(
    county_code: str,
    store: RiskStoreDep,
) -> CountyRiskResponse:
    risk = await risk_service.get_county_risk(county_code=county_code, store=store)
    if risk is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "county_not_found",
                "message": "Risk guidance is not available for that county.",
            },
        )
    return risk
