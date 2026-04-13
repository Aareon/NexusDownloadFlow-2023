import shutil
import sys
import time
from pathlib import Path

import cv2
import pyautogui
import toml
from mss import mss

from definitions import (
    ASSETS_PATH,
    CONFIG_PATH,
    DEFAULT_CONFIG,
    REAL_ASSETS_PATH,
    SCREENSHOT_PATH,
)


def load_config(config_path: Path, default_config: str) -> dict:
    if not config_path.exists():
        print(f"Config not found, creating {CONFIG_PATH}")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(config_path, "w") as f:
                f.write(default_config)
                f.flush()
        except Exception as e:
            print(f"An error occurred saving default config to file: {e}")
        finally:
            return toml.loads(default_config)
    else:
        try:
            return toml.load(config_path)
        except Exception as e:
            print(
                f"An error occurred reading config file: {e}"
                "Using default configuration."
            )
            return toml.loads(default_config)


def load_assets():
    # if local assets folder does not exist
    # create, move templates from temp, and return path to real assets folder
    if not REAL_ASSETS_PATH.exists():
        try:
            print("Local assets folder does not exist. Copying templates...")
            REAL_ASSETS_PATH.mkdir(parents=True)
            # copy files from temp assets folder
            files_to_copy = ASSETS_PATH.glob("*")
            for f in files_to_copy:
                if f.is_file():
                    shutil.copy(f, REAL_ASSETS_PATH)
            print("Done copying templates.")
        except Exception as e:
            print(f"Failed to create assets folder and copy templates: {e}")


def run_autoclicker(cli_mode=True):
    # load templates and create grayscale image for each
    templates = []
    for template_name in ("template1.png", "template2.png", "template3.png"):
        template_path = REAL_ASSETS_PATH / template_name
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
            if SCREENSHOT_PATH.exists():
                SCREENSHOT_PATH.unlink()  # delete screenshot image from filesystem
            try:
                check_delay = max(float(CONF.get("check_delay", 5)), 0.1)
            except (TypeError, ValueError):
                check_delay = 5.0
            time.sleep(check_delay)


if __name__ == "__main__":
    sep = "━" * max(
        [
            len(str(CONFIG_PATH)) + 13,
            len(str(ASSETS_PATH)) + 13,
            len(str(SCREENSHOT_PATH)) + 17,
        ]
    )
    print("NexusDownloadFlow-2023 starting...")
    print(f"┏{sep}┓")
    print(
        f"┃Config path: {CONFIG_PATH}{' ' * (len(sep) - len(str(CONFIG_PATH)) - 13)}┃"
    )
    print(
        f"┃Assets path: {ASSETS_PATH}{' ' * (len(sep) - len(str(ASSETS_PATH)) - 13)}┃"
    )
    print(
        f"┃Screenshot path: {SCREENSHOT_PATH}{' ' * (len(sep) - len(str(SCREENSHOT_PATH)) - 17)}┃"
    )
    print(f"┗{sep}┛")
    CONF = load_config(CONFIG_PATH, DEFAULT_CONFIG)
    load_assets()
    print(
        "Do not forget to replace the assets templates (1, 2 & 3) "
        "in order to match with the screenshots taken from your monitor!"
    )
    print(f"Delay is set to {CONF['check_delay']} second(s)")
    try:
        run_autoclicker()
    except (SystemExit, KeyboardInterrupt):
        print("\nExiting the program...")
    except (PermissionError, OSError):
        print(
            "\nCould not create/delete 'monitor-1.png' due to a permission error. "
            "This can happen when your computer goes to sleep, "
            "or the folder you installed to requires elevated priveleges."
        )
    except Exception as e:
        print("\nUnexpected exception " f"{type(e)}: {e}")
    finally:
        time.sleep(0.1)
        if SCREENSHOT_PATH.exists():
            SCREENSHOT_PATH.unlink()
        else:
            print("The screenshot does not exist")
        print("Done")
        sys.exit(0)
