from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from ..ontology.graph import OntologyGraph


def save_graph(graph: OntologyGraph, path: Path) -> None:
    payload: Dict[str, Any] = {
        "entities": graph.to_dict(),
        "relations": graph.relations,
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def load_graph(path: Path) -> OntologyGraph:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    graph = OntologyGraph.from_dict(payload.get("entities", {}))
    graph.relations = [tuple(edge) for edge in payload.get("relations", [])]
    return graph
