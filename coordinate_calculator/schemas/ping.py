# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import Literal

from pydantic import BaseModel


class PingResponse(BaseModel):
    """Ping result"""

    status: Literal["ok"] = "ok"
