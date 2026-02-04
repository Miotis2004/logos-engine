from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..ontology.models import ExplanationTrace, UncertaintyMarker


@dataclass
class AgentResult:
    created_entities: List[str] = field(default_factory=list)
    updated_entities: List[str] = field(default_factory=list)
    relations_added: List[str] = field(default_factory=list)
    uncertainty_markers: List[UncertaintyMarker] = field(default_factory=list)
    notes_for_auditor: List[str] = field(default_factory=list)
    traces: List[ExplanationTrace] = field(default_factory=list)


class BaseAgent:
    name = "base"

    def run(self, graph, context) -> AgentResult:  # type: ignore[override]
        raise NotImplementedError
