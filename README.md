# img_downloader 📷⬇️

A small, cross-platform CLI tool for downloading images from a list of URLs.

---

## Key features ✨

- Simple CLI workflow
- Works on Windows, macOS, and Linux
- Reproducible installs with `uv` and `uv.lock`
- Clean project layout ready for GitHub

---

## Requirements ✅

- **uv** installed
- **Python 3.13+** (as defined by the project)

Recommended: pin Python for this repository:

```bash
uv python pin 3.13
```

---

## Installation (uv) 🚀

Clone the repository and sync the project environment:

```bash
git clone https://github.com/bogzak/img_downloader.git
cd img_downloader

uv sync
```

What this does:
- Creates/updates a local virtual environment in `.venv`
- Installs dependencies from `pyproject.toml`
- Uses `uv.lock` (when present) for reproducible installs

---

## Usage ▶️

Run the CLI via `uv run` (recommended):

```bash
uv run imgdl --help
uv run imgdl
```

If you prefer activating the virtual environment manually:

### Windows
```bat
.\.venv\Scripts\activate
imgdl --help
imgdl
```

### macOS / Linux
```bash
source .venv/bin/activate
imgdl --help
imgdl
```

---

## Input format 🧾

Prepare a text file with **one URL per line**, for example:

```text
https://example.com/image1.jpg
https://example.com/image2.png
```

Notes:
- Keep URLs on separate lines.
- If your CLI supports comments/blank lines, they will be ignored; check `imgdl --help`.

---

## Dependency management 📦

Add a runtime dependency:

```bash
uv add <package>
uv sync
```

Add a development dependency:

```bash
uv add --dev ruff pytest
uv sync
```

Upgrade dependencies (and refresh the lockfile/environment):

```bash
uv sync --upgrade
```

---

## Troubleshooting 🧩

### `Failed to spawn: imgdl` / `program not found`

This usually means the console script entry point was not installed into the environment.

Fix:

```bash
uv sync
uv run imgdl --help
```

If it still happens, force an editable install:

```bash
uv pip install -e .
uv run imgdl --help
```
