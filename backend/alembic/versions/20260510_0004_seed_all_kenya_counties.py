"""seed all kenya counties

Revision ID: 20260510_0004
Revises: 20260509_0003
Create Date: 2026-05-10
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260510_0004"
down_revision: str | None = "20260509_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

COUNTIES: tuple[tuple[str, str, int], ...] = (
    ("KE-001", "Mombasa", 20),
    ("KE-002", "Kwale", 20),
    ("KE-003", "Kilifi", 20),
    ("KE-004", "Tana River", 20),
    ("KE-005", "Lamu", 20),
    ("KE-006", "Taita Taveta", 20),
    ("KE-007", "Garissa", 20),
    ("KE-008", "Wajir", 20),
    ("KE-009", "Mandera", 20),
    ("KE-010", "Marsabit", 20),
    ("KE-011", "Isiolo", 20),
    ("KE-012", "Meru", 20),
    ("KE-013", "Tharaka Nithi", 20),
    ("KE-014", "Embu", 20),
    ("KE-015", "Kitui", 20),
    ("KE-016", "Machakos", 20),
    ("KE-017", "Makueni", 20),
    ("KE-018", "Nyandarua", 20),
    ("KE-019", "Nyeri", 20),
    ("KE-020", "Kirinyaga", 20),
    ("KE-021", "Murang'a", 20),
    ("KE-022", "Kiambu", 20),
    ("KE-023", "Turkana", 20),
    ("KE-024", "West Pokot", 20),
    ("KE-025", "Samburu", 20),
    ("KE-026", "Trans Nzoia", 20),
    ("KE-027", "Uasin Gishu", 20),
    ("KE-028", "Elgeyo Marakwet", 20),
    ("KE-029", "Nandi", 20),
    ("KE-030", "Baringo", 20),
    ("KE-031", "Laikipia", 20),
    ("KE-032", "Nakuru", 20),
    ("KE-033", "Narok", 20),
    ("KE-034", "Kajiado", 20),
    ("KE-035", "Kericho", 20),
    ("KE-036", "Bomet", 20),
    ("KE-037", "Kakamega", 20),
    ("KE-038", "Vihiga", 20),
    ("KE-039", "Bungoma", 20),
    ("KE-040", "Busia", 20),
    ("KE-041", "Siaya", 20),
    ("KE-042", "Kisumu", 28),
    ("KE-043", "Homa Bay", 20),
    ("KE-044", "Migori", 20),
    ("KE-045", "Kisii", 20),
    ("KE-046", "Nyamira", 20),
    ("KE-047", "Nairobi", 54),
)


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text("DELETE FROM county_risk"))
    for county_code, county_name, score in COUNTIES:
        risk_level = "moderate" if score >= 40 else "low"
        summary = (
            "Community reports and public signals suggest elevated tension in some areas."
            if risk_level == "moderate"
            else "No unusual risk signals are currently visible in aggregated guidance."
        )
        bind.execute(
            sa.text(
                """
                INSERT INTO county_risk
                    (county_code, county_name, risk_level, score, updated_at, summary, guidance)
                VALUES
                    (:county_code, :county_name, :risk_level, :score, NOW(), :summary,
                     CAST(:guidance AS jsonb))
                """
            ),
            {
                "county_code": county_code,
                "county_name": county_name,
                "risk_level": risk_level,
                "score": score,
                "summary": summary,
                "guidance": (
                    '["Avoid sharing unverified claims.",'
                    '"Move away from crowds if tensions rise.",'
                    '"Use anonymous reporting if you witness intimidation."]'
                ),
            },
        )


def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text("DELETE FROM county_risk"))
    bind.execute(
        sa.text(
            """
            INSERT INTO county_risk
                (county_code, county_name, risk_level, score, updated_at, summary, guidance)
            VALUES
                (
                    'KE-30',
                    'Nairobi',
                    'moderate',
                    54,
                    NOW(),
                    'Community reports and public signals suggest elevated tension in some areas.',
                    '[
                        "Avoid sharing unverified claims.",
                        "Move away from crowds if tensions rise.",
                        "Use anonymous reporting if you witness intimidation."
                    ]'::jsonb
                ),
                (
                    'KE-42',
                    'Kisumu',
                    'low',
                    28,
                    NOW(),
                    'No unusual risk signals are currently visible in aggregated guidance.',
                    '[
                        "Continue verifying information before sharing.",
                        "Report intimidation or threats anonymously if you witness them."
                    ]'::jsonb
                )
            """
        )
    )
