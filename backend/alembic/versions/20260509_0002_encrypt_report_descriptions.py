"""encrypt report descriptions

Revision ID: 20260509_0002
Revises: 20260509_0001
Create Date: 2026-05-09
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260509_0002"
down_revision: str | None = "20260509_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LEGACY_REDACTED_DESCRIPTION = "redacted-before-encryption-migration"


def upgrade() -> None:
    op.add_column("reports", sa.Column("description_ciphertext", sa.Text(), nullable=True))
    op.execute(
        sa.text(
            "UPDATE reports SET description_ciphertext = :placeholder "
            "WHERE description_ciphertext IS NULL"
        ).bindparams(placeholder=LEGACY_REDACTED_DESCRIPTION)
    )
    op.alter_column("reports", "description_ciphertext", nullable=False)
    op.drop_column("reports", "description")


def downgrade() -> None:
    op.add_column("reports", sa.Column("description", sa.Text(), nullable=True))
    op.execute(
        sa.text(
            "UPDATE reports SET description = '[description encrypted before downgrade]' "
            "WHERE description IS NULL"
        )
    )
    op.alter_column("reports", "description", nullable=False)
    op.drop_column("reports", "description_ciphertext")
