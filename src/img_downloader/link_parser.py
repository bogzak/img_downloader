from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class LinkParser:
    """Parses a text file containing URLs (one per line)."""

    delimiters: tuple[str, ...] = (",", ";")

    def parse_file(self, path: Path, *, encoding: str = "utf-8") -> list[str]:
        text = path.read_text(encoding=encoding, errors="ignore")
        urls: list[str] = []

        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            for delim in self.delimiters:
                if delim in line:
                    line = line.split(delim, 1)[0].strip()

            if line:
                urls.append(line)

        return urls
