"""add internal api keys

Revision ID: 20260511_0005
Revises: 20260510_0004
Create Date: 2026-05-11
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260511_0005"
down_revision: str | None = "20260510_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

DEV_INTERNAL_TOKEN_SHA256 = "7d2a1692075ec011e6895c425e566d7954a389f79d58aa7f72942124f9f4ab1a"


def upgrade() -> None:
    op.create_table(
        "internal_api_keys",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key_hash", sa.String(length=64), nullable=False),
        sa.Column("reviewer_id", sa.String(length=80), nullable=False),
        sa.Column("role", sa.String(length=40), nullable=False, server_default="reviewer"),
        sa.Column("label", sa.String(length=120), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_internal_api_keys_active", "internal_api_keys", ["active"])
    op.create_index("ix_internal_api_keys_key_hash", "internal_api_keys", ["key_hash"], unique=True)
    op.create_index("ix_internal_api_keys_reviewer_id", "internal_api_keys", ["reviewer_id"])
    op.create_index("ix_internal_api_keys_role", "internal_api_keys", ["role"])

    bind = op.get_bind()
    bind.execute(
        sa.text(
            """
            INSERT INTO internal_api_keys
                (key_hash, reviewer_id, role, label, active, created_at)
            VALUES
                (:key_hash, 'dev-reviewer', 'reviewer', 'Local development reviewer', true, NOW())
            """
        ),
        {"key_hash": DEV_INTERNAL_TOKEN_SHA256},
    )


def downgrade() -> None:
    op.drop_index("ix_internal_api_keys_role", table_name="internal_api_keys")
    op.drop_index("ix_internal_api_keys_reviewer_id", table_name="internal_api_keys")
    op.drop_index("ix_internal_api_keys_key_hash", table_name="internal_api_keys")
    op.drop_index("ix_internal_api_keys_active", table_name="internal_api_keys")
    op.drop_table("internal_api_keys")
