from pathlib import Path

from src.automation import cleanup_screenshot, parse_stop_after_seconds
from src.config import AppConfig


def test_parse_stop_after_seconds_values() -> None:
    assert parse_stop_after_seconds("0") is None
    assert parse_stop_after_seconds("2m") == 120.0
    assert parse_stop_after_seconds("1h") == 3600.0


def test_cleanup_screenshot_deletes_existing_file(tmp_path: Path) -> None:
    screenshot_path = tmp_path / "monitor-1.png"
    screenshot_path.write_text("test", encoding="utf-8")

    cleanup_screenshot(screenshot_path)

    assert not screenshot_path.exists()


def test_app_config_check_delay_bounds() -> None:
    conf = AppConfig(check_delay=0.5)
    assert conf.check_delay == 0.5
