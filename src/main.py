"""Application entrypoint for NexusDownloadFlow."""

import argparse
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


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for runtime logging controls."""
    parser = argparse.ArgumentParser(description="NexusDownloadFlow")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging (INFO level).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging (DEBUG level).",
    )
    return parser.parse_args()


def resolve_log_level(args: argparse.Namespace, conf) -> str:
    """Resolve effective log level using CLI flags and config.

    CLI flags take precedence over config values.
    """
    if args.debug:
        return "DEBUG"
    if args.verbose:
        return "INFO"
    if conf.debug:
        return "DEBUG"
    if conf.verbose:
        return "INFO"
    return "WARNING"


def main() -> None:
    """Initialize runtime resources and start the auto-clicker loop."""
    args = parse_args()
    configure_logging("INFO")
    sep = "━" * max(
        [
            len(str(CONFIG_PATH)) + 13,
            len(str(REAL_ASSETS_PATH)) + 13,
            len(str(SCREENSHOT_PATH)) + 17,
        ]
    )
    logger.info("NexusDownloadFlow starting...")
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
    configure_logging(resolve_log_level(args, CONF))

    logger.debug("Effective runtime config: {}", CONF.model_dump())
    load_assets(ASSETS_PATH, REAL_ASSETS_PATH)
    logger.info(
        "Do not forget to replace the assets templates (1, 2 & 3) "
        "in order to match with the screenshots taken from your monitor!"
    )
    logger.info("Delay is set to {} second(s)", CONF.check_delay)
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


if __name__ == "__main__":
    main()
