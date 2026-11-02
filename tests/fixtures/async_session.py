# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncEngine


@pytest.fixture(scope="session")
async def async_session_maker(async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest.fixture
async def db_session(
    async_session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    session = async_session_maker()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
