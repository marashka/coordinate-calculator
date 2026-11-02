# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import contextlib
from typing import TYPE_CHECKING

import pytest
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import create_async_engine

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncEngine


@contextlib.asynccontextmanager
async def get_async_engine(database_url: str) -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(database_url)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="session")
def async_database_url(database_migrations: str) -> str:
    url = make_url(database_migrations).set(drivername="postgresql+asyncpg")
    return url.render_as_string(hide_password=False)


@pytest.fixture(scope="session")
async def async_engine(async_database_url: str) -> AsyncGenerator[AsyncEngine]:
    async with get_async_engine(async_database_url) as engine:
        yield engine
