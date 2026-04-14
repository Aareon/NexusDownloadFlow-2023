import argparse
import sys
from pathlib import Path

import pytest

import src.main as main_module
from src.config import AppConfig
from src.main import parse_args, resolve_log_level


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


def test_parse_args_defaults(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["nexusdownloadflow"])
    args = parse_args()
    assert args.verbose is False
    assert args.debug is False


def test_parse_args_with_flags(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["nexusdownloadflow", "--verbose", "--debug"])
    args = parse_args()
    assert args.verbose is True
    assert args.debug is True


def test_main_exits_cleanly_on_keyboard_interrupt(monkeypatch, tmp_path: Path) -> None:
    screenshot_path = tmp_path / "monitor-1.png"
    screenshot_path.write_text("tmp", encoding="utf-8")

    monkeypatch.setattr(main_module, "parse_args", lambda: argparse.Namespace(verbose=False, debug=False))
    monkeypatch.setattr(main_module, "configure_logging", lambda *args, **kwargs: None)
    monkeypatch.setattr(main_module, "load_config", lambda *args, **kwargs: AppConfig())
    monkeypatch.setattr(main_module, "load_assets", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        main_module,
        "run_autoclicker",
        lambda *args, **kwargs: (_ for _ in ()).throw(KeyboardInterrupt()),
    )

    monkeypatch.setattr(main_module, "CONFIG_PATH", tmp_path / "config" / "config.toml")
    monkeypatch.setattr(main_module, "REAL_ASSETS_PATH", tmp_path / "assets")
    monkeypatch.setattr(main_module, "SCREENSHOT_PATH", screenshot_path)

    with pytest.raises(SystemExit) as exc_info:
        main_module.main()

    assert exc_info.value.code == 0
    assert not screenshot_path.exists()
