from app.domain.schemas import CountyRiskResponse
from app.repositories.protocols import RiskStore


class RiskService:
    async def get_county_risk(
        self,
        county_code: str,
        store: RiskStore,
    ) -> CountyRiskResponse | None:
        return await store.get(county_code)


risk_service = RiskService()
