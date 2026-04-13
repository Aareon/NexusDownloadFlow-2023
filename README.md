# NexusDownloadFlow-2026: Auto-clicker script using computer vision

![Python](https://img.shields.io/badge/python-3.14-blue)
![uv](https://img.shields.io/badge/uv-managed-4B8BBE)
![Ruff Lint Workflow](https://github.com/Aareon/NexusDownloadFlow-2023/actions/workflows/ruff-lint.yaml/badge.svg)
![Packaging Workflow](https://github.com/Aareon/NexusDownloadFlow-2023/actions/workflows/pyinstaller-windows.yaml/badge.svg)

NexusDownloadFlow-2026 (NDF) is a script that takes screenshots and detects if any template matches with the
screenshot taken. It was made to automate process with `Wabbajack modlist installation of Nexus' mods` in which
you have to manually click on `Slow download` button is your NexusMods account is not premium.

## How to use NexusDownloadFlow-2026?

Just execute `NexusDownloadFlow-2026.exe` and open your NexusMods' download page.

## Configuration

The default delay for checking for the download button is 5 seconds. This value can be changed in `config/config.toml` by changing the `check_delay` value. It is not recommended to set this any lower than 1.

## Auto-clicker is not clicking

Do not worry, you have to replace the templates files where you installed NDF with the one you will screenshot:
`NexusDownloadFlow-2026/assets/template{x}.png`

+ `template1.png` is the raw `Slow download` button
+ `template2.png` is the `Slow download` button with mouse hovering over
+ `template3.png` is the `Click here` link appearing after clicking on `Slow download` button

## Credits

Thanks to [parsiad](https://github.com/parsiad) for his repository [parsiad/nexus-autodl](https://github.com/parsiad/nexus-autodl)

Thanks to [greg-ynx](https://github.com/greg-ynx) for his work on the [2022 version](https://github.com/greg-ynx/NexusDownloadFlow-2022) of this program.

Please send a :star: over to the awesome repos above!

## Requirements

+ `uv` (Python project/dependency manager)
+ `ruff` (linter/formatter, installed through `uv`)

## Development setup

Install dependencies and developer tools:

```powershell
uv python install 3.14
uv lock
uv sync --locked --extra dev --python 3.14
```

When dependencies change in `pyproject.toml`, regenerate and commit `uv.lock`.

Run lint checks:

```powershell
uv run ruff check .
```

## Contributing

Contributors are encouraged to help improve the code. If you find a bug, please feel free to create an issue and assign yourself if you can. When you fix the bug, please run Ruff (linter) to ensure your code matches the style of the rest of the repository. When finished, please submit a PR.

## Compiling to an EXE

If you would like to compile the program yourself, you are encouraged to do so. You will find running `scripts/create_exe.ps1` will utilize `build.spec` to compile an executable binary. This is the script we use to generate a new release. Using `create_exe.ps1` requires `uv`.

## Release process

Releases are automated with GitHub Actions in `.github/workflows/release.yaml`.

Automatic release from a tag:

```powershell
git tag v1.0.0
git push origin v1.0.0
```

Manual release from Actions:

1. Open the `Create GitHub Release` workflow.
2. Run workflow with `tag_name` (required), and optional `release_name` and `prerelease`.

The workflow builds the Windows EXE, generates SHA256 checksums, and attaches both to the GitHub Release.
