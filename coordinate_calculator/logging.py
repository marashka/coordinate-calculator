# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import logging.config

from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic_settings_logging import (
    FilterConfig,
    FormatterConfig,
    HandlerConfig,
    LoggerConfig,
    RootLoggerConfig,
    StreamHandlerConfig,
)
from pydantic_settings_logging import (
    LoggingSettings as BaseLoggingSettings,
)

__all__ = [
    "DEFAULT_LOGGING_SETTINGS",
    "LoggingSettings",
    "setup_logging",
]


class CallableFactoryConfig(BaseModel):
    """Logging config entry created by calling a factory, the ``()`` key in ``dictConfig``."""

    model_config = ConfigDict(extra="allow")

    callable: str = Field(
        description="Custom callable",
        validation_alias=AliasChoices("callable", "()"),
        serialization_alias="()",
    )


class LoggingSettings(BaseLoggingSettings):
    """Python logging configuration.

    See the dictionary schema in the
    `logging.config documentation <https://docs.python.org/3/library/logging.config.html#dictionary-schema-details>`_.
    """

    filters: dict[str, FilterConfig | CallableFactoryConfig] = Field(
        default_factory=dict,
        description="Logging filters",
    )
    formatters: dict[str, FormatterConfig | CallableFactoryConfig] = Field(
        default_factory=dict,
        description="Logging formatters",
    )
    handlers: dict[str, HandlerConfig | CallableFactoryConfig] = Field(
        default_factory=dict,
        description="Logging handlers",
    )


DEFAULT_LOGGING_SETTINGS = LoggingSettings(
    disable_existing_loggers=False,
    formatters={
        "plain": FormatterConfig(
            class_="logging.Formatter",
            format="%(asctime)s.%(msecs)03d %(name)s:%(lineno)d [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ),
    },
    handlers={
        "main": StreamHandlerConfig(
            formatter="plain",
            stream="ext://sys.stdout",
        ),
    },
    root=RootLoggerConfig(
        handlers=["main"],
        level="INFO",
    ),
    loggers={
        "uvicorn": LoggerConfig(
            handlers=["main"],
            level="INFO",
            propagate=False,
        ),
    },
)


def setup_logging(settings: LoggingSettings) -> None:
    logging.config.dictConfig(settings.model_dump())
