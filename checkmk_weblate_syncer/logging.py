import logging
from pathlib import Path

LOGGER = logging.getLogger()


def configure_logger(path: Path | None, level: int) -> None:
    if path:
        handler: logging.Handler = logging.FileHandler(path, encoding="UTF-8")
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)
