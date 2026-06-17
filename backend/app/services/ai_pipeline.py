from app.domain.enums import ReportStatus
from app.domain.records import ReportRecord
from app.repositories.protocols import ReportStore, RiskStore
from app.services.decision_intelligence_service import decision_intelligence_service


class AiPipeline:
    """Runs decision intelligence and applies backend workflow decisions."""

    async def process_report(
        self,
        report_reference: str,
        report_store: ReportStore,
        risk_store: RiskStore,
    ) -> ReportRecord | None:
        record = await report_store.get(report_reference)
        if record is None:
            return None

        labels = self.classify(record)
        needs_human_review = bool(labels["needs_human_review"])
        status = ReportStatus.under_review if needs_human_review else ReportStatus.aggregated
        updated = await report_store.update_status(
            report_reference,
            status=status,
            ai_labels=labels,
        )
        await risk_store.bump_for_report(
            record.county,
            severity_score=int(labels["severity_score"]),
            county_code=record.county_code,
        )
        return updated

    def classify(self, record: ReportRecord) -> dict[str, str | int | float | bool]:
        return decision_intelligence_service.score(record).to_labels()


ai_pipeline = AiPipeline()
