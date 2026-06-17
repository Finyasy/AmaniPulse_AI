"""add report county code

Revision ID: 20260513_0006
Revises: 20260511_0005
Create Date: 2026-05-13
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260513_0006"
down_revision: str | None = "20260511_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("reports", sa.Column("county_code", sa.String(length=16), nullable=True))
    op.create_index("ix_reports_county_code", "reports", ["county_code"])
    op.execute(
        sa.text(
            """
            UPDATE reports
            SET county_code = county_risk.county_code
            FROM county_risk
            WHERE lower(reports.county) = lower(county_risk.county_name)
            """
        )
    )


def downgrade() -> None:
    op.drop_index("ix_reports_county_code", table_name="reports")
    op.drop_column("reports", "county_code")
