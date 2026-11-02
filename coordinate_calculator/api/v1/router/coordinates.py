# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import Annotated

from fastapi import APIRouter, Depends

from coordinate_calculator.errors.registration import get_error_responses
from coordinate_calculator.errors.schemas import AlreadyExistsSchema, CalculationFailedSchema, InvalidRequestSchema
from coordinate_calculator.schemas.v1.coordinates import (
    CalculateCoordinatesRequestV1,
    CoordinatePointV1,
    CoordinatesResponseV1,
)
from coordinate_calculator.services.coordinates import CoordinateService

router = APIRouter(
    prefix="/coordinates",
    tags=["Coordinates"],
    responses=get_error_responses(
        include={AlreadyExistsSchema, CalculationFailedSchema, InvalidRequestSchema},
    ),
)


@router.post("/", summary="Calculate spacecraft coordinates")
async def calculate_coordinates(
    body: CalculateCoordinatesRequestV1,
    service: Annotated[CoordinateService, Depends()],
) -> CoordinatesResponseV1:
    points = await service.calculate(body)
    return CoordinatesResponseV1(points=[CoordinatePointV1.model_validate(point) for point in points])
