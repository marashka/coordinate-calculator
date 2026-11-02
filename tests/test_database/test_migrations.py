# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import pytest
from alembic.autogenerate import compare_metadata
from alembic.runtime.migration import MigrationContext
from sqlalchemy import Connection, MetaData, create_engine
from sqlalchemy.pool import NullPool

from coordinate_calculator.db.models import Base

pytestmark = pytest.mark.db


def get_diff_db_metadata(connection: Connection, metadata: MetaData):
    migration_ctx = MigrationContext.configure(connection)
    return compare_metadata(context=migration_ctx, metadata=metadata)


def test_migrations_up_to_date(
    request: pytest.FixtureRequest,
    database_migrations: str,
):
    engine = create_engine(database_migrations, poolclass=NullPool)

    def finalizer():
        engine.dispose()

    request.addfinalizer(finalizer)

    with engine.connect() as connection:
        diff = get_diff_db_metadata(connection, metadata=Base.metadata)
    assert not diff
