# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from datetime import date
from typing import Annotated

from fastapi import Depends

from coordinate_calculator.schemas.v1 import CalculateCoordinatesRequestV1, TleElementsV1
from coordinate_calculator.services.propagation import CoordinatePoint, load_orbit, load_tle, propagate
from coordinate_calculator.services.uow import UnitOfWork


class CoordinateService:
    def __init__(self, uow: Annotated[UnitOfWork, Depends()]):
        self._uow = uow

    async def calculate(self, request: CalculateCoordinatesRequestV1) -> list[CoordinatePoint]:
        if isinstance(request.elements, TleElementsV1):
            satellite, passport = load_tle(request.elements)
        else:
            satellite, passport = load_orbit(request.elements)
        points = propagate(satellite, request.start, request.end, request.step_seconds)
        async with self._uow:
            await self._save_passport(
                name=passport.name,
                norad_id=passport.norad_id,
                international_designator=passport.international_designator,
                launch_date=request.launch_date,
            )
        return points

    async def _save_passport(
        self,
        *,
        name: str,
        norad_id: int,
        international_designator: str,
        launch_date: date,
    ) -> None:
        existing = await self._uow.spacecraft.get_by_norad_id(norad_id)
        if existing is None:
            await self._uow.spacecraft.create(
                name=name,
                norad_id=norad_id,
                international_designator=international_designator,
                launch_date=launch_date,
            )
            return
        await self._uow.spacecraft.update(
            existing.id,
            name=name,
            international_designator=international_designator,
            launch_date=launch_date,
        )
