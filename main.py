import time

import cv2
import pyautogui
import toml
from mss import mss

from config.definitions import CONFIG_PATH, DEFAULT_CONFIG, ROOT_DIR, assets_dir
from pathlib import Path


def load_config(config_path: Path | str, default_config: str) -> dict:
    if not config_path.exists():
        print(f"Config not found, creating {CONFIG_PATH}")
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
            return default_config


if __name__ == "__main__":
    print("NexusDownloadFlow 2022 starting...")
    CONF = load_config(CONFIG_PATH, DEFAULT_CONFIG)
    print(
        "Do not forget to replace the assets templates (1, 2 & 3) "
        "in order to match with the screenshots taken from your monitor!"
    )
    print(f"Delay is set to {CONF['check_delay']} seconds")
    try:
        templates = [
            cv2.imread(str(assets_dir / "template1.png")),
            cv2.imread(str(assets_dir / "template2.png")),
            cv2.imread(str(assets_dir / "template3.png")),
        ]
        with mss() as sct:
            while True:
                for i in range(1, 4):
                    template = templates[i - 1]
                    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                    screenshot = cv2.imread(sct.shot())
                    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                    res = cv2.matchTemplate(
                        screenshot_gray, template_gray, cv2.TM_SQDIFF
                    )
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                    threshold = 3000
                    if min_val < threshold:
                        print("Matching template!")
                        top_left = min_loc
                        target = (
                            top_left[0] + template_gray.shape[1] / 2,
                            top_left[1] + template_gray.shape[0] / 2,
                        )
                        pyautogui.leftClick(target)
                        break
                time.sleep(CONF["check_delay"])
    except SystemExit:
        print("Exiting the program...")
        raise
    finally:
        time.sleep(CONF["check_delay"])
        monitor_img_fp = ROOT_DIR / "monitor-1.png"
        if monitor_img_fp.exists():
            monitor_img_fp.unlink()
        else:
            print("The monitor_img_fp does not exist")
        print("Program ended")
