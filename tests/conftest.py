# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
pytest_plugins = [
    "tests.factories.spacecraft",
    "tests.fixtures.alembic",
    "tests.fixtures.async_engine",
    "tests.fixtures.async_session",
    "tests.fixtures.client",
]
