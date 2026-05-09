from datetime import UTC, datetime
from threading import Lock

from app.domain.enums import ReportStatus, RiskLevel
from app.domain.records import ReportRecord
from app.domain.schemas import CountyRiskResponse


class InMemoryReportStore:
    def __init__(self) -> None:
        self._reports: dict[str, ReportRecord] = {}
        self._client_ids: set[str] = set()
        self._lock = Lock()

    async def create(self, record: ReportRecord) -> ReportRecord:
        with self._lock:
            if record.client_report_id in self._client_ids:
                existing = next(
                    item
                    for item in self._reports.values()
                    if item.client_report_id == record.client_report_id
                )
                return existing
            self._reports[record.report_reference] = record
            self._client_ids.add(record.client_report_id)
            return record

    async def get(self, report_reference: str) -> ReportRecord | None:
        with self._lock:
            return self._reports.get(report_reference)

    async def update_status(
        self,
        report_reference: str,
        status: ReportStatus,
        ai_labels: dict[str, str | int | float | bool] | None = None,
    ) -> ReportRecord | None:
        with self._lock:
            record = self._reports.get(report_reference)
            if record is None:
                return None
            record.status = status
            record.updated_at = datetime.now(UTC)
            if ai_labels:
                record.ai_labels.update(ai_labels)
            return record

    async def list_by_status(
        self,
        status: ReportStatus,
        limit: int = 50,
    ) -> list[ReportRecord]:
        with self._lock:
            matching = [record for record in self._reports.values() if record.status == status]
            return sorted(matching, key=lambda record: record.updated_at, reverse=True)[:limit]


class InMemoryRiskStore:
    def __init__(self) -> None:
        now = datetime.now(UTC)
        self._risk: dict[str, CountyRiskResponse] = {
            "KE-30": CountyRiskResponse(
                county_code="KE-30",
                county_name="Nairobi",
                risk_level=RiskLevel.moderate,
                score=54,
                updated_at=now,
                summary=(
                    "Community reports and public signals suggest elevated tension "
                    "in some areas."
                ),
                guidance=[
                    "Avoid sharing unverified claims.",
                    "Move away from crowds if tensions rise.",
                    "Use anonymous reporting if you witness intimidation.",
                ],
            ),
            "KE-42": CountyRiskResponse(
                county_code="KE-42",
                county_name="Kisumu",
                risk_level=RiskLevel.low,
                score=28,
                updated_at=now,
                summary="No unusual risk signals are currently visible in aggregated guidance.",
                guidance=[
                    "Continue verifying information before sharing.",
                    "Report intimidation or threats anonymously if you witness them.",
                ],
            ),
        }
        self._county_name_to_code = {
            "nairobi": "KE-30",
            "kisumu": "KE-42",
        }
        self._lock = Lock()

    async def get(self, county_code: str) -> CountyRiskResponse | None:
        with self._lock:
            return self._risk.get(county_code.upper())

    async def county_code_for_name(self, county_name: str | None) -> str | None:
        if county_name is None:
            return None
        return self._county_name_to_code.get(county_name.lower())

    async def bump_for_report(
        self,
        county_name: str | None,
        severity_score: int,
    ) -> CountyRiskResponse | None:
        county_code = await self.county_code_for_name(county_name)
        if county_code is None:
            return None
        with self._lock:
            current = self._risk[county_code]
            score = min(100, current.score + max(1, severity_score // 10))
            level = RiskLevel.low
            if score >= 80:
                level = RiskLevel.critical
            elif score >= 65:
                level = RiskLevel.high
            elif score >= 40:
                level = RiskLevel.moderate

            updated = current.model_copy(
                update={
                    "score": score,
                    "risk_level": level,
                    "updated_at": datetime.now(UTC),
                    "summary": (
                        "Recent anonymous reporting has been included in aggregated "
                        "county guidance."
                    ),
                }
            )
            self._risk[county_code] = updated
            return updated


report_store = InMemoryReportStore()
risk_store = InMemoryRiskStore()
