from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


@dataclass
class Rulebook:
    evidence_reliability_baselines: Dict[str, float]
    relevance_rules: List[Dict[str, Any]]
    assumption_penalties: Dict[str, float]
    constants: Dict[str, float]

    @classmethod
    def from_path(cls, path: Path) -> "Rulebook":
        with path.open("r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle)
        cls._validate_payload(payload)
        return cls(
            evidence_reliability_baselines=payload["evidence_reliability_baselines"],
            relevance_rules=payload["relevance_rules"],
            assumption_penalties=payload["assumption_penalties"],
            constants=payload["constants"],
        )

    @staticmethod
    def _validate_payload(payload: Dict[str, Any]) -> None:
        required_keys = {
            "evidence_reliability_baselines",
            "relevance_rules",
            "assumption_penalties",
            "constants",
        }
        missing = required_keys - set(payload.keys())
        if missing:
            raise ValueError(f"Missing keys in rulebook: {sorted(missing)}")

    def get_reliability_baseline(self, evidence_type: str) -> float:
        return self.evidence_reliability_baselines.get(
            evidence_type, self.evidence_reliability_baselines.get("unknown", 0.5)
        )

    def get_relevance_rules(self) -> List[Dict[str, Any]]:
        return list(self.relevance_rules)

    def get_assumption_penalties(self) -> Dict[str, float]:
        return dict(self.assumption_penalties)

    def get_constants(self) -> Dict[str, float]:
        return dict(self.constants)
