from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecisionIntelligenceResult:
    severity_score: int
    risk_score: int
    confidence: float
    risk_factors: tuple[str, ...]
    recommended_action: str
    review_priority: str
    public_guidance_allowed: bool
    needs_human_review: bool
    matched_escalation_terms: int
    pii_detected: bool
    safety_flag_count: int
    safety_flags: str
    model_version: str

    @property
    def urgency(self) -> str:
        return "high" if self.review_priority in {"high", "critical"} else "standard"

    def to_labels(self) -> dict[str, str | int | float | bool]:
        return {
            "severity_score": self.severity_score,
            "risk_score": self.risk_score,
            "confidence": self.confidence,
            "risk_factors": ",".join(self.risk_factors),
            "recommended_action": self.recommended_action,
            "review_priority": self.review_priority,
            "public_guidance_allowed": self.public_guidance_allowed,
            "needs_human_review": self.needs_human_review,
            "urgency": self.urgency,
            "matched_escalation_terms": self.matched_escalation_terms,
            "pii_detected": self.pii_detected,
            "safety_flag_count": self.safety_flag_count,
            "safety_flags": self.safety_flags,
            "model_version": self.model_version,
        }
