# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import http
from typing import Any, Literal

from coordinate_calculator.errors.base import BaseErrorSchema
from coordinate_calculator.errors.registration import register_error_response


@register_error_response(
    exception=NotImplementedError,
    status=http.HTTPStatus.NOT_IMPLEMENTED,
)
class NotImplementedErrorSchema(BaseErrorSchema):
    code: Literal["not_implemented"] = "not_implemented"
    details: Any = None
