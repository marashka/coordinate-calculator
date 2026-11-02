# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from coordinate_calculator.db.mixins.has_id import HasId
from coordinate_calculator.db.models.base import Base


class Spacecraft(HasId, Base):
    __tablename__ = "spacecraft"

    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    norad_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
    )
    international_designator: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False,
    )
    launch_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
