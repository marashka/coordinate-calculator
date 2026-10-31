# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import http
from typing import Any, Literal

from pydantic import BaseModel

from coordinate_calculator.errors.base import BaseErrorSchema
from coordinate_calculator.errors.registration import register_error_response
from coordinate_calculator.exceptions.entity import EntityNotFoundError


class NotFoundDetailsSchema(BaseModel):
    entity_type: str
    field: str
    value: Any


@register_error_response(
    exception=EntityNotFoundError,
    status=http.HTTPStatus.NOT_FOUND,
)
class NotFoundSchema(BaseErrorSchema):
    code: Literal["not_found"] = "not_found"
    details: NotFoundDetailsSchema
