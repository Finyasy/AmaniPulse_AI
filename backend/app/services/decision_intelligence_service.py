from app.domain.enums import IncidentCategory
from app.domain.intelligence import DecisionIntelligenceResult
from app.domain.records import ReportRecord
from app.services.safety_service import safety_service


class DecisionIntelligenceService:
    """Swappable MVP decision-intelligence provider.

    The current provider is deterministic and auditable. It produces the same output shape a
    future NLP/ML provider should preserve, so downstream review and risk systems stay stable.
    """

    model_version = "decision-rules-mvp-0.2"

    _escalation_terms = {
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
        "mobilize",
        "threat",
        "armed",
    }

    _high_risk_categories = {
        IncidentCategory.active_violence,
        IncidentCategory.violence_threat,
        IncidentCategory.hate_speech_or_incitement,
        IncidentCategory.suspicious_mobilization,
    }

    _category_weights = {
        IncidentCategory.active_violence: 45,
        IncidentCategory.violence_threat: 35,
        IncidentCategory.hate_speech_or_incitement: 35,
        IncidentCategory.suspicious_mobilization: 30,
        IncidentCategory.voter_intimidation: 25,
        IncidentCategory.authority_abuse: 22,
        IncidentCategory.corruption_bribery_or_coercion: 18,
        IncidentCategory.misinformation_or_rumor: 16,
        IncidentCategory.other_election_safety_concern: 10,
    }

    def score(self, record: ReportRecord) -> DecisionIntelligenceResult:
        text = record.description.lower()
        matched_terms = sorted(term for term in self._escalation_terms if term in text)
        safety = safety_service.assess_text(record.description)
        duplicate_signal = bool(record.ai_labels.get("duplicate_signal", False))
        risk_factors = self._risk_factors(record, matched_terms, safety.pii_detected)

        category_weight = self._category_weights[record.category]
        escalation_weight = min(30, len(matched_terms) * 8)
        pii_weight = 7 if safety.pii_detected else 0
        duplicate_weight = 8 if duplicate_signal else 0
        location_weight = 5 if record.county else 0
        severity_score = min(
            100,
            20 + category_weight + escalation_weight + pii_weight + duplicate_weight,
        )
        risk_score = min(100, severity_score + location_weight)
        review_priority = self._review_priority(risk_score, record.category, safety.pii_detected)
        needs_human_review = (
            review_priority in {"high", "critical"} or safety.pii_detected or duplicate_signal
        )

        return DecisionIntelligenceResult(
            severity_score=severity_score,
            risk_score=risk_score,
            confidence=self._confidence(record, matched_terms),
            risk_factors=tuple(risk_factors),
            recommended_action=self._recommended_action(review_priority, duplicate_signal),
            review_priority=review_priority,
            public_guidance_allowed=not needs_human_review and not duplicate_signal,
            needs_human_review=needs_human_review,
            matched_escalation_terms=len(matched_terms),
            pii_detected=safety.pii_detected,
            safety_flag_count=safety.flag_count,
            safety_flags=safety.flag_summary,
            model_version=self.model_version,
        )

    def _risk_factors(
        self,
        record: ReportRecord,
        matched_terms: list[str],
        pii_detected: bool,
    ) -> list[str]:
        factors = [f"category:{record.category.value}"]
        if record.category in self._high_risk_categories:
            factors.append("high_risk_category")
        if matched_terms:
            factors.append("escalation_language")
        if pii_detected:
            factors.append("pii_or_identifying_detail")
        if record.ai_labels.get("duplicate_signal"):
            factors.append("possible_duplicate_or_spam")
        if record.county:
            factors.append("county_signal")
        return factors

    def _review_priority(
        self,
        risk_score: int,
        category: IncidentCategory,
        pii_detected: bool,
    ) -> str:
        if category == IncidentCategory.active_violence or risk_score >= 85:
            return "critical"
        if risk_score >= 65 or pii_detected:
            return "high"
        if risk_score >= 45:
            return "medium"
        return "low"

    def _recommended_action(self, review_priority: str, duplicate_signal: bool) -> str:
        if duplicate_signal:
            return "review_duplicate_before_aggregation"
        if review_priority == "critical":
            return "urgent_human_review"
        if review_priority == "high":
            return "human_review"
        if review_priority == "medium":
            return "aggregate_with_monitoring"
        return "aggregate"

    def _confidence(self, record: ReportRecord, matched_terms: list[str]) -> float:
        confidence = 0.55
        if record.category in self._high_risk_categories:
            confidence += 0.15
        if matched_terms:
            confidence += min(0.2, len(matched_terms) * 0.05)
        if record.county:
            confidence += 0.05
        return round(min(confidence, 0.95), 2)


decision_intelligence_service = DecisionIntelligenceService()
