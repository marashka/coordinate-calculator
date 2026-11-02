# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import asyncio
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import make_url

from coordinate_calculator import application_factory
from coordinate_calculator.settings.application import ApplicationSettings

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture(scope="session")
def client(database_migrations: str) -> Generator[TestClient]:
    async_url = make_url(database_migrations).set(drivername="postgresql+asyncpg")
    settings = ApplicationSettings(database={"url": async_url.render_as_string(hide_password=False)})
    application = application_factory(settings)
    with TestClient(application) as test_client:
        yield test_client
    asyncio.run(application.state.session_factory.kw["bind"].dispose())
