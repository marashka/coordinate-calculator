# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from coordinate_calculator.errors.schemas.already_exists import AlreadyExistsSchema
from coordinate_calculator.errors.schemas.calculation_failed import CalculationFailedSchema
from coordinate_calculator.errors.schemas.invalid_request import InvalidRequestSchema
from coordinate_calculator.errors.schemas.not_found import NotFoundSchema
from coordinate_calculator.errors.schemas.not_implemented import NotImplementedErrorSchema

__all__ = [
    "AlreadyExistsSchema",
    "CalculationFailedSchema",
    "InvalidRequestSchema",
    "NotFoundSchema",
    "NotImplementedErrorSchema",
]
