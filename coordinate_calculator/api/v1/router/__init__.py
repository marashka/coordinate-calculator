# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from fastapi import APIRouter

from coordinate_calculator.api.v1.router.coordinates import router as coordinates_router

router = APIRouter(prefix="/v1")
router.include_router(coordinates_router)
