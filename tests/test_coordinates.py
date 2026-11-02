# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import json
from datetime import UTC, date, datetime
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from sqlalchemy import select

from coordinate_calculator.db.models import Spacecraft

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from sqlalchemy.ext.asyncio import AsyncSession

    from tests.factories.spacecraft import SpacecraftFactory

pytestmark = pytest.mark.db

DATA = Path(__file__).parent / "data"


@pytest.fixture
def bulletin() -> dict[str, object]:
    payload = json.loads((DATA / "iss_25544.json").read_text(encoding="utf-8"))
    return payload[0]


@pytest.fixture
def schedule(bulletin: dict[str, object]) -> dict[str, object]:
    epoch = datetime.fromisoformat(str(bulletin["EPOCH"])).replace(tzinfo=UTC).isoformat()
    return {
        "launch_date": "1998-11-20",
        "start": epoch,
        "end": epoch,
        "step_seconds": 60,
    }


async def test_tle_request_succeeds(
    client: TestClient,
    bulletin: dict[str, object],
    schedule: dict[str, object],
    db_session: AsyncSession,
) -> None:
    name, line1, line2 = (DATA / "iss_25544.tle").read_text(encoding="utf-8").splitlines()
    response = client.post(
        "/v1/coordinates/",
        json={
            **schedule,
            "elements": {
                "source": "tle",
                "name": name,
                "line1": line1,
                "line2": line2,
            },
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "points": [
            {
                "time": "2026-11-01T12:44:51.278784Z",
                "latitude_deg": -0.00006295476364692119,
                "longitude_deg": 108.40953346249096,
                "altitude_km": 415.5860287472115,
            },
        ],
    }
    stored = await db_session.scalar(select(Spacecraft).where(Spacecraft.norad_id == bulletin["NORAD_CAT_ID"]))
    assert stored is not None
    assert stored.name == bulletin["OBJECT_NAME"]
    assert stored.norad_id == bulletin["NORAD_CAT_ID"]
    assert stored.international_designator == bulletin["OBJECT_ID"]
    assert stored.launch_date == date(1998, 11, 20)


async def test_orbit_request_succeeds(
    client: TestClient,
    bulletin: dict[str, object],
    schedule: dict[str, object],
    db_session: AsyncSession,
) -> None:
    response = client.post(
        "/v1/coordinates/",
        json={
            **schedule,
            "elements": {**bulletin, "source": "orbit"},
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "points": [
            {
                "time": "2026-11-01T12:44:51.278784Z",
                "latitude_deg": -0.00006293755489907418,
                "longitude_deg": 108.4095334760189,
                "altitude_km": 415.5860287457325,
            },
        ],
    }
    stored = await db_session.scalar(select(Spacecraft).where(Spacecraft.norad_id == bulletin["NORAD_CAT_ID"]))
    assert stored is not None
    assert stored.name == bulletin["OBJECT_NAME"]
    assert stored.norad_id == bulletin["NORAD_CAT_ID"]
    assert stored.international_designator == bulletin["OBJECT_ID"]
    assert stored.launch_date == date(1998, 11, 20)


async def test_orbit_request_conflicts_when_designator_belongs_to_another_norad(
    client: TestClient,
    bulletin: dict[str, object],
    schedule: dict[str, object],
    db_session: AsyncSession,
    spacecraft_factory: type[SpacecraftFactory],
) -> None:
    occupant = spacecraft_factory(norad_id=99_901)
    request_norad = occupant.norad_id + 1
    db_session.add(occupant)
    await db_session.commit()

    response = client.post(
        "/v1/coordinates/",
        json={
            **schedule,
            "elements": {
                **bulletin,
                "source": "orbit",
                "OBJECT_ID": occupant.international_designator,
                "NORAD_CAT_ID": request_norad,
            },
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "error": {
            "code": "conflict",
            "message": "Spacecraft already exists",
            "details": {
                "entity_type": "Spacecraft",
                "field": "international_designator",
                "value": occupant.international_designator,
            },
        },
    }
