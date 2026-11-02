# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import os
from textwrap import dedent
from typing import TYPE_CHECKING

from coordinate_calculator.settings.application import ApplicationSettings

if TYPE_CHECKING:
    import pytest


def _clear_settings_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for variable_name in tuple(os.environ):
        if variable_name.startswith("COORDINATE_CALCULATOR__"):
            monkeypatch.delenv(variable_name)
    monkeypatch.delenv("COORDINATE_CALCULATOR_CONFIG_FILE", raising=False)


def test_application_settings_are_loaded_from_default_yaml_file(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_settings_environment(monkeypatch)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config.yml").write_text(
        dedent(
            """\
            database:
              url: postgresql+asyncpg://yaml:yaml@localhost:5432/coordinate_calculator
            """,
        ),
        encoding="utf-8",
    )

    settings = ApplicationSettings()

    assert str(settings.database.url) == "postgresql+asyncpg://yaml:yaml@localhost:5432/coordinate_calculator"


def test_yaml_file_overrides_environment(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_settings_environment(monkeypatch)
    config_path = tmp_path / "custom.yml"
    config_path.write_text(
        dedent(
            """\
            database:
              url: postgresql+asyncpg://yaml:yaml@localhost:5432/coordinate_calculator
            """,
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("COORDINATE_CALCULATOR_CONFIG_FILE", str(config_path))
    monkeypatch.setenv(
        "COORDINATE_CALCULATOR__DATABASE__URL",
        "postgresql+asyncpg://env:env@localhost:5432/coordinate_calculator",
    )

    settings = ApplicationSettings()

    assert str(settings.database.url) == "postgresql+asyncpg://yaml:yaml@localhost:5432/coordinate_calculator"


def test_settings_can_be_loaded_from_environment_without_yaml_file(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_settings_environment(monkeypatch)
    monkeypatch.setenv("COORDINATE_CALCULATOR_CONFIG_FILE", str(tmp_path / "missing.yml"))
    monkeypatch.setenv(
        "COORDINATE_CALCULATOR__DATABASE__URL",
        "postgresql+asyncpg://env:env@localhost:5432/coordinate_calculator",
    )

    settings = ApplicationSettings()

    assert str(settings.database.url) == "postgresql+asyncpg://env:env@localhost:5432/coordinate_calculator"
