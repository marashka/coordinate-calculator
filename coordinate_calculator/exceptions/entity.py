# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import Any

from coordinate_calculator.exceptions.base import ApplicationError


class EntityNotFoundError(ApplicationError):
    """Entity not found."""

    entity_type: str
    field: str
    value: Any

    def __init__(self, entity_type: str, field: str, value: Any):
        self.entity_type = entity_type
        self.field = field
        self.value = value

    @property
    def message(self) -> str:
        return f"{self.entity_type} not found"

    @property
    def details(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "field": self.field,
            "value": self.value,
        }


class EntityAlreadyExistsError(ApplicationError):
    """Entity already exists."""

    entity_type: str
    field: str
    value: Any

    def __init__(
        self,
        entity_type: str,
        field: str,
        value: Any,
        *,
        message: str | None = None,
    ):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        self._message = message

    @property
    def message(self) -> str:
        return self._message or f"{self.entity_type} already exists"

    @property
    def details(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "field": self.field,
            "value": self.value,
        }
