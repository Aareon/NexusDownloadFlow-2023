"""Auto-clicker automation for NexusDownloadFlow-2026."""

import time
from pathlib import Path
from typing import Any

import cv2
import pyautogui
from loguru import logger
from mss import mss
from numpy.typing import NDArray

from src.config import AppConfig

TEMPLATE_NAMES = ("template1.png", "template2.png", "template3.png")
MATCH_THRESHOLD = 3000


def load_template_images(real_assets_path: Path) -> list[NDArray[Any]]:
    """Load template images and return grayscale arrays.

    Args:
        real_assets_path: Directory containing template image files.

    Returns:
        Grayscale template arrays in matching order.
    """
    templates = []
    for template_name in TEMPLATE_NAMES:
        template_path = real_assets_path / template_name
        template_img = cv2.imread(str(template_path))
        if template_img is None:
            raise FileNotFoundError(
                f"Template could not be loaded: {template_path}. "
                "Ensure template files exist and are valid PNG images."
            )
        templates.append(cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY))
    return templates


def take_screenshot_gray(sct: mss) -> NDArray[Any]:
    """Capture a screenshot and convert it to grayscale image array."""
    screenshot = cv2.imread(sct.shot())
    if screenshot is None:
        raise RuntimeError("Failed to capture screenshot for template matching.")
    return cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)


def find_template_target(
    screenshot_gray: NDArray[Any], template_gray: NDArray[Any]
) -> tuple[float, float] | None:
    """Compute click target for a matched template.

    Args:
        screenshot_gray: Current screenshot as grayscale image array.
        template_gray: Template image as grayscale image array.

    Returns:
        Center coordinate for click target if matched; otherwise None.
    """
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_SQDIFF)
    min_val, _, min_loc, _ = cv2.minMaxLoc(result)
    if min_val >= MATCH_THRESHOLD:
        return None

    top_left = min_loc
    return (
        top_left[0] + template_gray.shape[1] / 2,
        top_left[1] + template_gray.shape[0] / 2,
    )


def click_and_restore_cursor(target: tuple[float, float]) -> None:
    """Click the matched target and restore cursor to its previous position."""
    orig_pos = pyautogui.position()
    pyautogui.leftClick(target)
    pyautogui.moveTo(orig_pos)


def cleanup_screenshot(screenshot_path: Path) -> None:
    """Delete temporary screenshot file if present."""
    if screenshot_path.exists():
        screenshot_path.unlink()


def resolve_check_delay(conf: AppConfig) -> float:
    """Get validated check delay from config model."""
    return conf.check_delay


def run_autoclicker(
    conf: AppConfig,
    real_assets_path: Path,
    screenshot_path: Path,
    cli_mode: bool = True,
) -> None:
    """Main auto-clicker loop for template matching and clicking.

    Continuously captures screenshots, matches them against templates,
    and clicks on matches. Respects configured delay between checks.

    Args:
        conf: Validated application config.
        real_assets_path: Path to template assets.
        screenshot_path: Path where temporary screenshots are stored.
        cli_mode: If True, print match count to terminal.

    Raises:
        FileNotFoundError: If template files cannot be loaded.
        KeyboardInterrupt: When user exits with Ctrl+C.
    """
    templates = load_template_images(real_assets_path)

    with mss() as sct:
        match_count = 0
        while True:
            screenshot_gray = take_screenshot_gray(sct)
            for template_gray in templates:
                target = find_template_target(screenshot_gray, template_gray)
                if target is not None:
                    match_count += 1
                    if cli_mode:
                        logger.info("Download button found (match #{})", match_count)
                    click_and_restore_cursor(target)
                    break
            cleanup_screenshot(screenshot_path)
            time.sleep(resolve_check_delay(conf))
