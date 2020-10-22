"""
foo bar baz
"""
import logging
import os
import sys
from typing import Any, cast

_LOGGER_INITIALIZED = False
TRACE_LOG_LEVEL = 5


class Logger(logging.Logger):
    def trace(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...  # pragma: no cover


def get_logger(name: str) -> Logger:
    """
    foo bar baz
    """
    global _LOGGER_INITIALIZED

    if not _LOGGER_INITIALIZED:
        _LOGGER_INITIALIZED = True
        logging.addLevelName(TRACE_LOG_LEVEL, "TRACE")
        log_level = os.environ.get("SNADRA_LOG_LEVEL", "").upper()

        if log_level in {"DEBUG", "TRACE"}:
            logger = logging.getLogger("snadra")
            logger.setLevel(logging.DEBUG if log_level == "DEBUG" else TRACE_LOG_LEVEL)
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            logger.addHandler(handler)

    logger = logging.getLogger(name)

    def trace(self, message: str, *args: Any, **kwargs: Any) -> None:
        logger.log(TRACE_LOG_LEVEL, message, *args, **kwargs)

    logger.trace = trace  # type: ignore
    return cast(Logger, logger)
