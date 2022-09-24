from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Type, TypedDict, cast

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


__all__ = (
    "AnmitsuAutomationConfig",
    "AnmitsuAuthConfig",
    "AnmitsuDatabaseConfig",
    "AnmitsuConfig",
)


# TODO
class AzukiManga:
    pass


class _AnmitsuAutomateConfigOptionalType(TypedDict, total=False):
    startFrom: Optional[int]
    includeChapterName: Optional[bool]
    autoUpload: Optional[bool]
    nyaaDescription: Optional[str]


class _AnmitsuAutomateConfigType(_AnmitsuAutomateConfigOptionalType):
    slug: str
    title: str
    outputFormat: str


class _AnmitsuAuthConfigType(TypedDict):
    username: str
    password: str


class _AnmitsuDBConfigType(TypedDict):
    path: str


class _AnmitsuConfigOptionalType(TypedDict, total=False):
    db: Optional[_AnmitsuDBConfigType]


class _AnmitsuConfigType(_AnmitsuConfigOptionalType):
    automate: List[_AnmitsuAutomateConfigType]
    nyaaInfo: _AnmitsuAuthConfigType
    azukiAuth: _AnmitsuAuthConfigType


@dataclass
class AnmitsuAutomationConfig:
    slug: str
    title: str
    output_format: str
    start_from: Optional[int] = None
    include_chapter_name: bool = False
    auto_upload: bool = False
    nyaa_description: Optional[str] = None

    @classmethod
    def from_yaml(cls: Type[AnmitsuAutomationConfig], configuration: _AnmitsuAutomateConfigType):
        clean_str = lambda x: x.strip() if isinstance(x, str) else x  # noqa: E731
        return cls(
            slug=configuration["slug"],
            title=clean_str(configuration["title"]),
            output_format=clean_str(configuration["outputFormat"]),
            start_from=configuration.get("startFrom"),
            include_chapter_name=configuration.get("includeChapterName", False),
            auto_upload=configuration.get("autoUpload", False),
            nyaa_description=clean_str(configuration.get("nyaaDescription")),
        )


@dataclass
class AnmitsuAuthConfig:
    username: str
    password: str

    @classmethod
    def from_yaml(cls: Type[AnmitsuAuthConfig], configuration: _AnmitsuAuthConfigType):
        return cls(username=configuration["username"], password=configuration["password"])


@dataclass
class AnmitsuDatabaseConfig:
    path: str

    @classmethod
    def from_yaml(cls: Type[AnmitsuDatabaseConfig], db_path: Optional[str] = None):
        # TODO: Fallback to user path
        return cls(path=db_path or "anmitsu.db")


@dataclass
class AnmitsuConfig:
    automate: List[AnmitsuAutomationConfig]
    nyaa_auth: AnmitsuAuthConfig
    azuki_auth: AnmitsuAuthConfig
    db: AnmitsuDatabaseConfig

    @classmethod
    def from_yaml(cls: Type[AnmitsuConfig], configuration: _AnmitsuConfigType):
        db_conf = AnmitsuDatabaseConfig.from_yaml(configuration.get("db", {}).get("path"))
        return cls(
            automate=[AnmitsuAutomationConfig.from_yaml(conf) for conf in configuration["automate"]],
            nyaa_auth=AnmitsuAuthConfig.from_yaml(configuration["nyaaInfo"]),
            azuki_auth=AnmitsuAuthConfig.from_yaml(configuration["azukiAuth"]),
            db=db_conf,
        )

    @classmethod
    def from_string(cls: Type[AnmitsuConfig], configuration: str):
        data = cast(_AnmitsuConfigType, load(configuration, Loader=Loader))
        return cls.from_yaml(data)


if __name__ == "__main__":
    from pathlib import Path

    config = Path(__file__).absolute().parent.parent / "config.yml"
    config_str = config.read_text()
    print(AnmitsuConfig.from_string(config_str))
