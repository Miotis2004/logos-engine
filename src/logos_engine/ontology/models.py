from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, confloat

Score = confloat(ge=0.0, le=1.0)


class Span(BaseModel):
    span_id: str
    page: Optional[int] = None
    paragraph: Optional[int] = None
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None


class Source(BaseModel):
    id: str
    title: str
    source_type: str
    uri: Optional[str] = None
    summary: Optional[str] = None


class Claim(BaseModel):
    id: str
    text: str
    source_id: Optional[str] = None
    span: Optional[Span] = None
    confidence: Optional[Score] = None


class Evidence(BaseModel):
    id: str
    text: str
    evidence_type: str
    source_id: Optional[str] = None
    span: Optional[Span] = None
    reliability: Optional[Score] = None
    relevance: Optional[Score] = None
    polarity: int = Field(default=1, description="1 for supporting, -1 for challenging")


class Assumption(BaseModel):
    id: str
    text: str
    source_id: Optional[str] = None
    span: Optional[Span] = None
    penalty: Optional[Score] = None


class Argument(BaseModel):
    id: str
    claim_id: str
    evidence_ids: List[str] = Field(default_factory=list)
    assumption_ids: List[str] = Field(default_factory=list)
    strength: Optional[Score] = None


class Value(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    weight: Optional[Score] = None


class Constraint(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    severity: Optional[Score] = None


class DecisionOption(BaseModel):
    id: str
    label: str
    description: Optional[str] = None
    score: Optional[Score] = None


class EthicalFramework(BaseModel):
    id: str
    name: str
    decision_rules: List[Dict[str, Any]] = Field(default_factory=list)


class EthicalEvaluation(BaseModel):
    id: str
    framework_id: str
    option_id: str
    score: Optional[Score] = None
    rationale: Optional[str] = None


class ReasoningStep(BaseModel):
    id: str
    rule_id: str
    description: str
    delta: float
    resulting_score: Optional[Score] = None


class ExplanationTrace(BaseModel):
    id: str
    subject_id: str
    steps: List[ReasoningStep] = Field(default_factory=list)
    uncertainty_markers: List["UncertaintyMarker"] = Field(default_factory=list)


class UncertaintyMarker(BaseModel):
    id: str
    subject_id: str
    note: str
    severity: Optional[Score] = None


MODEL_REGISTRY = {
    "Source": Source,
    "Claim": Claim,
    "Evidence": Evidence,
    "Assumption": Assumption,
    "Argument": Argument,
    "Value": Value,
    "Constraint": Constraint,
    "DecisionOption": DecisionOption,
    "EthicalFramework": EthicalFramework,
    "EthicalEvaluation": EthicalEvaluation,
    "ReasoningStep": ReasoningStep,
    "ExplanationTrace": ExplanationTrace,
    "UncertaintyMarker": UncertaintyMarker,
}

ExplanationTrace.model_rebuild()
