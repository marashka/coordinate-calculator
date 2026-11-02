# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import TYPE_CHECKING

import pytest_asyncio
from sqlalchemy import delete

from coordinate_calculator.db.models import Base

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@pytest_asyncio.fixture(autouse=True)
async def cleanup_database(
    async_session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[None]:
    yield
    async with async_session_maker() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(delete(table))
        await session.commit()
