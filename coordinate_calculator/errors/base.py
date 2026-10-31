# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import Any, TypeVar

from pydantic import BaseModel


class BaseErrorSchema(BaseModel):
    code: str
    message: str
    details: Any


ErrorModel = TypeVar("ErrorModel", bound=BaseErrorSchema)


class APIErrorSchema[ErrorModel: BaseErrorSchema](BaseModel):
    error: ErrorModel
