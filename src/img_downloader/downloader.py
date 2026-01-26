from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .utils import filename_from_url, sanitize_filename, unique_destination


@dataclass(frozen=True, slots=True)
class DownloadResult:
    url: str
    status: str  # "ok" | "skipped" | "failed"
    path: Optional[Path] = None
    error: Optional[str] = None


class ImageDownloader:
    """Downloads files using a configured requests.Session with retries."""

    def __init__(
        self,
        *,
        timeout_seconds: float,
        retries: int,
        backoff_factor: float,
        user_agent: str,
    ) -> None:
        self._timeout_seconds = timeout_seconds
        self._session = self._build_session(retries=retries, backoff_factor=backoff_factor)
        self._session.headers.update({"User-Agent": user_agent})

    def close(self) -> None:
        self._session.close()

    def _build_session(self, *, retries: int, backoff_factor: float) -> requests.Session:
        session = requests.Session()

        retry = Retry(
            total=retries,
            connect=retries,
            read=retries,
            status=retries,
            backoff_factor=backoff_factor,
            status_forcelist=(408, 429, 500, 502, 503, 504),
            allowed_methods=("GET",),
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def download(self, url: str, dest_dir: Path) -> DownloadResult:
        dest_dir.mkdir(parents=True, exist_ok=True)

        raw_name = filename_from_url(url)
        safe_name = sanitize_filename(raw_name, fallback="download")
        dest = unique_destination(dest_dir, safe_name, url=url)

        if dest.exists() and dest.stat().st_size > 0:
            logging.info("Skip (already exists): %s", dest.name)
            return DownloadResult(url=url, status="skipped", path=dest)

        tmp = dest.with_suffix(dest.suffix + ".part")

        try:
            with self._session.get(url, stream=True, timeout=self._timeout_seconds) as resp:
                resp.raise_for_status()
                with open(tmp, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 64):
                        if chunk:
                            f.write(chunk)

            if tmp.stat().st_size == 0:
                tmp.unlink(missing_ok=True)
                return DownloadResult(url=url, status="failed", error="Downloaded file is empty")

            shutil.move(str(tmp), str(dest))
            logging.info("OK: %s", dest.name)
            return DownloadResult(url=url, status="ok", path=dest)

        except Exception as e:  # noqa: BLE001 - CLI tool should report any failure per URL
            tmp.unlink(missing_ok=True)
            logging.error("Failed: %s (%s)", url, e)
            return DownloadResult(url=url, status="failed", error=str(e))
