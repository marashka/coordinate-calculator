# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from fastapi import FastAPI

from coordinate_calculator.logging import setup_logging
from coordinate_calculator.settings.application import ApplicationSettings

__version__ = "0.1.0"


def application_factory(settings: ApplicationSettings) -> FastAPI:
    """Build the FastAPI application."""
    application = FastAPI(
        title="coordinate-calculator",
        description="Service that calculates spacecraft coordinates from orbital data",
        version=__version__,
    )
    application.state.settings = settings
    return application


def get_application() -> FastAPI:
    """Load settings, configure logging, and build the application."""
    settings = ApplicationSettings()
    setup_logging(settings.logging)
    return application_factory(settings)
