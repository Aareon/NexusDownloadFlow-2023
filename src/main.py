import sys
import time

from src.assets import load_assets
from src.automation import run_autoclicker
from src.config import load_config
from src.definitions import (
    ASSETS_PATH,
    CONFIG_PATH,
    DEFAULT_CONFIG,
    REAL_ASSETS_PATH,
    SCREENSHOT_PATH,
)

if __name__ == "__main__":
    sep = "━" * max(
        [
            len(str(CONFIG_PATH)) + 13,
            len(str(REAL_ASSETS_PATH)) + 13,
            len(str(SCREENSHOT_PATH)) + 17,
        ]
    )
    print("NexusDownloadFlow-2023 starting...")
    print(f"┏{sep}┓")
    print(
        f"┃Config path: {CONFIG_PATH}{' ' * (len(sep) - len(str(CONFIG_PATH)) - 13)}┃"
    )
    print(
        f"┃Assets path: {REAL_ASSETS_PATH}{' ' * (len(sep) - len(str(REAL_ASSETS_PATH)) - 13)}┃"
    )
    print(
        f"┃Screenshot path: {SCREENSHOT_PATH}{' ' * (len(sep) - len(str(SCREENSHOT_PATH)) - 17)}┃"
    )
    print(f"┗{sep}┛")
    CONF = load_config(CONFIG_PATH, DEFAULT_CONFIG)
    load_assets(ASSETS_PATH, REAL_ASSETS_PATH)
    print(
        "Do not forget to replace the assets templates (1, 2 & 3) "
        "in order to match with the screenshots taken from your monitor!"
    )
    print(f"Delay is set to {CONF['check_delay']} second(s)")
    try:
        run_autoclicker(CONF, REAL_ASSETS_PATH, SCREENSHOT_PATH)
    except (SystemExit, KeyboardInterrupt):
        print("\nExiting the program...")
    except FileNotFoundError as e:
        print(f"\n{e}")
    except PermissionError:
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
