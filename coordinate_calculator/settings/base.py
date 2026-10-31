# SPDX-FileCopyrightText: 2026-present Marat Akhmetov
# SPDX-License-Identifier: MIT
import os
from typing import ClassVar

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import (
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class BaseSettings(PydanticBaseSettings):
    """Settings loaded from a YAML file and from the environment."""

    DEFAULT_CONFIG_FILE: ClassVar[str] = "config.yml"

    model_config = SettingsConfigDict(
        env_prefix="COORDINATE_CALCULATOR__",
        env_nested_delimiter="__",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[PydanticBaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        yaml_file_path = os.getenv("COORDINATE_CALCULATOR_CONFIG_FILE", cls.DEFAULT_CONFIG_FILE)
        yaml_settings = YamlConfigSettingsSource(
            settings_cls,
            yaml_file=yaml_file_path,
            yaml_file_encoding="utf-8",
        )
        return (
            init_settings,
            yaml_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
