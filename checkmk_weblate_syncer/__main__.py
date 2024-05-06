import sys
from pathlib import Path
from typing import TypeVar

from .cli import Mode, parse_arguments
from .config import PoModeConfig, PotModeConfig
from .logging import LOGGER, configure_logger
from .po import run as run_po_mode
from .pot import run as run_pot_mode


def _main() -> None:
    args = parse_arguments()
    configure_logger(args.log_path, args.log_level)

    match args.mode:
        case Mode.POT:
            sys.exit(run_pot_mode(_load_config(args.config_path, PotModeConfig)))
        case Mode.PO:
            sys.exit(run_po_mode(_load_config(args.config_path, PoModeConfig)))


_ConfigTypeT = TypeVar("_ConfigTypeT", PotModeConfig, PoModeConfig)


def _load_config(config_path: Path, config_type: type[_ConfigTypeT]) -> _ConfigTypeT:
    try:
        return config_type.model_validate_json(config_path.read_text())
    except Exception as e:
        LOGGER.error("Loading config failed")
        LOGGER.exception(e)
        raise e


_main()
