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

## CLI Parameters Documentation

This section provides details about the most important command-line interface (CLI) parameters for the image downloader tool (`imgdl`).

### `--input` / `-i`
- **Type:** `Path`
- **Description:** Specifies the path to the file containing URLs to download. The default is `links.txt`.

### `--output` / `-o`
- **Type:** `Path`
- **Description:** Specifies the output directory where downloaded files will be saved. The default is `downloads`.

### `--timeout`
- **Type:** `float`
- **Default:** `30.0`
- **Description:** Defines the request timeout in seconds. It specifies the maximum time the downloader will wait for a response.

### `--retries`
- **Type:** `int`
- **Default:** `3`
- **Description:** Specifies how many times the downloader will retry a failed request before marking it as failed.

### `--verbose` / `-v`
- **Type:** `flag`
- **Description:** Enables debug logging, which provides more detailed output during execution.

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
