from __future__ import annotations

from ..ontology.graph import OntologyGraph
from ..ontology.models import Evidence
from ..ontology.relations import SUPPORTS
from ..utils.ids import new_id
from .base import AgentResult, BaseAgent


class EvidenceMapper(BaseAgent):
    name = "evidence_mapper"

    def run(self, graph: OntologyGraph, context: dict) -> AgentResult:
        result = AgentResult()
        for claim in graph.entities.get("Claim", {}).values():
            evidence = Evidence(
                id=new_id("evidence"),
                text=f"Stub evidence for claim: {claim.text}",
                evidence_type="empirical",
                source_id=claim.source_id,
                polarity=1,
            )
            graph.add_entity(evidence)
            graph.add_relation(evidence.id, SUPPORTS, claim.id)
            result.created_entities.append(evidence.id)
            result.relations_added.append(f"{evidence.id}->{claim.id}")
        return result
