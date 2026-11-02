# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from collections.abc import AsyncGenerator
from types import TracebackType
from typing import Annotated, Self

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import HTTPConnection

from coordinate_calculator.db.repositories.spacecraft import SpacecraftRepository


async def get_session(connection: HTTPConnection) -> AsyncGenerator[AsyncSession]:
    async with connection.app.state.session_factory() as session:
        yield session


class UnitOfWork:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
    ):
        self._session = session
        self.spacecraft = SpacecraftRepository(session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
