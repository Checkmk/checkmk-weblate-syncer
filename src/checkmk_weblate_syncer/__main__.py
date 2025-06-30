import sys
from pathlib import Path
from typing import assert_never

from .cli import Mode, parse_arguments
from .config import UpdateSourcesConfig, UpdateTranslationsConfig
from .logger import LOGGER, configure_logger
from .update_sources import run as run_update_sources
from .update_translations import run as run_update_translations


def main() -> int:
    args = parse_arguments()
    configure_logger(args.log_level)

    match args.mode:
        case Mode.UPDATE_SOURCES:
            return run_update_sources(
                _load_config(args.config_path, UpdateSourcesConfig)
            )
        case Mode.UPDATE_TRANSLATIONS:
            return run_update_translations(
                _load_config(args.config_path, UpdateTranslationsConfig)
            )
        case _:
            assert_never(args.mode)


if __name__ == "__main__":
    sys.exit(main())


def _load_config[T: (UpdateSourcesConfig, UpdateTranslationsConfig)](
    config_path: Path, config_type: type[T]
) -> T:
    try:
        return config_type.model_validate_json(config_path.read_text())
    except Exception:
        LOGGER.error("Loading config failed")
        raise
