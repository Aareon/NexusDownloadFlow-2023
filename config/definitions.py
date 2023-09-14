from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

main_path = ROOT_DIR / "main.py"

assets_dir = ROOT_DIR / "assets"

DEFAULT_CONFIG = """# NexusDownloadFlow-2023 Config
check_delay = 5  # This is the check delay in seconds"""

CONFIG_PATH = ROOT_DIR / "config.toml"
