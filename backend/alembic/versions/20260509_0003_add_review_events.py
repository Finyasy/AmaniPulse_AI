"""add review events

Revision ID: 20260509_0003
Revises: 20260509_0002
Create Date: 2026-05-09
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260509_0003"
down_revision: str | None = "20260509_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "review_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_reference", sa.String(length=32), nullable=False),
        sa.Column("reviewer_id", sa.String(length=80), nullable=False),
        sa.Column("previous_status", sa.String(length=40), nullable=False),
        sa.Column("new_status", sa.String(length=40), nullable=False),
        sa.Column("note", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_review_events_created_at", "review_events", ["created_at"])
    op.create_index("ix_review_events_new_status", "review_events", ["new_status"])
    op.create_index("ix_review_events_previous_status", "review_events", ["previous_status"])
    op.create_index("ix_review_events_report_reference", "review_events", ["report_reference"])
    op.create_index("ix_review_events_reviewer_id", "review_events", ["reviewer_id"])


def downgrade() -> None:
    op.drop_index("ix_review_events_reviewer_id", table_name="review_events")
    op.drop_index("ix_review_events_report_reference", table_name="review_events")
    op.drop_index("ix_review_events_previous_status", table_name="review_events")
    op.drop_index("ix_review_events_new_status", table_name="review_events")
    op.drop_index("ix_review_events_created_at", table_name="review_events")
    op.drop_table("review_events")
