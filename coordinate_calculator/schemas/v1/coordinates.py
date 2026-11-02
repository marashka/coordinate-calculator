# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from datetime import UTC, date, datetime
from typing import Final, Literal, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_serializer, field_validator, model_validator
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv, verify_checksum

MAX_COORDINATE_POINTS: Final[int] = 86_400


class TleElementsV1(BaseModel):
    source: Literal["tle"] = Field(description="Two-line element set")
    name: str = Field(min_length=1, max_length=128, description="Spacecraft name")
    line1: str = Field(min_length=69, max_length=69, description="First line of the two-line element set")
    line2: str = Field(min_length=69, max_length=69, description="Second line of the two-line element set")

    @field_validator("name", "line1", "line2", mode="before")
    @classmethod
    def strip_text(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @model_validator(mode="after")
    def check_tle(self) -> Self:
        try:
            twoline2rv(self.line1, self.line2, wgs72)
            verify_checksum(self.line1, self.line2)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        return self


class OrbitElementsV1(BaseModel):
    source: Literal["orbit"] = Field(description="Celestrak OMM JSON object")
    object_name: str = Field(
        alias="OBJECT_NAME",
        min_length=1,
        max_length=128,
        description="Spacecraft name",
    )
    object_id: str = Field(
        alias="OBJECT_ID",
        pattern=r"^\d{4}-\d{3}[A-Z]{1,3}$",
        description="International designator, for example 1998-067A",
    )
    norad_cat_id: int = Field(alias="NORAD_CAT_ID", gt=0, description="NORAD catalog id")
    epoch: datetime = Field(alias="EPOCH", description="Epoch of the element set, UTC")
    mean_motion: float = Field(alias="MEAN_MOTION", gt=0, description="Revolutions per day")
    eccentricity: float = Field(alias="ECCENTRICITY", ge=0, lt=1)
    inclination: float = Field(alias="INCLINATION", ge=0, le=180, description="Degrees")
    ra_of_asc_node: float = Field(alias="RA_OF_ASC_NODE", ge=0, lt=360, description="Degrees")
    arg_of_pericenter: float = Field(alias="ARG_OF_PERICENTER", ge=0, lt=360, description="Degrees")
    mean_anomaly: float = Field(alias="MEAN_ANOMALY", ge=0, lt=360, description="Degrees")
    bstar: float = Field(alias="BSTAR", default=0, description="Drag term, 1/Earth radii")
    mean_motion_dot: float = Field(
        alias="MEAN_MOTION_DOT",
        default=0,
        description="First derivative, revolutions per day squared",
    )
    mean_motion_ddot: float = Field(
        alias="MEAN_MOTION_DDOT",
        default=0,
        description="Second derivative, revolutions/day^3",
    )
    classification_type: str = Field(alias="CLASSIFICATION_TYPE", default="U", min_length=1, max_length=1)
    ephemeris_type: int = Field(alias="EPHEMERIS_TYPE", default=0)
    element_set_no: int = Field(alias="ELEMENT_SET_NO", default=0, ge=0)
    rev_at_epoch: int = Field(alias="REV_AT_EPOCH", default=0, ge=0)

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("epoch")
    @classmethod
    def epoch_as_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    @field_serializer("epoch")
    def epoch_for_omm(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%dT%H:%M:%S.%f")


class CalculateCoordinatesRequestV1(BaseModel):
    launch_date: date = Field(description="Launch date stored with the spacecraft passport")
    start: AwareDatetime = Field(description="First moment of the interval, inclusive")
    end: AwareDatetime = Field(description="Last moment of the interval, inclusive")
    step_seconds: int = Field(ge=1, le=60, description="Sampling step in seconds")
    elements: TleElementsV1 | OrbitElementsV1 = Field(
        discriminator="source",
        description="Orbital element set",
    )

    @model_validator(mode="after")
    def check_interval(self) -> Self:
        if self.end < self.start:
            message = "end must be greater than or equal to start"
            raise ValueError(message)
        point_count = int((self.end - self.start).total_seconds() // self.step_seconds) + 1
        if point_count > MAX_COORDINATE_POINTS:
            message = f"Interval produces {point_count} points; the limit is {MAX_COORDINATE_POINTS}"
            raise ValueError(message)
        return self


class CoordinatePointV1(BaseModel):
    time: datetime = Field(description="UTC time of the point")
    latitude_deg: float = Field(description="WGS84 geodetic latitude, degrees")
    longitude_deg: float = Field(description="WGS84 geodetic longitude, degrees")
    altitude_km: float = Field(description="WGS84 altitude above the ellipsoid, kilometers")

    model_config = ConfigDict(from_attributes=True)


class CoordinatesResponseV1(BaseModel):
    points: list[CoordinatePointV1]
