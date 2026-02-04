from __future__ import annotations

from ..ontology.graph import OntologyGraph
from ..ontology.models import Argument
from ..utils.ids import new_id
from .base import AgentResult, BaseAgent


class ArgumentBuilder(BaseAgent):
    name = "argument_builder"

    def run(self, graph: OntologyGraph, context: dict) -> AgentResult:
        result = AgentResult()
        evidence_ids = list(graph.entities.get("Evidence", {}).keys())
        assumption_ids = list(graph.entities.get("Assumption", {}).keys())
        for claim in graph.entities.get("Claim", {}).values():
            argument = Argument(
                id=new_id("argument"),
                claim_id=claim.id,
                evidence_ids=evidence_ids,
                assumption_ids=assumption_ids,
            )
            graph.add_entity(argument)
            result.created_entities.append(argument.id)
        return result
