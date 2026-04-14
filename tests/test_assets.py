from pathlib import Path

import src.assets as assets_module
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


def test_load_assets_warns_when_some_templates_still_missing(tmp_path: Path) -> None:
    source_assets = tmp_path / "source"
    real_assets = tmp_path / "real"

    source_assets.mkdir(parents=True, exist_ok=True)
    (source_assets / "template1.png").write_text("x", encoding="utf-8")

    load_assets(source_assets, real_assets)

    assert (real_assets / "template1.png").exists()
    assert not (real_assets / "template2.png").exists()
    assert not (real_assets / "template3.png").exists()


def test_load_assets_handles_internal_exception(monkeypatch, tmp_path: Path) -> None:
    source_assets = tmp_path / "source"
    real_assets = tmp_path / "real"

    original_mkdir = Path.mkdir

    def raise_mkdir(*args, **kwargs):
        current_path = args[0]
        if current_path == real_assets:
            raise OSError("mkdir failed")
        return original_mkdir(*args, **kwargs)

    monkeypatch.setattr(assets_module.Path, "mkdir", raise_mkdir)

    # Function should swallow internal errors and not raise.
    load_assets(source_assets, real_assets)

    assert not real_assets.exists()
