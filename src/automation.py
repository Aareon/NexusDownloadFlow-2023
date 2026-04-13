"""Auto-clicker automation for NexusDownloadFlow-2023."""

import time
from pathlib import Path

import cv2
import pyautogui
from mss import mss


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
    # load templates and create grayscale image for each
    templates = []
    for template_name in ("template1.png", "template2.png", "template3.png"):
        template_path = real_assets_path / template_name
        template_img = cv2.imread(str(template_path))
        if template_img is None:
            raise FileNotFoundError(
                f"Template could not be loaded: {template_path}. "
                "Ensure template files exist and are valid PNG images."
            )
        templates.append(cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY))

    with mss() as sct:
        match_count = 0  # counter for template matches
        while True:
            for i in range(1, 4):
                template_gray = templates[i - 1]
                screenshot = cv2.imread(
                    sct.shot()
                )  # take screenshot/convert to opencv image
                screenshot_gray = cv2.cvtColor(
                    screenshot, cv2.COLOR_BGR2GRAY
                )  # grayscale screenshot
                res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_SQDIFF)
                min_val, _, min_loc, _ = cv2.minMaxLoc(res)
                threshold = 3000
                if min_val < threshold:
                    match_count += 1
                    if cli_mode:
                        print(f"\r[{match_count}] Download button found!", end="")
                    top_left = min_loc
                    target = (
                        top_left[0] + template_gray.shape[1] / 2,
                        top_left[1] + template_gray.shape[0] / 2,
                    )
                    orig_pos = pyautogui.position()  # original mouse position
                    pyautogui.leftClick(target)  # click the detected download button
                    pyautogui.moveTo(
                        orig_pos
                    )  # move mouse back to where it was originally
                    break
            if screenshot_path.exists():
                screenshot_path.unlink()  # delete screenshot image from filesystem
            try:
                check_delay = max(float(conf.get("check_delay", 5)), 0.1)
            except (TypeError, ValueError):
                check_delay = 5.0
            time.sleep(check_delay)
