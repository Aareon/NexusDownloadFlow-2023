from pathlib import Path

import pytest
from pydantic import ValidationError

from src.config import AppConfig, load_config


def test_app_config_accepts_valid_stop_after_values() -> None:
    conf_minutes = AppConfig.model_validate({"stop_after": "12m"})
    conf_hours = AppConfig.model_validate({"stop_after": "1h"})
    conf_disabled = AppConfig.model_validate({"stop_after": "0"})

    assert conf_minutes.stop_after == "12m"
    assert conf_hours.stop_after == "1h"
    assert conf_disabled.stop_after == "0"


def test_app_config_rejects_invalid_stop_after_values() -> None:
    with pytest.raises(ValidationError):
        AppConfig.model_validate({"stop_after": "abc"})


def test_load_config_falls_back_to_defaults_on_invalid_file(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text("check_delay = -1\nstop_after = 'bad'\n", encoding="utf-8")

    default_config = (
        "check_delay = 5\n"
        "verbose = false\n"
        "debug = false\n"
        "prevent_sleep = true\n"
        "stop_after = \"1h\"\n"
    )

    conf = load_config(config_path, default_config)

    assert conf.check_delay == 5
    assert conf.stop_after == "1h"


def test_load_config_creates_missing_file(tmp_path: Path) -> None:
    config_path = tmp_path / "new-config.toml"
    default_config = (
        "check_delay = 5\n"
        "verbose = false\n"
        "debug = false\n"
        "prevent_sleep = true\n"
        "stop_after = \"1h\"\n"
    )

    conf = load_config(config_path, default_config)

    assert config_path.exists()
    assert conf.check_delay == 5
    assert conf.verbose is False


def test_load_config_reads_existing_valid_file(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        "check_delay = 2.5\nverbose = true\ndebug = false\n"
        "prevent_sleep = false\nstop_after = \"12m\"\n",
        encoding="utf-8",
    )
    default_config = (
        "check_delay = 5\n"
        "verbose = false\n"
        "debug = false\n"
        "prevent_sleep = true\n"
        "stop_after = \"1h\"\n"
    )

    conf = load_config(config_path, default_config)

    assert conf.check_delay == 2.5
    assert conf.verbose is True
    assert conf.prevent_sleep is False
    assert conf.stop_after == "12m"
