# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
"""Create spacecraft

Revision ID: 21e35c0e3a97
Revises:
Create Date: 2026-11-01 22:49:24.281773

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "21e35c0e3a97"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "spacecraft",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("norad_id", sa.Integer(), nullable=False),
        sa.Column("international_designator", sa.String(length=16), nullable=False),
        sa.Column("launch_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__spacecraft")),
        sa.UniqueConstraint("norad_id", name=op.f("uq__spacecraft__norad_id")),
        sa.UniqueConstraint(
            "international_designator",
            name=op.f("uq__spacecraft__international_designator"),
        ),
    )


def downgrade() -> None:
    op.drop_table("spacecraft")
