from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List

from ..ontology.models import ExplanationTrace, ReasoningStep, UncertaintyMarker
from ..utils.ids import new_id


@dataclass
class TraceLogger:
    log_dir: Path
    traces: List[ExplanationTrace] = field(default_factory=list)

    def add_trace(self, trace: ExplanationTrace) -> None:
        self.traces.append(trace)

    def export(self) -> List[Path]:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        exported: List[Path] = []
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        for trace in self.traces:
            path = self.log_dir / f"trace_{trace.subject_id}_{timestamp}.json"
            with path.open("w", encoding="utf-8") as handle:
                json.dump(trace.to_dict(), handle, indent=2)
            exported.append(path)
        return exported


def make_step(rule_id: str, description: str, delta: float, resulting_score: float | None) -> ReasoningStep:
    return ReasoningStep(
        id=new_id("step"),
        rule_id=rule_id,
        description=description,
        delta=delta,
        resulting_score=resulting_score,
    )


def make_trace(subject_id: str, steps: List[ReasoningStep], uncertainties: List[UncertaintyMarker]) -> ExplanationTrace:
    return ExplanationTrace(
        id=new_id("trace"),
        subject_id=subject_id,
        steps=steps,
        uncertainty_markers=uncertainties,
    )


def make_uncertainty(subject_id: str, note: str, severity: float | None = None) -> UncertaintyMarker:
    return UncertaintyMarker(id=new_id("uncertainty"), subject_id=subject_id, note=note, severity=severity)
