import argparse

from src.config import AppConfig
from src.main import resolve_log_level


def test_resolve_log_level_cli_debug_overrides_config() -> None:
    args = argparse.Namespace(verbose=False, debug=True)
    conf = AppConfig()
    assert resolve_log_level(args, conf) == "DEBUG"


def test_resolve_log_level_cli_verbose_overrides_config() -> None:
    args = argparse.Namespace(verbose=True, debug=False)
    conf = AppConfig(debug=False, verbose=False)
    assert resolve_log_level(args, conf) == "INFO"


def test_resolve_log_level_uses_config_when_no_flags() -> None:
    args = argparse.Namespace(verbose=False, debug=False)

    assert resolve_log_level(args, AppConfig(debug=True)) == "DEBUG"
    assert resolve_log_level(args, AppConfig(verbose=True)) == "INFO"
    assert resolve_log_level(args, AppConfig()) == "WARNING"
