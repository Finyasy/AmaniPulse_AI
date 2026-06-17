from typing import Protocol

from app.domain.enums import ReportStatus
from app.domain.records import ReportRecord
from app.domain.review import ReviewEventRecord
from app.domain.schemas import CountyRiskResponse


class ReportStore(Protocol):
    async def create(self, record: ReportRecord) -> ReportRecord:
        pass

    async def get(self, report_reference: str) -> ReportRecord | None:
        pass

    async def update_status(
        self,
        report_reference: str,
        status: ReportStatus,
        ai_labels: dict[str, str | int | float | bool] | None = None,
    ) -> ReportRecord | None:
        pass

    async def list_by_status(
        self,
        status: ReportStatus,
        limit: int = 50,
    ) -> list[ReportRecord]:
        pass

    async def add_review_event(self, event: ReviewEventRecord) -> ReviewEventRecord:
        pass

    async def list_review_events(
        self,
        report_reference: str,
        limit: int = 50,
    ) -> list[ReviewEventRecord]:
        pass


class RiskStore(Protocol):
    async def get(self, county_code: str) -> CountyRiskResponse | None:
        pass

    async def county_code_for_name(self, county_name: str | None) -> str | None:
        pass

    async def bump_for_report(
        self,
        county_name: str | None,
        severity_score: int,
        county_code: str | None = None,
    ) -> CountyRiskResponse | None:
        pass
