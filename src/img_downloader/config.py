from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AppConfig:
    input_file: Path
    output_dir: Path
    log_file: Path
    timeout_seconds: float = 30.0
    retries: int = 3
    backoff_factor: float = 0.5
    workers: int = 1
    user_agent: str = "imgdl/1.0 (+https://github.com/your-org/photo-downloader)"
