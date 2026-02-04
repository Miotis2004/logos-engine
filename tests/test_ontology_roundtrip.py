from pathlib import Path

from logos_engine.ontology.graph import OntologyGraph
from logos_engine.ontology.models import Claim
from logos_engine.storage.json_graph_store import load_graph, save_graph
from logos_engine.utils.ids import new_id


def test_graph_roundtrip(tmp_path):
    graph = OntologyGraph()
    claim = Claim(id=new_id("claim"), text="Test claim.")
    graph.add_entity(claim)

    path = tmp_path / "graph.json"
    save_graph(graph, path)
    loaded = load_graph(path)

    assert loaded.get_entity(claim.id) is not None
