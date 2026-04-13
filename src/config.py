"""Configuration loading and management for NexusDownloadFlow-2026."""

from pathlib import Path

import toml
from loguru import logger


def load_config(config_path: Path, default_config: str) -> dict:
    """Load configuration from file or create default if missing.

    Args:
        config_path: Path to the config file to load.
        default_config: Default TOML config as string to use as fallback.

    Returns:
        Parsed configuration dictionary.

    """
    if not config_path.exists():
        logger.warning("Config not found, creating {}", config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(config_path, "w") as f:
                f.write(default_config)
                f.flush()
        except Exception as e:
            logger.exception("Error saving default config file: {}", e)
        return toml.loads(default_config)
    else:
        try:
            return toml.load(config_path)
        except Exception as e:
            logger.exception("Error reading config file ({}). Using default configuration.", e)
            return toml.loads(default_config)
