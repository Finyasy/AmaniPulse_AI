from datetime import UTC, datetime

from app.domain.enums import ReportStatus
from app.domain.records import ReportRecord
from app.domain.review import ReviewEventRecord
from app.domain.schemas import (
    ReviewDecisionResponse,
    ReviewEventItem,
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
        current = await store.get(report_reference)
        if current is None:
            return None
        previous_status = current.status

        updated = await store.update_status(
            report_reference,
            status=status,
            ai_labels={"last_reviewed_at": reviewed_at.isoformat()},
        )
        if updated is None:
            return None
        await store.add_review_event(
            ReviewEventRecord(
                report_reference=report_reference,
                reviewer_id=reviewer_id,
                previous_status=previous_status,
                new_status=status,
                note=note,
                created_at=reviewed_at,
            )
        )
        return ReviewDecisionResponse(
            report_reference=updated.report_reference,
            status=updated.status,
            updated_at=updated.updated_at,
            reviewer_id=reviewer_id,
            note=note,
        )

    async def list_review_events(
        self,
        report_reference: str,
        store: ReportStore,
        limit: int,
    ) -> list[ReviewEventItem] | None:
        if await store.get(report_reference) is None:
            return None
        events = await store.list_review_events(report_reference, limit=limit)
        return [
            ReviewEventItem(
                report_reference=event.report_reference,
                reviewer_id=event.reviewer_id,
                previous_status=event.previous_status,
                new_status=event.new_status,
                note=event.note,
                created_at=event.created_at,
            )
            for event in events
        ]

    def _to_summary(self, report: ReportRecord) -> ReviewReportSummary:
        return ReviewReportSummary(
            report_reference=report.report_reference,
            category=report.category,
            status=report.status,
            incident_time=report.incident_time,
            received_at=report.received_at,
            updated_at=report.updated_at,
            county_code=report.county_code,
            county=report.county,
            area_label=report.location.area_label,
            language=report.language,
            severity_score=self._optional_int(report.ai_labels.get("severity_score")),
            risk_score=self._optional_int(report.ai_labels.get("risk_score")),
            confidence=self._optional_float(report.ai_labels.get("confidence")),
            urgency=self._optional_str(report.ai_labels.get("urgency")),
            review_priority=self._optional_str(report.ai_labels.get("review_priority")),
            recommended_action=self._optional_str(report.ai_labels.get("recommended_action")),
            needs_human_review=self._optional_bool(report.ai_labels.get("needs_human_review")),
        )

    def _optional_int(self, value: object) -> int | None:
        return value if isinstance(value, int) else None

    def _optional_str(self, value: object) -> str | None:
        return value if isinstance(value, str) else None

    def _optional_float(self, value: object) -> float | None:
        return value if isinstance(value, int | float) else None

    def _optional_bool(self, value: object) -> bool | None:
        return value if isinstance(value, bool) else None


review_service = ReviewService()
