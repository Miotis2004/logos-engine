from __future__ import annotations

from ..ontology.graph import OntologyGraph
from .base import AgentResult, BaseAgent


class LogicAuditor(BaseAgent):
    name = "logic_auditor"

    def run(self, graph: OntologyGraph, context: dict) -> AgentResult:
        result = AgentResult()
        errors = graph.validate()
        if errors:
            result.notes_for_auditor.extend(errors)
        return result
