import secrets
import string
from datetime import UTC, datetime

from app.core.abuse import duplicate_report_guard
from app.core.config import get_settings
from app.domain.enums import ReportStatus
from app.domain.records import ReportRecord
from app.domain.schemas import ReportCreate, ReportReceipt, ReportStatusResponse
from app.repositories.protocols import ReportStore


class ReportService:
    async def submit_report(
        self,
        payload: ReportCreate,
        store: ReportStore,
    ) -> tuple[ReportReceipt, ReportRecord]:
        now = datetime.now(UTC)
        settings = get_settings()
        duplicate_signal, duplicate_fingerprint = duplicate_report_guard.assess(
            category=payload.category.value,
            county=payload.location.county,
            description=payload.description,
            window_seconds=settings.duplicate_report_window_seconds,
        )
        record = ReportRecord(
            report_reference=self._new_reference(),
            client_report_id=payload.client_report_id,
            category=payload.category,
            description=payload.description.strip(),
            incident_time=payload.incident_time,
            location=payload.location,
            language=payload.language,
            source=payload.source,
            app_version=payload.app_version,
            status=ReportStatus.received,
            received_at=now,
            updated_at=now,
            ai_labels={
                "duplicate_signal": duplicate_signal,
                "duplicate_fingerprint": duplicate_fingerprint,
            },
        )
        stored = await store.create(record)
        receipt = ReportReceipt(
            report_reference=stored.report_reference,
            status=stored.status,
            received_at=stored.received_at,
            message="Your anonymous report was received.",
        )
        return receipt, stored

    async def get_report_status(
        self,
        report_reference: str,
        store: ReportStore,
    ) -> ReportStatusResponse | None:
        record = await store.get(report_reference)
        if record is None:
            return None
        message_by_status = {
            ReportStatus.received: "Your report has been received.",
            ReportStatus.under_review: "Your report has been received and is being reviewed.",
            ReportStatus.aggregated: (
                "Your report has been included in aggregated peace intelligence."
            ),
            ReportStatus.closed: "Review for this report is complete.",
            ReportStatus.unable_to_process: "This report could not be processed.",
        }
        return ReportStatusResponse(
            report_reference=record.report_reference,
            status=record.status,
            updated_at=record.updated_at,
            display_message=message_by_status[record.status],
        )

    def _new_reference(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        suffix = "".join(secrets.choice(alphabet) for _ in range(6))
        return f"AP-2027-{suffix}"


report_service = ReportService()
