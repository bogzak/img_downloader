from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Set


@dataclass(frozen=True)
class ParsedLinks:
    urls: List[str]
    duplicates_skipped: int


class LinkParser:
    def parse_file(self, path: Path) -> ParsedLinks:
        seen: Set[str] = set()
        unique_urls: List[str] = []
        duplicates = 0

        with path.open("r", encoding="utf-8") as f:
            for raw_line in f:
                url = self._normalize_line(raw_line)
                if not url:
                    continue

                if url in seen:
                    duplicates += 1
                    continue

                seen.add(url)
                unique_urls.append(url)

        return ParsedLinks(urls=unique_urls, duplicates_skipped=duplicates)

    @staticmethod
    def _normalize_line(line: str) -> str:
        s = line.strip()
        if not s or s.startswith("#"):
            return ""
        s = s.rstrip(",;")

        return s
