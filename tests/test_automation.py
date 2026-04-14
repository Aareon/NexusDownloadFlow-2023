from pathlib import Path

import cv2
import numpy as np
import pytest

import src.automation as automation
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


def test_find_template_target_match_and_no_match() -> None:
    screenshot = np.zeros((12, 12), dtype=np.uint8)
    screenshot[3:6, 4:7] = 255
    template = np.full((3, 3), 255, dtype=np.uint8)

    matched = automation.find_template_target(screenshot, template)
    assert matched is not None

    no_match_template = np.full((3, 3), 123, dtype=np.uint8)
    not_matched = automation.find_template_target(screenshot, no_match_template)
    assert not_matched is None


def test_take_screenshot_gray_uses_requested_output_path(tmp_path: Path) -> None:
    screenshot_path = tmp_path / "monitor-1.png"
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    image[:, :, 1] = 255

    class FakeSct:
        def shot(self, output: str) -> str:
            cv2.imwrite(output, image)
            return output

    gray = automation.take_screenshot_gray(FakeSct(), screenshot_path)

    assert screenshot_path.exists()
    assert gray.shape == (10, 10)


def test_load_template_images_raises_for_missing_template(tmp_path: Path) -> None:
    assets_path = tmp_path / "assets"
    assets_path.mkdir(parents=True, exist_ok=True)

    with np.errstate(all="ignore"):
        cv2.imwrite(str(assets_path / "template1.png"), np.zeros((5, 5, 3), dtype=np.uint8))
        cv2.imwrite(str(assets_path / "template2.png"), np.zeros((5, 5, 3), dtype=np.uint8))

    with pytest.raises(FileNotFoundError):
        automation.load_template_images(assets_path)


def test_run_autoclicker_honors_stop_after_and_restores_sleep_state(monkeypatch, tmp_path: Path) -> None:
    conf = AppConfig(check_delay=5, prevent_sleep=True, stop_after="1m")
    screenshot_path = tmp_path / "monitor-1.png"

    class DummyMss:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    calls: list[bool] = []

    monkeypatch.setattr(automation, "load_template_images", lambda _: [])
    monkeypatch.setattr(automation, "mss", lambda: DummyMss())
    monkeypatch.setattr(automation, "set_sleep_prevention", lambda enabled: calls.append(enabled))

    monotonic_values = iter([100.0, 200.0])
    monkeypatch.setattr(automation.time, "monotonic", lambda: next(monotonic_values))

    automation.run_autoclicker(conf, tmp_path, screenshot_path, cli_mode=False)

    assert calls == [True, False]


def test_set_sleep_prevention_noop_without_windll(monkeypatch) -> None:
    monkeypatch.delattr(automation.ctypes, "windll", raising=False)

    automation.set_sleep_prevention(True)
    automation.set_sleep_prevention(False)


def test_run_autoclicker_cleans_screenshot_on_exception(monkeypatch, tmp_path: Path) -> None:
    conf = AppConfig(check_delay=1.0, prevent_sleep=False, stop_after="0")
    screenshot_path = tmp_path / "monitor-1.png"

    class DummyMss:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_take_screenshot_gray(_sct, screenshot_target: Path):
        screenshot_target.write_text("temp", encoding="utf-8")
        raise RuntimeError("capture failed")

    monkeypatch.setattr(automation, "load_template_images", lambda _: [])
    monkeypatch.setattr(automation, "mss", lambda: DummyMss())
    monkeypatch.setattr(automation, "take_screenshot_gray", fake_take_screenshot_gray)

    with pytest.raises(RuntimeError):
        automation.run_autoclicker(conf, tmp_path, screenshot_path, cli_mode=False)

    assert not screenshot_path.exists()
