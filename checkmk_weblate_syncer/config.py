from collections.abc import Sequence
from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, BaseModel


def _validate_path_is_absolute(path: Path) -> Path:
    assert path.is_absolute(), f"{path} is not absolute"
    return path


def _validate_path_is_relative(path: Path) -> Path:
    assert not path.is_absolute(), f"{path} is absolute but should be relative"
    return path


class RepositoryConfig(BaseModel, frozen=True):
    path: Annotated[Path, AfterValidator(_validate_path_is_absolute)]
    branch: str


class BaseConfig(BaseModel, frozen=True):
    checkmk_repository: RepositoryConfig
    locale_repository: RepositoryConfig


class PotModeConfig(BaseConfig, frozen=True):
    checkmk_pot_generation_script: Annotated[
        Path, AfterValidator(_validate_path_is_relative)
    ]
    locale_pot_path: Annotated[Path, AfterValidator(_validate_path_is_relative)]


class PoFilePair(BaseModel, frozen=True):
    checkmk: Annotated[Path, AfterValidator(_validate_path_is_relative)]
    locale: Annotated[Path, AfterValidator(_validate_path_is_relative)]


class PoModeConfig(BaseConfig, frozen=True):
    po_file_pairs: Sequence[PoFilePair]
