"""Configuration loading and management for NexusDownloadFlow-2023."""

from pathlib import Path

import toml


def load_config(config_path: Path, default_config: str) -> dict:
    """Load configuration from file or create default if missing.

    Args:
        config_path: Path to the config file to load.
        default_config: Default TOML config as string to use as fallback.

    Returns:
        Parsed configuration dictionary.

    """
    if not config_path.exists():
        print(f"Config not found, creating {config_path}")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(config_path, "w") as f:
                f.write(default_config)
                f.flush()
        except Exception as e:
            print(f"An error occurred saving default config to file: {e}")
        return toml.loads(default_config)
    else:
        try:
            return toml.load(config_path)
        except Exception as e:
            print(
                f"An error occurred reading config file: {e}. "
                "Using default configuration."
            )
            return toml.loads(default_config)
