from app.domain.enums import IncidentCategory, ReportStatus
from app.domain.records import ReportRecord
from app.repositories.protocols import ReportStore, RiskStore


class AiPipeline:
    """Small deterministic MVP classifier that stands in for a future AI worker."""

    _urgent_words = {
        "attack",
        "burn",
        "kill",
        "weapon",
        "machete",
        "panga",
        "stone",
        "revenge",
        "riot",
        "clash",
        "incite",
    }

    _high_risk_categories = {
        IncidentCategory.active_violence,
        IncidentCategory.violence_threat,
        IncidentCategory.hate_speech_or_incitement,
        IncidentCategory.suspicious_mobilization,
    }

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
        )
        return updated

    def classify(self, record: ReportRecord) -> dict[str, str | int | float | bool]:
        text = record.description.lower()
        urgent_matches = [word for word in self._urgent_words if word in text]
        base_score = 25

        if record.category in self._high_risk_categories:
            base_score += 30
        if urgent_matches:
            base_score += min(30, len(urgent_matches) * 10)
        if record.category == IncidentCategory.misinformation_or_rumor:
            base_score += 10

        severity_score = min(base_score, 100)
        needs_human_review = (
            severity_score >= 65 or record.category == IncidentCategory.active_violence
        )

        return {
            "severity_score": severity_score,
            "urgency": "high" if severity_score >= 65 else "standard",
            "needs_human_review": needs_human_review,
            "matched_escalation_terms": len(urgent_matches),
            "model_version": "rules-mvp-0.1",
        }


ai_pipeline = AiPipeline()
