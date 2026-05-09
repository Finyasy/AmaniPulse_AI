from datetime import UTC, datetime

from app.domain.enums import ReportStatus
from app.domain.records import ReportRecord
from app.domain.schemas import (
    ReviewDecisionResponse,
    ReviewReportDetail,
    ReviewReportSummary,
)
from app.repositories.protocols import ReportStore


class ReviewService:
    async def list_review_queue(
        self,
        store: ReportStore,
        limit: int,
    ) -> list[ReviewReportSummary]:
        reports = await store.list_by_status(ReportStatus.under_review, limit=limit)
        return [self._to_summary(report) for report in reports]

    async def get_review_report(
        self,
        report_reference: str,
        store: ReportStore,
    ) -> ReviewReportDetail | None:
        report = await store.get(report_reference)
        if report is None:
            return None
        return ReviewReportDetail(
            **self._to_summary(report).model_dump(),
            description=report.description,
            ai_labels=report.ai_labels,
        )

    async def apply_decision(
        self,
        report_reference: str,
        status: ReportStatus,
        reviewer_id: str,
        note: str,
        store: ReportStore,
    ) -> ReviewDecisionResponse | None:
        reviewed_at = datetime.now(UTC)
        updated = await store.update_status(
            report_reference,
            status=status,
            ai_labels={
                "reviewer_id": reviewer_id,
                "review_note": note,
                "reviewed_at": reviewed_at.isoformat(),
            },
        )
        if updated is None:
            return None
        return ReviewDecisionResponse(
            report_reference=updated.report_reference,
            status=updated.status,
            updated_at=updated.updated_at,
            reviewer_id=reviewer_id,
            note=note,
        )

    def _to_summary(self, report: ReportRecord) -> ReviewReportSummary:
        return ReviewReportSummary(
            report_reference=report.report_reference,
            category=report.category,
            status=report.status,
            incident_time=report.incident_time,
            received_at=report.received_at,
            updated_at=report.updated_at,
            county=report.county,
            area_label=report.location.area_label,
            language=report.language,
            severity_score=self._optional_int(report.ai_labels.get("severity_score")),
            urgency=self._optional_str(report.ai_labels.get("urgency")),
            needs_human_review=self._optional_bool(report.ai_labels.get("needs_human_review")),
        )

    def _optional_int(self, value: object) -> int | None:
        return value if isinstance(value, int) else None

    def _optional_str(self, value: object) -> str | None:
        return value if isinstance(value, str) else None

    def _optional_bool(self, value: object) -> bool | None:
        return value if isinstance(value, bool) else None


review_service = ReviewService()
