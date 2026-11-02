# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import TYPE_CHECKING

from factory.alchemy import SQLAlchemyModelFactory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class _Session:
    current: AsyncSession | None = None


def bind_session(session: AsyncSession | None) -> None:
    _Session.current = session


def _session_factory() -> AsyncSession:
    if _Session.current is None:
        message = "No session provided."
        raise RuntimeError(message)
    return _Session.current


class DatabaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_factory = _session_factory
