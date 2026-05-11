from dataclasses import dataclass

from app.domain.enums import RiskLevel


@dataclass(frozen=True, slots=True)
class CountyRiskSeed:
    county_code: str
    county_name: str
    score: int = 20

    @property
    def risk_level(self) -> RiskLevel:
        if self.score >= 80:
            return RiskLevel.critical
        if self.score >= 65:
            return RiskLevel.high
        if self.score >= 40:
            return RiskLevel.moderate
        return RiskLevel.low

    @property
    def summary(self) -> str:
        if self.risk_level == RiskLevel.moderate:
            return (
                "Community reports and public signals suggest elevated tension "
                "in some areas."
            )
        return "No unusual risk signals are currently visible in aggregated guidance."

    @property
    def guidance(self) -> list[str]:
        return [
            "Avoid sharing unverified claims.",
            "Move away from crowds if tensions rise.",
            "Use anonymous reporting if you witness intimidation.",
        ]


KENYA_COUNTY_RISK_SEEDS: tuple[CountyRiskSeed, ...] = (
    CountyRiskSeed("KE-001", "Mombasa"),
    CountyRiskSeed("KE-002", "Kwale"),
    CountyRiskSeed("KE-003", "Kilifi"),
    CountyRiskSeed("KE-004", "Tana River"),
    CountyRiskSeed("KE-005", "Lamu"),
    CountyRiskSeed("KE-006", "Taita Taveta"),
    CountyRiskSeed("KE-007", "Garissa"),
    CountyRiskSeed("KE-008", "Wajir"),
    CountyRiskSeed("KE-009", "Mandera"),
    CountyRiskSeed("KE-010", "Marsabit"),
    CountyRiskSeed("KE-011", "Isiolo"),
    CountyRiskSeed("KE-012", "Meru"),
    CountyRiskSeed("KE-013", "Tharaka Nithi"),
    CountyRiskSeed("KE-014", "Embu"),
    CountyRiskSeed("KE-015", "Kitui"),
    CountyRiskSeed("KE-016", "Machakos"),
    CountyRiskSeed("KE-017", "Makueni"),
    CountyRiskSeed("KE-018", "Nyandarua"),
    CountyRiskSeed("KE-019", "Nyeri"),
    CountyRiskSeed("KE-020", "Kirinyaga"),
    CountyRiskSeed("KE-021", "Murang'a"),
    CountyRiskSeed("KE-022", "Kiambu"),
    CountyRiskSeed("KE-023", "Turkana"),
    CountyRiskSeed("KE-024", "West Pokot"),
    CountyRiskSeed("KE-025", "Samburu"),
    CountyRiskSeed("KE-026", "Trans Nzoia"),
    CountyRiskSeed("KE-027", "Uasin Gishu"),
    CountyRiskSeed("KE-028", "Elgeyo Marakwet"),
    CountyRiskSeed("KE-029", "Nandi"),
    CountyRiskSeed("KE-030", "Baringo"),
    CountyRiskSeed("KE-031", "Laikipia"),
    CountyRiskSeed("KE-032", "Nakuru"),
    CountyRiskSeed("KE-033", "Narok"),
    CountyRiskSeed("KE-034", "Kajiado"),
    CountyRiskSeed("KE-035", "Kericho"),
    CountyRiskSeed("KE-036", "Bomet"),
    CountyRiskSeed("KE-037", "Kakamega"),
    CountyRiskSeed("KE-038", "Vihiga"),
    CountyRiskSeed("KE-039", "Bungoma"),
    CountyRiskSeed("KE-040", "Busia"),
    CountyRiskSeed("KE-041", "Siaya"),
    CountyRiskSeed("KE-042", "Kisumu", score=28),
    CountyRiskSeed("KE-043", "Homa Bay"),
    CountyRiskSeed("KE-044", "Migori"),
    CountyRiskSeed("KE-045", "Kisii"),
    CountyRiskSeed("KE-046", "Nyamira"),
    CountyRiskSeed("KE-047", "Nairobi", score=54),
)
