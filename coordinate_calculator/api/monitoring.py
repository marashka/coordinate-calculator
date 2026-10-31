# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from fastapi import APIRouter

from coordinate_calculator.schemas import PingResponse

router = APIRouter(tags=["Monitoring"], prefix="/monitoring")


@router.get("/ping", summary="Check if server is alive")
async def ping() -> PingResponse:
    return PingResponse()
