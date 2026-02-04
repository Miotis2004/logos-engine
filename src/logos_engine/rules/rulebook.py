from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


def _parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _load_simple_yaml(path: Path) -> Dict[str, Any]:
    lines = [line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()]
    idx = 0
    result: Dict[str, Any] = {}
    while idx < len(lines):
        line = lines[idx]
        if not line.strip() or line.lstrip().startswith("#"):
            idx += 1
            continue
        if line.startswith(" "):
            idx += 1
            continue
        if ":" not in line:
            idx += 1
            continue
        key, _ = line.split(":", 1)
        key = key.strip()
        idx += 1
        if idx >= len(lines) or not lines[idx].startswith(" "):
            result[key] = None
            continue
        if lines[idx].lstrip().startswith("-"):
            items: List[Dict[str, Any]] = []
            while idx < len(lines) and lines[idx].startswith(" "):
                if lines[idx].lstrip().startswith("-"):
                    item_line = lines[idx].lstrip()[2:]
                    item: Dict[str, Any] = {}
                    if item_line:
                        item_key, item_value = item_line.split(":", 1)
                        item[item_key.strip()] = _parse_scalar(item_value.strip())
                    idx += 1
                    while idx < len(lines) and lines[idx].startswith("    ") and not lines[idx].lstrip().startswith("-"):
                        sub_key, sub_value = lines[idx].strip().split(":", 1)
                        item[sub_key.strip()] = _parse_scalar(sub_value.strip())
                        idx += 1
                    items.append(item)
                else:
                    idx += 1
            result[key] = items
        else:
            mapping: Dict[str, Any] = {}
            while idx < len(lines) and lines[idx].startswith(" ") and not lines[idx].lstrip().startswith("-"):
                sub_key, sub_value = lines[idx].strip().split(":", 1)
                mapping[sub_key.strip()] = _parse_scalar(sub_value.strip())
                idx += 1
            result[key] = mapping
    return result


@dataclass
class Rulebook:
    evidence_reliability_baselines: Dict[str, float]
    relevance_rules: List[Dict[str, Any]]
    assumption_penalties: Dict[str, float]
    constants: Dict[str, float]

    @classmethod
    def from_path(cls, path: Path) -> "Rulebook":
        payload = _load_simple_yaml(path)
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
