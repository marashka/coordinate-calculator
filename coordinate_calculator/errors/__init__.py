# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from coordinate_calculator.errors.base import BaseErrorSchema
from coordinate_calculator.errors.registration import (
    APIErrorResponse,
    get_error_responses,
    get_response_for_exception,
    get_response_for_status_code,
)

__all__ = [
    "APIErrorResponse",
    "BaseErrorSchema",
    "get_error_responses",
    "get_response_for_exception",
    "get_response_for_status_code",
]
