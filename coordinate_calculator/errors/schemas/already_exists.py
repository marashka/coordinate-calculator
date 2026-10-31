# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import http
from typing import Any, Literal

from pydantic import BaseModel

from coordinate_calculator.errors.base import BaseErrorSchema
from coordinate_calculator.errors.registration import register_error_response
from coordinate_calculator.exceptions.entity import EntityAlreadyExistsError


class AlreadyExistsDetailsSchema(BaseModel):
    entity_type: str
    field: str
    value: Any


@register_error_response(
    exception=EntityAlreadyExistsError,
    status=http.HTTPStatus.CONFLICT,
)
class AlreadyExistsSchema(BaseErrorSchema):
    code: Literal["conflict"] = "conflict"
    details: AlreadyExistsDetailsSchema
