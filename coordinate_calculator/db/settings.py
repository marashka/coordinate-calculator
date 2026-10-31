# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import textwrap
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, PostgresDsn, UrlConstraints
from sqlalchemy import make_url

from coordinate_calculator.logging import DEFAULT_LOGGING_SETTINGS, LoggingSettings
from coordinate_calculator.settings.base import BaseSettings


def validate_url(value: PostgresDsn):
    url = make_url(str(value))
    if not url.database:
        message = "Database URL must contain database name"
        raise ValueError(message)

    if not url.username or not url.password:
        message = "Database URL must contain username and password"
        raise ValueError(message)

    return value


PostgresURL = Annotated[
    PostgresDsn,
    UrlConstraints(
        allowed_schemes=["postgresql+asyncpg", "postgresql+psycopg"],
        default_port=5432,
        host_required=True,
    ),
    AfterValidator(validate_url),
]


class DatabaseSettings(BaseModel):
    """Database settings.

    Extra fields are passed through to the SQLAlchemy engine.
    """

    url: PostgresURL = Field(
        description=textwrap.dedent(
            """
            Database connection URL.

            Mandatory components:

            * host
            * username (urlencoded)
            * password (urlencoded)

            Only async drivers are supported: ``postgresql+asyncpg`` and ``postgresql+psycopg``.
            """,
        ),
    )

    model_config = ConfigDict(extra="allow")

    def __repr_args__(self):
        safe_url = make_url(str(self.url)).render_as_string(hide_password=True)
        extra = super().__repr_args__()
        return [
            ("url", safe_url),
            *[item for item in extra if item[0] != "url"],
        ]


class DatabaseApplicationSettings(BaseSettings):
    """Settings used by database migrations and maintenance scripts."""

    database: DatabaseSettings = Field(
        default_factory=DatabaseSettings,  # type: ignore[arg-type]
        description="Database settings",
    )
    logging: LoggingSettings = Field(
        default=DEFAULT_LOGGING_SETTINGS,
        description="Logging settings",
    )
