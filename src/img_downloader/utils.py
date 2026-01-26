from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import urlsplit


_INVALID_FILENAME_CHARS = re.compile(r"[\\/:*?\"<>|\x00-\x1F]")  # Windows + control chars
_TRAILING_DOTS_SPACES = re.compile(r"[\.\s]+$")  # Windows disallows trailing dots/spaces


def filename_from_url(url: str) -> str:
    """Extract the filename from a URL path."""
    return Path(urlsplit(url).path).name


def sanitize_filename(name: str, *, fallback: str = "download") -> str:
    name = name.strip()
    name = _INVALID_FILENAME_CHARS.sub("_", name)
    name = _TRAILING_DOTS_SPACES.sub("", name)

    if not name:
        return fallback

    # Avoid reserved Windows device names.
    reserved = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    stem = Path(name).stem
    if stem.upper() in reserved:
        name = f"_{name}"

    return name


def unique_destination(dest_dir: Path, filename: str, *, url: str) -> Path:
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate

    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    p = Path(filename)
    new_name = f"{p.stem}_{h}{p.suffix}"
    return dest_dir / new_name
