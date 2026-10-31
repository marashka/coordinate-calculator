# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import http
from typing import Any, Literal

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from coordinate_calculator.errors.base import BaseErrorSchema
from coordinate_calculator.errors.registration import register_error_response


class InvalidRequestBaseErrorSchema(BaseModel):
    loc: list[str | int] = Field(alias="location")
    msg: str = Field(alias="message")
    type: str = Field(alias="code")
    ctx: dict = Field(default_factory=dict, alias="context")
    input: Any = Field(default=None)

    model_config = ConfigDict(populate_by_name=True)


@register_error_response(
    exception=RequestValidationError,
    status=http.HTTPStatus.UNPROCESSABLE_ENTITY,
)
@register_error_response(
    exception=ValidationError,
    status=http.HTTPStatus.UNPROCESSABLE_ENTITY,
)
class InvalidRequestSchema(BaseErrorSchema):
    code: Literal["invalid_request"] = "invalid_request"
    message: Literal["Invalid request"] = "Invalid request"
    details: list[InvalidRequestBaseErrorSchema]
