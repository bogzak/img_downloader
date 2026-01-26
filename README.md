# Photo Downloader (imgdl)

Cross-platform CLI utility to download images/files from a text file with URLs.

## Features

- Works on Windows/macOS/Linux (uses `pathlib`, no OS-specific assumptions)
- Robust link parsing: ignores blank lines, `#` comments, trailing CSV/semicolon fragments
- Safe/atomic downloads (`.part` temp file then rename)
- Retries with backoff for transient network errors
- Optional parallel downloads

## Install (local / editable)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Usage

Download using defaults (`links.txt` -> `downloads/`):

```bash
imgdl
```

Custom paths and options:

```bash
imgdl --input links.txt --output downloads --workers 8 --timeout 30 --retries 3
```

### Link file format (`links.txt`)

- One URL per line
- Blank lines ignored
- `#` comments supported
- If a line contains `,` or `;`, everything after the first delimiter is ignored (useful for CSV exports)

Example:

```text
# Product images
https://example.com/a.jpg
https://example.com/b.png, some comment
https://example.com/c.webp; another comment
```

## Development

Run tests:

```bash
pytest
```

Lint:

```bash
ruff check .
```

## License

MIT
