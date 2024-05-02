from pathlib import Path
from typing import TypeVar

from .cli import Mode, parse_arguments
from .config import PotModeConfig
from .logging import LOGGER, configure_logger
from .pot import run as run_pot_mode


def _main() -> None:
    args = parse_arguments()
    configure_logger(args.log_path, args.log_level)

    match args.mode:
        case Mode.POT:
            run_pot_mode(_load_config(args.config_path, PotModeConfig))
        # TODO (apparently does not work with enums with only one variant):  # pylint: disable=fixme
        # case _:
        #     assert_never(args.mode)


# TODO:  # pylint: disable=fixme
# _ConfigTypeT = TypeVar("_ConfigTypeT", PotModeConfig, PoModeConfig)
# apparently, type vars cannot have a single constraint, so we have to use bound for now
_ConfigTypeT = TypeVar("_ConfigTypeT", bound=PotModeConfig)


def _load_config(config_path: Path, config_type: type[_ConfigTypeT]) -> _ConfigTypeT:
    try:
        return config_type.model_validate_json(config_path.read_text())
    except Exception as e:
        LOGGER.error("Loading config failed")
        LOGGER.exception(e)
        raise e


_main()
