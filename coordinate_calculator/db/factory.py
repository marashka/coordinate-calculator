# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

if TYPE_CHECKING:
    from coordinate_calculator.db.settings import DatabaseSettings


def create_session_factory(settings: DatabaseSettings) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(url=str(settings.url), **settings.model_dump(exclude={"url"}))
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
