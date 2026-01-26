from __future__ import annotations

import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

from .config import AppConfig
from .downloader import ImageDownloader, DownloadResult
from .link_parser import LinkParser
from .logging_utils import setup_logging


DEFAULT_INPUT = Path("links.txt")
DEFAULT_OUTPUT_DIR = Path("downloads")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="imgdl",
        description="Download images/files from a text file containing URLs.",
    )
    p.add_argument("--input", "-i", type=Path, default=DEFAULT_INPUT, help="Path to links file.")
    p.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory.")
    p.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Log file path (default: <output>/download.log).",
    )
    p.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds.")
    p.add_argument("--retries", type=int, default=3, help="Retry count for transient errors.")
    p.add_argument(
        "--backoff",
        type=float,
        default=0.5,
        help="Backoff factor for retries (e.g., 0.5 => 0.5s, 1s, 2s, ...).",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Parallel download workers (threads). Use 1 to disable concurrency.",
    )
    p.add_argument("--encoding", type=str, default="utf-8", help="Links file encoding.")
    p.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging.")
    return p


def _to_config(args: argparse.Namespace) -> AppConfig:
    output_dir: Path = args.output
    log_file: Path = args.log_file or (output_dir / "download.log")
    return AppConfig(
        input_file=args.input,
        output_dir=output_dir,
        log_file=log_file,
        timeout_seconds=args.timeout,
        retries=max(0, args.retries),
        backoff_factor=max(0.0, args.backoff),
        workers=max(1, args.workers),
    )


def _summarize(results: Iterable[DownloadResult]) -> tuple[int, int, int]:
    ok = skipped = failed = 0
    for r in results:
        if r.status == "ok":
            ok += 1
        elif r.status == "skipped":
            skipped += 1
        else:
            failed += 1
    return ok, skipped, failed


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    config = _to_config(args)
    setup_logging(config.log_file, verbose=args.verbose)

    logging.info("Links file: %s", config.input_file.resolve())
    logging.info("Output dir: %s", config.output_dir.resolve())
    logging.info("Log file:   %s", config.log_file.resolve())

    if not config.input_file.exists():
        logging.error("Links file does not exist: %s", config.input_file)
        return 2

    urls = LinkParser().parse_file(config.input_file, encoding=args.encoding)
    if not urls:
        logging.warning("No links found in %s", config.input_file)
        return 0

    downloader = ImageDownloader(
        timeout_seconds=config.timeout_seconds,
        retries=config.retries,
        backoff_factor=config.backoff_factor,
        user_agent=config.user_agent,
    )

    results: list[DownloadResult] = []
    try:
        if config.workers == 1:
            for url in urls:
                results.append(downloader.download(url, config.output_dir))
        else:
            with ThreadPoolExecutor(max_workers=config.workers) as pool:
                future_to_url = {pool.submit(downloader.download, u, config.output_dir): u for u in urls}
                for fut in as_completed(future_to_url):
                    results.append(fut.result())
    finally:
        downloader.close()

    ok, skipped, failed = _summarize(results)
    logging.info("Done: ok=%d skipped=%d failed=%d", ok, skipped, failed)

    return 1 if failed else 0
