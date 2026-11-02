# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
from typing import TYPE_CHECKING

from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from sqlalchemy import engine_from_config, pool

if TYPE_CHECKING:
    from alembic.config import Config as AlembicConfig
    from sqlalchemy import MetaData


def do_run_migrations(
    config: AlembicConfig,
    target_metadata: MetaData,
    revision: str,
    action: str = "up",
) -> None:
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs(revision, rev)  # noqa: SLF001

    def downgrade(rev, context):
        return script._downgrade_revs(revision, rev)  # noqa: SLF001

    with EnvironmentContext(
        config,
        script=script,
        fn=upgrade if action == "up" else downgrade,
        as_sql=False,
        starting_rev=None,
        destination_rev=revision,
    ) as context:
        engine = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()

        engine.dispose()
