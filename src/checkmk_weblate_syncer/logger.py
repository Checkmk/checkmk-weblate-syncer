import logging

LOGGER = logging.getLogger()


def configure_logger(level: int) -> None:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s",
    )
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)
