from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..ontology.graph import OntologyGraph
from .assumption_detector import AssumptionDetector
from .auditors import LogicAuditor
from .base import AgentResult, BaseAgent
from .claim_extractor import ClaimExtractor
from .document_ingestor import DocumentIngestor
from .evidence_mapper import EvidenceMapper
from .explanation_composer import ExplanationComposer
from .argument_builder import ArgumentBuilder


@dataclass
class Orchestrator(BaseAgent):
    name: str = "orchestrator"
    agents: List[BaseAgent] = field(
        default_factory=lambda: [
            DocumentIngestor(),
            ClaimExtractor(),
            EvidenceMapper(),
            AssumptionDetector(),
            ArgumentBuilder(),
            LogicAuditor(),
            ExplanationComposer(),
        ]
    )

    def run(self, graph: OntologyGraph, context: dict) -> AgentResult:
        result = AgentResult()
        for agent in self.agents:
            agent_result = agent.run(graph, context)
            result.created_entities.extend(agent_result.created_entities)
            result.updated_entities.extend(agent_result.updated_entities)
            result.relations_added.extend(agent_result.relations_added)
            result.uncertainty_markers.extend(agent_result.uncertainty_markers)
            result.notes_for_auditor.extend(agent_result.notes_for_auditor)
            result.traces.extend(agent_result.traces)
        return result
