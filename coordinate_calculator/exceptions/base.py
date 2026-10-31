# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from abc import ABC, abstractmethod
from typing import Any


class ApplicationError(ABC, Exception):
    """Base class for exceptions raised by coordinate-calculator."""

    @property
    @abstractmethod
    def message(self) -> str:
        """Message string."""
        ...

    @property
    @abstractmethod
    def details(self) -> Any:
        """Details related to specific error."""
        ...

    def __str__(self) -> str:
        return self.message
