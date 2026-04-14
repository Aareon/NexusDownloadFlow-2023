from pathlib import Path

from src.assets import load_assets


TEMPLATES = ("template1.png", "template2.png", "template3.png")


def _write_templates(target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for template_name in TEMPLATES:
        (target_dir / template_name).write_text("x", encoding="utf-8")


def test_load_assets_copies_missing_templates(tmp_path: Path) -> None:
    source_assets = tmp_path / "source"
    real_assets = tmp_path / "real"
    _write_templates(source_assets)

    load_assets(source_assets, real_assets)

    for template_name in TEMPLATES:
        assert (real_assets / template_name).exists()


def test_load_assets_noop_when_templates_already_present(tmp_path: Path) -> None:
    source_assets = tmp_path / "missing-source"
    real_assets = tmp_path / "real"
    _write_templates(real_assets)

    load_assets(source_assets, real_assets)

    for template_name in TEMPLATES:
        assert (real_assets / template_name).exists()


def test_load_assets_handles_missing_bundled_assets(tmp_path: Path) -> None:
    source_assets = tmp_path / "missing-source"
    real_assets = tmp_path / "real"

    load_assets(source_assets, real_assets)

    assert real_assets.exists()
    for template_name in TEMPLATES:
        assert not (real_assets / template_name).exists()
