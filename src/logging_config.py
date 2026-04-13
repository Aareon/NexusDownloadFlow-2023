"""Centralized logging configuration for NexusDownloadFlow."""

import sys
from pathlib import Path

from loguru import logger


def configure_logging(level: str = "INFO", log_file_path: Path | None = None) -> None:
    """Configure loguru to log cleanly to stdout for CLI and EXE use.

    Args:
        level: Log level name such as INFO, DEBUG, or WARNING.
        log_file_path: Optional file path for persistent log output.
    """
    logger.remove()
    logger.add(
        sys.stdout,
        level=level,
        format="<level>{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}</level>",
        colorize=False,
    )

    if log_file_path is not None:
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(log_file_path),
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            rotation="5 MB",
            retention="10 days",
            encoding="utf-8",
        )
