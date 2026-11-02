# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from fastapi import APIRouter

from coordinate_calculator.api.monitoring import router as monitoring_router
from coordinate_calculator.api.v1.router import router as v1_router

api_router = APIRouter()
api_router.include_router(monitoring_router)
api_router.include_router(v1_router)
