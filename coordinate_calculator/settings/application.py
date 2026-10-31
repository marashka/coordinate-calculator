# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from pydantic import Field

from coordinate_calculator.db.settings import DatabaseSettings
from coordinate_calculator.logging import DEFAULT_LOGGING_SETTINGS, LoggingSettings
from coordinate_calculator.settings.base import BaseSettings
from coordinate_calculator.settings.server import ServerSettings


class ApplicationSettings(BaseSettings):
    """Application settings.

    Sources, in descending order of priority:

    * Arguments passed to the constructor
    * ``config.yml``, or the file set by ``COORDINATE_CALCULATOR_CONFIG_FILE``
    * Environment variables prefixed with ``COORDINATE_CALCULATOR__``, with ``__`` between nested fields
    """

    database: DatabaseSettings = Field(
        default_factory=DatabaseSettings,  # type: ignore[arg-type]
        description="Database settings",
    )
    logging: LoggingSettings = Field(
        default=DEFAULT_LOGGING_SETTINGS,
        description="Logging settings",
    )
    server: ServerSettings = Field(
        default_factory=ServerSettings,
        description="Server settings",
    )
