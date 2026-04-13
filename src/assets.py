"""Asset and template loading for NexusDownloadFlow."""

import shutil
from pathlib import Path

from loguru import logger


def load_assets(assets_path: Path, real_assets_path: Path) -> None:
    """Copy bundled template assets to local installation directory.

    If local assets folder does not exist, creates it and copies templates
    from the bundled assets folder.

    Args:
        assets_path: Path to bundled assets (in executable/temp folder).
        real_assets_path: Path to local assets folder (install directory).

    Raises:
        FileNotFoundError: If unable to create or copy assets.
    """
    required_templates = ("template1.png", "template2.png", "template3.png")
    try:
        real_assets_path.mkdir(parents=True, exist_ok=True)
        missing_templates = [
            name
            for name in required_templates
            if not (real_assets_path / name).exists()
        ]
        if not missing_templates:
            return

        logger.info("Local assets are missing templates. Copying templates...")
        if not assets_path.exists():
            logger.warning(
                "Bundled assets folder is missing. Place template1.png, template2.png, and template3.png in {}.",
                real_assets_path,
            )
            return

        for template_name in missing_templates:
            source = assets_path / template_name
            if source.is_file():
                shutil.copy(source, real_assets_path / template_name)

        still_missing = [
            name
            for name in required_templates
            if not (real_assets_path / name).exists()
        ]
        if still_missing:
            logger.warning(
                "Some templates are still missing after copy attempt: {}",
                ", ".join(still_missing),
            )
        else:
            logger.info("Done copying templates.")
    except Exception as e:
        logger.exception("Failed to create assets folder and copy templates: {}", e)
