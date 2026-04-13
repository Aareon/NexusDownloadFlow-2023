"""Centralized logging configuration for NexusDownloadFlow-2026."""

import sys

from loguru import logger


def configure_logging() -> None:
    """Configure loguru to log cleanly to stdout for CLI and EXE use."""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<level>{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}</level>",
        colorize=False,
    )
