# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from coordinate_calculator.exceptions.base import ApplicationError


class CalculationError(ApplicationError):
    """Orbital elements could not be propagated."""

    def __init__(self, message: str) -> None:
        self._message = message

    @property
    def message(self) -> str:
        return self._message

    @property
    def details(self) -> None:
        return None
