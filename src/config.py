"""Configuration loading and management for NexusDownloadFlow."""

from pathlib import Path

import toml
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class AppConfig(BaseModel):
    """Validated application configuration."""

    model_config = ConfigDict(extra="ignore")

    check_delay: float = Field(default=5.0, ge=0.1)
    verbose: bool = False
    debug: bool = False
    prevent_sleep: bool = True
    stop_after: str = "1h"


def validate_config(raw_config: dict, default_config: str) -> AppConfig:
    """Validate config data and fall back to defaults if invalid."""
    try:
        return AppConfig.model_validate(raw_config)
    except ValidationError as e:
        logger.error("Config validation failed: {}. Using defaults.", e)
        return AppConfig.model_validate(toml.loads(default_config))


def load_config(config_path: Path, default_config: str) -> AppConfig:
    """Load configuration from file or create default if missing.

    Args:
        config_path: Path to the config file to load.
        default_config: Default TOML config as string to use as fallback.

    Returns:
        Validated application configuration.

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
        return AppConfig.model_validate(toml.loads(default_config))
    else:
        try:
            raw_config = toml.load(config_path)
            return validate_config(raw_config, default_config)
        except Exception as e:
            logger.exception("Error reading config file ({}). Using default configuration.", e)
            return AppConfig.model_validate(toml.loads(default_config))
