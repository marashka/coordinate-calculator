# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from datetime import date

import factory
from pytest_factoryboy import register

from coordinate_calculator.db.models import Spacecraft


class SpacecraftFactory(factory.Factory):
    class Meta:
        model = Spacecraft

    name = "ISS (ZARYA)"
    norad_id = factory.Sequence(lambda number: 25_544 + number)
    international_designator = factory.Sequence(lambda number: f"1998-{number:03d}A")
    launch_date = date(1998, 11, 20)


register(SpacecraftFactory)
