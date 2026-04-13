"""Build pipeline for NexusDownloadFlow.

Runs lock, lint, tests, and packaging in sequence using uv.
"""

from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path

PYTHON_VERSION = "3.14"


def run_step(label: str, command: list[str], cwd: Path) -> None:
    """Run a single build step and fail fast if it errors."""
    print(f"\n==> {label}")
    print("$", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    """Execute the full build pipeline."""
    project_root = Path(__file__).resolve().parent
    pyproject_path = project_root / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        pyproject_data = tomllib.load(f)
    project_version = pyproject_data["project"]["version"]

    print(f"Building NexusDownloadFlow version {project_version}")

    steps = [
        ("Lock dependencies", ["uv", "lock"]),
        (
            "Sync dependencies",
            ["uv", "sync", "--locked", "--extra", "dev", "--python", PYTHON_VERSION],
        ),
        ("Ruff lint", ["uv", "run", "--python", PYTHON_VERSION, "ruff", "check", "src"]),
        ("Pytest", ["uv", "run", "--python", PYTHON_VERSION, "pytest", "-q"]),
        (
            "PyInstaller build",
            [
                "uv",
                "run",
                "--python",
                PYTHON_VERSION,
                "pyinstaller",
                "build.spec",
                "--noconfirm",
                "--clean",
            ],
        ),
    ]

    try:
        for label, command in steps:
            run_step(label, command, project_root)
    except subprocess.CalledProcessError as exc:
        print(f"\nBuild failed during step with exit code {exc.returncode}")
        return exc.returncode

    print("\nBuild completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
