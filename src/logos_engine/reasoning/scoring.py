from __future__ import annotations

import math
from typing import List, Tuple

from ..ontology.graph import OntologyGraph
from ..ontology.models import (
    Argument,
    Assumption,
    Claim,
    Evidence,
    ExplanationTrace,
    ReasoningStep,
    UncertaintyMarker,
)
from ..ontology.relations import CHALLENGES, SUPPORTS, UNDERLIES
from ..rules import builtin_rules
from ..rules.rulebook import Rulebook
from ..utils.clamp import clamp
from .trace import make_step, make_trace, make_uncertainty


def score_evidence_reliability(
    evidence: Evidence, rulebook: Rulebook
) -> Tuple[float, List[ReasoningStep], List[UncertaintyMarker]]:
    steps: List[ReasoningStep] = []
    uncertainties: List[UncertaintyMarker] = []
    baseline = rulebook.get_reliability_baseline(evidence.evidence_type)
    steps.append(
        make_step(
            builtin_rules.RELIABILITY_BASELINE,
            f"Reliability baseline for {evidence.evidence_type}",
            baseline,
            baseline,
        )
    )
    if evidence.evidence_type not in rulebook.evidence_reliability_baselines:
        uncertainties.append(
            make_uncertainty(evidence.id, f"Unknown evidence type {evidence.evidence_type}.", 0.3)
        )
    return clamp(baseline), steps, uncertainties


def score_evidence_relevance(
    evidence: Evidence, claim: Claim, rulebook: Rulebook
) -> Tuple[float, List[ReasoningStep], List[UncertaintyMarker]]:
    steps: List[ReasoningStep] = []
    uncertainties: List[UncertaintyMarker] = []
    constants = rulebook.get_constants()
    score = constants.get("relevance_baseline", 0.5)
    steps.append(
        make_step(
            builtin_rules.RELEVANCE_BASELINE,
            "Relevance baseline",
            score,
            score,
        )
    )
    claim_tokens = set(claim.text.lower().split())
    evidence_tokens = set(evidence.text.lower().split())
    for rule in rulebook.get_relevance_rules():
        rule_id = rule.get("id", "unknown")
        adjustment = float(rule.get("adjustment", 0.0))
        if rule_id == "rel.match.title" and claim_tokens.intersection(evidence_tokens):
            score += adjustment
            steps.append(make_step(rule_id, rule.get("description", "match"), adjustment, score))
        elif rule_id == "rel.scope.mismatch" and not claim_tokens.intersection(evidence_tokens):
            score += adjustment
            steps.append(make_step(rule_id, rule.get("description", "mismatch"), adjustment, score))
    return clamp(score), steps, uncertainties


def _net_confidence(support: float, challenge: float, k: float) -> float:
    return (support - challenge) / (support + challenge + k)


def compute_claim_confidence(
    claim_id: str, graph: OntologyGraph, rulebook: Rulebook
) -> Tuple[float, ExplanationTrace]:
    claim_entity = graph.get_entity(claim_id)
    if not isinstance(claim_entity, Claim):
        raise ValueError(f"Claim {claim_id} not found")
    constants = rulebook.get_constants()
    k = constants.get("k", 0.5)
    steps: List[ReasoningStep] = []
    uncertainties: List[UncertaintyMarker] = []

    support = 0.0
    challenge = 0.0
    evidence_count = 0
    for src_id, relation, dst_id in graph.get_relations(dst_id=claim_id):
        if relation not in {SUPPORTS, CHALLENGES}:
            continue
        evidence = graph.get_entity(src_id)
        if not isinstance(evidence, Evidence):
            continue
        reliability, rel_steps, rel_uncertainties = score_evidence_reliability(evidence, rulebook)
        relevance, relv_steps, relv_uncertainties = score_evidence_relevance(evidence, claim_entity, rulebook)
        steps.extend(rel_steps + relv_steps)
        uncertainties.extend(rel_uncertainties + relv_uncertainties)
        evidence_count += 1
        magnitude = reliability * relevance
        if relation == SUPPORTS:
            support += magnitude
        else:
            challenge += magnitude
    net = _net_confidence(support, challenge, k)
    normalized = (net + 1) / 2
    volume_factor = 1 - math.exp(-evidence_count)
    score = normalized * volume_factor
    steps.append(
        make_step(
            builtin_rules.CLAIM_CONFIDENCE,
            "Computed claim confidence",
            score,
            score,
        )
    )

    penalty = 0.0
    for src_id, relation, dst_id in graph.get_relations(dst_id=claim_id):
        if relation != UNDERLIES:
            continue
        assumption = graph.get_entity(src_id)
        if isinstance(assumption, Assumption):
            penalty += rulebook.get_assumption_penalties().get("default", 0.1)
    penalty_cap = constants.get("penalty_cap", 0.4)
    penalty = min(penalty, penalty_cap)
    if penalty:
        score = clamp(score - penalty)
        steps.append(
            make_step(
                builtin_rules.ASSUMPTION_PENALTY,
                "Applied assumption penalty",
                -penalty,
                score,
            )
        )
    return clamp(score), make_trace(claim_id, steps, uncertainties)


def compute_argument_strength(
    argument_id: str, graph: OntologyGraph, rulebook: Rulebook
) -> Tuple[float, ExplanationTrace]:
    argument = graph.get_entity(argument_id)
    if not isinstance(argument, Argument):
        raise ValueError(f"Argument {argument_id} not found")
    claim_confidence, trace = compute_claim_confidence(argument.claim_id, graph, rulebook)
    coherence_scores: List[float] = []
    for evidence_id in argument.evidence_ids:
        evidence = graph.get_entity(evidence_id)
        if not isinstance(evidence, Evidence):
            continue
        reliability, _, _ = score_evidence_reliability(evidence, rulebook)
        coherence_scores.append(reliability)
    coherence = sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0.0
    strength = clamp(0.7 * claim_confidence + 0.3 * coherence)
    trace.steps.append(
        make_step(
            builtin_rules.ARGUMENT_STRENGTH,
            "Computed argument strength",
            strength,
            strength,
        )
    )
    trace.subject_id = argument_id
    return strength, trace
