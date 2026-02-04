from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Local runtime settings."""

    data_dir: Path = Path("data")
    logs_dir: Path = Path("logs")
    config_dir: Path = Path("config")

    def ensure_dirs(self) -> None:
        """Create expected local directories if they do not exist."""
        (self.data_dir / "documents").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "synthetic_cases").mkdir(parents=True, exist_ok=True)
        (self.logs_dir / "reasoning_traces").mkdir(parents=True, exist_ok=True)
