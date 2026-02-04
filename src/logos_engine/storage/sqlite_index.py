from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class SQLiteIndex:
    path: Path

    def initialize(self) -> None:
        """Placeholder for future SQLite schema initialization."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()
