from __future__ import annotations

from ..ontology.graph import OntologyGraph
from ..ontology.models import Claim
from ..utils.ids import new_id
from ..utils.text import extract_claims
from .base import AgentResult, BaseAgent


class ClaimExtractor(BaseAgent):
    name = "claim_extractor"

    def run(self, graph: OntologyGraph, context: dict) -> AgentResult:
        result = AgentResult()
        text = context.get("document_text", "")
        source_id = context.get("source_id")
        for claim_text in extract_claims(text):
            claim = Claim(id=new_id("claim"), text=claim_text, source_id=source_id)
            graph.add_entity(claim)
            result.created_entities.append(claim.id)
        return result
