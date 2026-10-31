# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import generic_repr

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()],
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s"),
    "pk": "pk__%(table_name)s",
}

backend_metadata = MetaData(naming_convention=convention)  # type: ignore[arg-type]


@generic_repr
class Base(DeclarativeBase):
    metadata = backend_metadata
