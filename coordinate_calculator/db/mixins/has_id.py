# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from uuid import UUID, uuid8

from sqlalchemy import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column


class HasId:
    id: Mapped[UUID] = mapped_column(
        SQL_UUID,
        primary_key=True,
        default=uuid8,
        nullable=False,
    )
