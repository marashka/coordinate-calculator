# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from sgp4 import omm
from sgp4.api import Satrec
from sgp4.exporter import export_omm
from skyfield.api import EarthSatellite, load, wgs84

from coordinate_calculator.exceptions import CalculationError

if TYPE_CHECKING:
    from coordinate_calculator.schemas.v1.coordinates import OrbitElementsV1, TleElementsV1

_TIMESCALE = load.timescale()


@dataclass(frozen=True, slots=True)
class SpacecraftPassport:
    name: str
    norad_id: int
    international_designator: str


@dataclass(frozen=True, slots=True)
class CoordinatePoint:
    time: datetime
    latitude_deg: float
    longitude_deg: float
    altitude_km: float


def load_tle(elements: TleElementsV1) -> tuple[Satrec, SpacecraftPassport]:
    try:
        satellite = Satrec.twoline2rv(elements.line1, elements.line2)
    except ValueError as exc:
        raise CalculationError(str(exc)) from exc
    return satellite, SpacecraftPassport(
        name=elements.name,
        norad_id=int(satellite.satnum),
        international_designator=export_omm(satellite, elements.name)["OBJECT_ID"],
    )


def load_orbit(elements: OrbitElementsV1) -> tuple[Satrec, SpacecraftPassport]:
    satellite = Satrec()
    try:
        omm.initialize(satellite, elements.model_dump(by_alias=True, exclude={"source"}))
    except (KeyError, ValueError) as exc:
        raise CalculationError(str(exc)) from exc
    return satellite, SpacecraftPassport(
        name=elements.object_name,
        norad_id=elements.norad_cat_id,
        international_designator=export_omm(satellite, elements.object_name)["OBJECT_ID"],
    )


def propagate(
    satellite: Satrec,
    start: datetime,
    end: datetime,
    step_seconds: int,
) -> list[CoordinatePoint]:
    viewed = EarthSatellite.from_satrec(satellite, _TIMESCALE)
    moments = _moments(start, end, step_seconds)
    position = viewed.at(_TIMESCALE.from_datetimes(moments))
    _raise_if_propagation_failed(moments, position.message)
    geographic = wgs84.geographic_position_of(position)
    latitudes = geographic.latitude.degrees
    longitudes = geographic.longitude.degrees
    altitudes = geographic.elevation.km
    return [
        CoordinatePoint(
            time=moment,
            latitude_deg=float(latitudes[index]),
            longitude_deg=float(longitudes[index]),
            altitude_km=float(altitudes[index]),
        )
        for index, moment in enumerate(moments)
    ]


def _moments(start: datetime, end: datetime, step_seconds: int) -> list[datetime]:
    step = timedelta(seconds=step_seconds)
    moment = start.astimezone(UTC)
    finish = end.astimezone(UTC)
    moments: list[datetime] = []
    while moment <= finish:
        moments.append(moment)
        moment += step
    return moments


def _raise_if_propagation_failed(moments: list[datetime], messages: object) -> None:
    if isinstance(messages, str):
        message = f"SGP4 failed at {moments[0].isoformat()}: {messages}"
        raise CalculationError(message)
    if not isinstance(messages, list):
        return
    for moment, detail in zip(moments, messages, strict=True):
        if detail:
            message = f"SGP4 failed at {moment.isoformat()}: {detail}"
            raise CalculationError(message)
