from __future__ import annotations

from pathlib import Path

from ..ontology.graph import OntologyGraph
from ..ontology.models import Source
from ..utils.ids import new_id
from .base import AgentResult, BaseAgent


class DocumentIngestor(BaseAgent):
    name = "document_ingestor"

    def run(self, graph: OntologyGraph, context: dict) -> AgentResult:
        result = AgentResult()
        path = Path(context.get("path", ""))
        text = ""
        if path.exists():
            text = path.read_text(encoding="utf-8")
        source = Source(
            id=new_id("source"),
            title=path.name or "untitled",
            source_type="local_document",
            uri=str(path) if path else None,
            summary=text[:200] if text else None,
        )
        graph.add_entity(source)
        context["source_id"] = source.id
        context["document_text"] = text
        result.created_entities.append(source.id)
        return result
