# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import os
import secrets
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy import create_engine, make_url, text
from sqlalchemy_utils.functions import create_database, database_exists

from coordinate_calculator.db.models import Base
from coordinate_calculator.db.settings import DatabaseApplicationSettings
from tests.test_database.utils import do_run_migrations

if TYPE_CHECKING:
    from collections.abc import Generator

    from sqlalchemy.engine import URL

_PROJECT = Path(__file__).resolve().parents[2] / "coordinate_calculator"


@pytest.fixture(scope="session")
def sync_database_url() -> Generator[str]:
    database_name = secrets.token_hex(8)
    url = make_url(str(DatabaseApplicationSettings().database.url)).set(
        drivername="postgresql+psycopg",
        database=database_name,
    )
    rendered = url.render_as_string(hide_password=False)
    if not database_exists(rendered):
        create_database(rendered)

    yield rendered

    _drop_database(url)


@pytest.fixture(scope="session")
def database_migrations(sync_database_url: str) -> str:
    config = AlembicConfig(_PROJECT / "db/migrations/alembic.ini")
    config.set_main_option("sqlalchemy.url", sync_database_url)
    config.set_main_option("script_location", os.fspath(_PROJECT / "db/migrations"))
    do_run_migrations(config, Base.metadata, "head")
    return sync_database_url


def _drop_database(url: URL) -> None:
    admin = url.set(database="postgres")
    engine = create_engine(admin, isolation_level="AUTOCOMMIT")
    try:
        with engine.connect() as connection:
            connection.execute(text(f'DROP DATABASE IF EXISTS "{url.database}" WITH (FORCE)'))
    finally:
        engine.dispose()
