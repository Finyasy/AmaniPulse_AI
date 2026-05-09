"""initial postgis schema

Revision ID: 20260509_0001
Revises:
Create Date: 2026-05-09
"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "20260509_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "county_risk",
        sa.Column("county_code", sa.String(length=16), nullable=False),
        sa.Column("county_name", sa.String(length=80), nullable=False),
        sa.Column("risk_level", sa.String(length=20), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("guidance", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "centroid",
            geoalchemy2.types.Geometry(
                geometry_type="POINT",
                srid=4326,
                from_text="ST_GeomFromEWKT",
                name="geometry",
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("county_code"),
    )
    op.create_index("ix_county_risk_county_name", "county_risk", ["county_name"], unique=True)
    op.create_index("ix_county_risk_risk_level", "county_risk", ["risk_level"])
    op.create_index("ix_county_risk_updated_at", "county_risk", ["updated_at"])

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_reference", sa.String(length=32), nullable=False),
        sa.Column("client_report_id", sa.String(length=80), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("incident_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location_mode", sa.String(length=40), nullable=False),
        sa.Column("country", sa.String(length=2), nullable=True),
        sa.Column("county", sa.String(length=80), nullable=True),
        sa.Column("area_label", sa.String(length=120), nullable=True),
        sa.Column("latitude_rounded", sa.Float(), nullable=True),
        sa.Column("longitude_rounded", sa.Float(), nullable=True),
        sa.Column("precision_km", sa.Integer(), nullable=True),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("source", sa.String(length=40), nullable=False),
        sa.Column("app_version", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ai_labels", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reports_app_source", "reports", ["source"])
    op.create_index("ix_reports_category", "reports", ["category"])
    op.create_index("ix_reports_client_report_id", "reports", ["client_report_id"], unique=True)
    op.create_index("ix_reports_country", "reports", ["country"])
    op.create_index("ix_reports_county", "reports", ["county"])
    op.create_index("ix_reports_incident_time", "reports", ["incident_time"])
    op.create_index("ix_reports_language", "reports", ["language"])
    op.create_index("ix_reports_location_mode", "reports", ["location_mode"])
    op.create_index("ix_reports_received_at", "reports", ["received_at"])
    op.create_index("ix_reports_report_reference", "reports", ["report_reference"], unique=True)
    op.create_index("ix_reports_status", "reports", ["status"])
    op.create_index("ix_reports_updated_at", "reports", ["updated_at"])

    op.execute(
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


def downgrade() -> None:
    op.drop_index("ix_reports_updated_at", table_name="reports")
    op.drop_index("ix_reports_status", table_name="reports")
    op.drop_index("ix_reports_report_reference", table_name="reports")
    op.drop_index("ix_reports_received_at", table_name="reports")
    op.drop_index("ix_reports_location_mode", table_name="reports")
    op.drop_index("ix_reports_language", table_name="reports")
    op.drop_index("ix_reports_incident_time", table_name="reports")
    op.drop_index("ix_reports_county", table_name="reports")
    op.drop_index("ix_reports_country", table_name="reports")
    op.drop_index("ix_reports_client_report_id", table_name="reports")
    op.drop_index("ix_reports_category", table_name="reports")
    op.drop_index("ix_reports_app_source", table_name="reports")
    op.drop_table("reports")

    op.drop_index("ix_county_risk_updated_at", table_name="county_risk")
    op.drop_index("ix_county_risk_risk_level", table_name="county_risk")
    op.drop_index("ix_county_risk_county_name", table_name="county_risk")
    op.drop_table("county_risk")
