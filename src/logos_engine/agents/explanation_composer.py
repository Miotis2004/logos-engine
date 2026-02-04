from __future__ import annotations

from ..ontology.graph import OntologyGraph
from .base import AgentResult, BaseAgent


class ExplanationComposer(BaseAgent):
    name = "explanation_composer"

    def run(self, graph: OntologyGraph, context: dict) -> AgentResult:
        result = AgentResult()
        claim_count = len(graph.entities.get("Claim", {}))
        evidence_count = len(graph.entities.get("Evidence", {}))
        result.notes_for_auditor.append(
            f"Composed explanation with {claim_count} claims and {evidence_count} evidence items."
        )
        return result
