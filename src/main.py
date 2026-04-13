import sys
import time

from loguru import logger

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
from src.logging_config import configure_logging

if __name__ == "__main__":
    configure_logging()
    sep = "━" * max(
        [
            len(str(CONFIG_PATH)) + 13,
            len(str(REAL_ASSETS_PATH)) + 13,
            len(str(SCREENSHOT_PATH)) + 17,
        ]
    )
    logger.info("NexusDownloadFlow-2026 starting...")
    logger.info(f"┏{sep}┓")
    logger.info(
        f"┃Config path: {CONFIG_PATH}{' ' * (len(sep) - len(str(CONFIG_PATH)) - 13)}┃"
    )
    logger.info(
        f"┃Assets path: {REAL_ASSETS_PATH}{' ' * (len(sep) - len(str(REAL_ASSETS_PATH)) - 13)}┃"
    )
    logger.info(
        f"┃Screenshot path: {SCREENSHOT_PATH}{' ' * (len(sep) - len(str(SCREENSHOT_PATH)) - 17)}┃"
    )
    logger.info(f"┗{sep}┛")
    CONF = load_config(CONFIG_PATH, DEFAULT_CONFIG)
    load_assets(ASSETS_PATH, REAL_ASSETS_PATH)
    logger.info(
        "Do not forget to replace the assets templates (1, 2 & 3) "
        "in order to match with the screenshots taken from your monitor!"
    )
    logger.info("Delay is set to {} second(s)", CONF["check_delay"])
    try:
        run_autoclicker(CONF, REAL_ASSETS_PATH, SCREENSHOT_PATH)
    except (SystemExit, KeyboardInterrupt):
        logger.info("Exiting the program...")
    except FileNotFoundError as e:
        logger.error("{}", e)
    except PermissionError:
        logger.error(
            "\nCould not create/delete 'monitor-1.png' due to a permission error. "
            "This can happen when your computer goes to sleep, "
            "or the folder you installed to requires elevated priveleges."
        )
    except Exception as e:
        logger.exception("Unexpected exception {}: {}", type(e), e)
    finally:
        time.sleep(0.1)
        if SCREENSHOT_PATH.exists():
            SCREENSHOT_PATH.unlink()
        else:
            logger.warning("The screenshot does not exist")
        logger.info("Done")
        sys.exit(0)
