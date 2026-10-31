# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from pydantic import BaseModel


class ServerSettings(BaseModel):
    """Backend server settings."""
