from argparse import ArgumentParser
from enum import Enum
from logging import DEBUG, INFO, WARNING
from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field


class Mode(Enum):
    UPDATE_SOURCES = "update-sources"
    UPDATE_TRANSLATIONS = "update-translations"


def _parse_log_level(raw: int) -> int:
    if raw <= 0:
        return WARNING
    if raw == 1:
        return INFO
    return DEBUG


class Arguments(BaseModel, frozen=True):
    mode: Mode
    config_path: Path
    log_level: Annotated[int, AfterValidator(_parse_log_level)] = Field(alias="verbose")


def parse_arguments() -> Arguments:
    parser = ArgumentParser()
    parser.add_argument(
        "mode",
        type=str,
        choices=[mode.value for mode in Mode],
        metavar="MODE",
        help="Operation mode. update-sources: Update source strings (.pot file). "
        "update-translations: Update translations (.po files).",
    )
    parser.add_argument(
        "config_path",
        type=Path,
        metavar="CONFIG_PATH",
        help="Configuration file path.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase logging verbosity. The default log level is WARNING. "
        "Use -v for INFO and -vv for DEBUG.",
    )
    return Arguments.model_validate(vars(parser.parse_args()))
