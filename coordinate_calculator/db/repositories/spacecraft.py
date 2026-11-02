# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import NoReturn

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError

from coordinate_calculator.db.models import Spacecraft
from coordinate_calculator.db.repositories.base import Repository
from coordinate_calculator.exceptions import EntityAlreadyExistsError


class SpacecraftRepository(Repository[Spacecraft]):
    async def get_by_norad_id(self, norad_id: int) -> Spacecraft | None:
        query = select(Spacecraft).where(Spacecraft.norad_id == norad_id)
        return await self._session.scalar(query)

    def _raise_error(self, err: DBAPIError, obj: Spacecraft) -> NoReturn:
        constraint = _constraint_name(err)
        if constraint == "uq__spacecraft__norad_id":
            raise EntityAlreadyExistsError(Spacecraft.__name__, "norad_id", obj.norad_id) from err
        if constraint == "uq__spacecraft__international_designator":
            raise EntityAlreadyExistsError(
                Spacecraft.__name__,
                "international_designator",
                obj.international_designator,
            ) from err
        super()._raise_error(err, obj)


def _constraint_name(err: DBAPIError) -> str | None:
    nested = getattr(getattr(err, "__cause__", None), "__cause__", None)
    for candidate in (getattr(err, "orig", None), nested):
        name = getattr(candidate, "constraint_name", None)
        if isinstance(name, str):
            return name
    return None
