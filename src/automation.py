"""Auto-clicker automation for NexusDownloadFlow-2026."""

import time
from pathlib import Path

import cv2
import pyautogui
from loguru import logger
from mss import mss

TEMPLATE_NAMES = ("template1.png", "template2.png", "template3.png")
MATCH_THRESHOLD = 3000


def load_template_images(real_assets_path: Path) -> list:
    """Load all template images and return their grayscale forms."""
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


def take_screenshot_gray(sct: mss):
    """Take a screenshot and convert it to grayscale."""
    screenshot = cv2.imread(sct.shot())
    if screenshot is None:
        raise RuntimeError("Failed to capture screenshot for template matching.")
    return cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)


def find_template_target(screenshot_gray, template_gray):
    """Return center target for a template match, or None if not matched."""
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_SQDIFF)
    min_val, _, min_loc, _ = cv2.minMaxLoc(result)
    if min_val >= MATCH_THRESHOLD:
        return None

    top_left = min_loc
    return (
        top_left[0] + template_gray.shape[1] / 2,
        top_left[1] + template_gray.shape[0] / 2,
    )


def click_and_restore_cursor(target) -> None:
    """Click the matched target and restore cursor to its previous position."""
    orig_pos = pyautogui.position()
    pyautogui.leftClick(target)
    pyautogui.moveTo(orig_pos)


def cleanup_screenshot(screenshot_path: Path) -> None:
    """Delete temporary screenshot file if present."""
    if screenshot_path.exists():
        screenshot_path.unlink()


def resolve_check_delay(conf: dict) -> float:
    """Get validated check delay from config."""
    try:
        return max(float(conf.get("check_delay", 5)), 0.1)
    except (TypeError, ValueError):
        return 5.0


def run_autoclicker(conf: dict, real_assets_path: Path, screenshot_path: Path, cli_mode: bool = True) -> None:
    """Main auto-clicker loop for template matching and clicking.

    Continuously captures screenshots, matches them against templates,
    and clicks on matches. Respects configured delay between checks.

    Args:
        conf: Configuration dictionary containing check_delay.
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
