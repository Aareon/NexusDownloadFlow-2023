"""Centralized logging configuration for NexusDownloadFlow."""

import sys

from loguru import logger


def configure_logging(level: str = "INFO") -> None:
    """Configure loguru to log cleanly to stdout for CLI and EXE use.

    Args:
        level: Log level name such as INFO, DEBUG, or WARNING.
    """
    logger.remove()
    logger.add(
        sys.stdout,
        level=level,
        format="<level>{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}</level>",
        colorize=False,
    )
