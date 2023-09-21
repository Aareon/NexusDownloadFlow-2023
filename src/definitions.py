import sys
from pathlib import Path


def app_path(path):
    """Return a path to a file within execution temp folder.
    Files that get put in the execution temp folder are files that were bundled
    during the creation of the EXE."""
    if hasattr(sys, "frozen"):
        # we are running in executable mode
        # will return temp folder binary is unpacked to
        app_dir = Path(sys._MEIPASS)
    else:
        # we are running in a normal Python environment
        app_dir = Path(__file__).parent.parent
    return app_dir.joinpath(path).resolve()


def real_path(path):
    """Return a path to a file located within the EXE install directory."""
    # a file relative to the binary that is not in temp folder
    return Path(sys.argv[0]).parent.joinpath(path).resolve()


CONFIG_PATH = real_path("../config/config.toml")

ASSETS_PATH = app_path("assets/")  # default assets stored in temp
REAL_ASSETS_PATH = real_path(
    "../assets/"
)  # locally stored assets/templates (install dir)

SCREENSHOT_PATH = real_path("../monitor-1.png")

DEFAULT_CONFIG = """# NexusDownloadFlow-2023 Config
check_delay = 5  # This is the check delay in seconds
prevent_sleep = true  # prevent computer from entering sleep or turning off display
stop_after = "1h"  # accepts `0` to disable, otherwise use `m` (minutes), `h` (hours). Example: 12m"""
