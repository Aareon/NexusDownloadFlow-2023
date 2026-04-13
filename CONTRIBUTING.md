# Contributing

Thanks for contributing to NexusDownloadFlow.

## Setup

```powershell
uv python install 3.14
uv lock
uv sync --locked --extra dev --python 3.14
```

## Local checks

Run lint checks before opening a PR:

```powershell
uv run --python 3.14 ruff check src
```

Install pre-commit hooks to enforce lockfile checks on every commit:

```powershell
uv run --python 3.14 pre-commit install
```

## Build locally

```powershell
uv run --python 3.14 pyinstaller build.spec --noconfirm --clean
```

Or use the helper script:

```powershell
./scripts/create_exe.ps1
```

## Pull requests

- Keep changes focused and small.
- Update docs when behavior/config changes.
- Add or update changelog entries in `CHANGELOG.md` when appropriate.
- Ensure CI is green before requesting review.

## Release notes

Releases are automated through GitHub Actions in `.github/workflows/release.yaml`.
