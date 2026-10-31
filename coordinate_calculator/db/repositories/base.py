# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from collections.abc import Sequence
from typing import Any, NoReturn, TypeVar
from uuid import UUID

from sqlalchemy import (
    ScalarResult,
    Select,
    delete,
    func,
    select,
)
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.sql.selectable import ForUpdateArg

from coordinate_calculator.db.models import Base
from coordinate_calculator.db.utils.pagination import Pagination
from coordinate_calculator.exceptions import EntityNotFoundError

Model = TypeVar("Model", bound=Base)


class Repository[Model]:
    def __init__(self, session: AsyncSession):
        self._model = self.__class__.__orig_bases__[0].__args__[0]  # type: ignore[attr-defined]
        self._session = session

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}()"

    async def get_by_id(self, id: UUID) -> Model:
        obj = await self._session.get(self._model, id)
        if obj is None:
            raise EntityNotFoundError(self._model.__name__, "id", id)
        return obj

    async def create(self, **kwargs: Any) -> Model:
        obj = self._model(**kwargs)
        try:
            self._session.add(obj)
            await self._session.flush()
        except IntegrityError as e:
            self._raise_error(e, obj)
        return await self.get_by_id(obj.id)

    async def update(self, id: UUID, **kwargs: Any) -> Model:
        obj = await self.get_by_id(id)
        for key, value in kwargs.items():
            setattr(obj, key, value)

        try:
            await self._session.flush()
        except IntegrityError as e:
            self._raise_error(e, obj)
        return await self.get_by_id(id)

    async def delete(self, id: UUID) -> None:
        result = await self._session.execute(delete(self._model).filter_by(id=id))
        await self._session.flush()
        if result.rowcount == 0:  # type: ignore[attr-defined]
            raise EntityNotFoundError(self._model.__name__, "id", id)

    async def lock_for_update(self, id: UUID) -> Model:
        obj = await self._session.get(self._model, id, with_for_update=ForUpdateArg(key_share=True))
        if obj is None:
            raise EntityNotFoundError(self._model.__name__, "id", id)
        return obj

    async def _paginate_scalar_query(
        self,
        query: Select,
        page: int,
        page_size: int,
        options: Sequence[ExecutableOption] | None = None,
    ) -> Pagination[Model]:
        items_query = query.limit(page_size).offset((page - 1) * page_size)
        if options:
            items_query = items_query.options(*options)

        total_query = select(func.count()).select_from(query.subquery())
        items_result: ScalarResult[Model] = await self._session.scalars(items_query)

        total_count: int = await self._session.scalar(total_query)  # type: ignore[assignment]
        return Pagination(
            items=list(items_result.all()),
            total_count=total_count,
            page=page,
            page_size=page_size,
        )

    def _raise_error(self, err: DBAPIError, obj: Model) -> NoReturn:
        raise err
