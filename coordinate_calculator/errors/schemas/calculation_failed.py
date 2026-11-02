# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import http
from typing import Literal

from coordinate_calculator.errors.base import BaseErrorSchema
from coordinate_calculator.errors.registration import register_error_response
from coordinate_calculator.exceptions import CalculationError


@register_error_response(
    exception=CalculationError,
    status=http.HTTPStatus.BAD_REQUEST,
)
class CalculationFailedSchema(BaseErrorSchema):
    code: Literal["calculation_failed"] = "calculation_failed"
    details: None = None
