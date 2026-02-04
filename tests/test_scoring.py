from pathlib import Path

from logos_engine.ontology.graph import OntologyGraph
from logos_engine.ontology.models import Assumption, Claim, Evidence
from logos_engine.ontology.relations import CHALLENGES, SUPPORTS, UNDERLIES
from logos_engine.reasoning.scoring import compute_claim_confidence
from logos_engine.rules import builtin_rules
from logos_engine.rules.rulebook import Rulebook
from logos_engine.utils.ids import new_id


def _build_graph(with_assumption: bool) -> OntologyGraph:
    graph = OntologyGraph()
    claim = Claim(id=new_id("claim"), text="The system is reliable.")
    graph.add_entity(claim)

    supporting = Evidence(
        id=new_id("evidence"),
        text="Empirical study shows reliability.",
        evidence_type="empirical",
        polarity=1,
    )
    challenging = Evidence(
        id=new_id("evidence"),
        text="Anecdotal report suggests failure.",
        evidence_type="anecdotal",
        polarity=-1,
    )
    graph.add_entity(supporting)
    graph.add_entity(challenging)
    graph.add_relation(supporting.id, SUPPORTS, claim.id)
    graph.add_relation(challenging.id, CHALLENGES, claim.id)

    if with_assumption:
        assumption = Assumption(id=new_id("assumption"), text="Data is representative.")
        graph.add_entity(assumption)
        graph.add_relation(assumption.id, UNDERLIES, claim.id)

    return graph


def test_scoring_penalty_and_trace():
    rulebook = Rulebook.from_path(Path("config/rules.yaml"))
    graph_with = _build_graph(with_assumption=True)
    graph_without = _build_graph(with_assumption=False)

    score_with, trace_with = compute_claim_confidence(
        list(graph_with.entities["Claim"].keys())[0], graph_with, rulebook
    )
    score_without, _ = compute_claim_confidence(
        list(graph_without.entities["Claim"].keys())[0], graph_without, rulebook
    )

    assert 0.0 <= score_with <= 1.0
    assert score_with <= score_without
    assert any(step.rule_id == builtin_rules.CLAIM_CONFIDENCE for step in trace_with.steps)
