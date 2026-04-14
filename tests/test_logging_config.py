from pathlib import Path

from loguru import logger

from src.logging_config import configure_logging


def test_configure_logging_with_file_sink_writes_warning(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "nexusdownloadflow.log"

    configure_logging("WARNING", log_file)
    logger.warning("warning message")
    logger.info("info message")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "warning message" in content


def test_configure_logging_without_file_sink() -> None:
    configure_logging("INFO", None)
    logger.info("console-only message")
