from __future__ import annotations

from ..ontology.graph import OntologyGraph
from ..ontology.models import Assumption
from ..ontology.relations import UNDERLIES
from ..utils.ids import new_id
from .base import AgentResult, BaseAgent


class AssumptionDetector(BaseAgent):
    name = "assumption_detector"

    def run(self, graph: OntologyGraph, context: dict) -> AgentResult:
        result = AgentResult()
        for claim in graph.entities.get("Claim", {}).values():
            assumption = Assumption(
                id=new_id("assumption"),
                text="Methodological assumption: data is representative.",
                source_id=claim.source_id,
            )
            graph.add_entity(assumption)
            graph.add_relation(assumption.id, UNDERLIES, claim.id)
            result.created_entities.append(assumption.id)
            result.relations_added.append(f"{assumption.id}->{claim.id}")
        return result
