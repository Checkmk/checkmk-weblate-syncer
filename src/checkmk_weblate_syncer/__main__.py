import sys
from pathlib import Path
from typing import TypeVar, assert_never

from .cli import Mode, parse_arguments
from .config import UpdateSourcesConfig, UpdateTranslationsConfig
from .logging import LOGGER, configure_logger
from .update_sources import run as run_update_sources
from .update_translations import run as run_update_translations


def _main() -> None:
    args = parse_arguments()
    configure_logger(args.log_level)

    match args.mode:
        case Mode.UPDATE_SOURCES:
            sys.exit(
                run_update_sources(_load_config(args.config_path, UpdateSourcesConfig))
            )
        case Mode.UPDATE_TRANSLATIONS:
            sys.exit(
                run_update_translations(
                    _load_config(args.config_path, UpdateTranslationsConfig)
                )
            )
        case _:
            assert_never(args.mode)


_ConfigTypeT = TypeVar("_ConfigTypeT", UpdateSourcesConfig, UpdateTranslationsConfig)


def _load_config(config_path: Path, config_type: type[_ConfigTypeT]) -> _ConfigTypeT:
    try:
        return config_type.model_validate_json(config_path.read_text())
    except Exception as e:
        LOGGER.error("Loading config failed")
        raise e


_main()
