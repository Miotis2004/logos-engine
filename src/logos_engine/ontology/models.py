from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Type, TypeVar

Score = float

T = TypeVar("T")


def _asdict(value: Any) -> Any:
    if dataclass_is_instance(value):
        return asdict(value)
    if isinstance(value, list):
        return [_asdict(item) for item in value]
    return value


def dataclass_is_instance(value: Any) -> bool:
    return hasattr(value, "__dataclass_fields__")


@dataclass
class Span:
    span_id: str
    page: Optional[int] = None
    paragraph: Optional[int] = None
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class Source:
    id: str
    title: str
    source_type: str
    uri: Optional[str] = None
    summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class Claim:
    id: str
    text: str
    source_id: Optional[str] = None
    span: Optional[Span] = None
    confidence: Optional[Score] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.span:
            data["span"] = self.span.to_dict()
        return data

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        span = payload.get("span")
        if isinstance(span, dict):
            payload = dict(payload)
            payload["span"] = Span.from_dict(span)
        return cls(**payload)


@dataclass
class Evidence:
    id: str
    text: str
    evidence_type: str
    source_id: Optional[str] = None
    span: Optional[Span] = None
    reliability: Optional[Score] = None
    relevance: Optional[Score] = None
    polarity: int = 1

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.span:
            data["span"] = self.span.to_dict()
        return data

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        span = payload.get("span")
        if isinstance(span, dict):
            payload = dict(payload)
            payload["span"] = Span.from_dict(span)
        return cls(**payload)


@dataclass
class Assumption:
    id: str
    text: str
    source_id: Optional[str] = None
    span: Optional[Span] = None
    penalty: Optional[Score] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.span:
            data["span"] = self.span.to_dict()
        return data

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        span = payload.get("span")
        if isinstance(span, dict):
            payload = dict(payload)
            payload["span"] = Span.from_dict(span)
        return cls(**payload)


@dataclass
class Argument:
    id: str
    claim_id: str
    evidence_ids: List[str] = field(default_factory=list)
    assumption_ids: List[str] = field(default_factory=list)
    strength: Optional[Score] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class Value:
    id: str
    name: str
    description: Optional[str] = None
    weight: Optional[Score] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class Constraint:
    id: str
    name: str
    description: Optional[str] = None
    severity: Optional[Score] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class DecisionOption:
    id: str
    label: str
    description: Optional[str] = None
    score: Optional[Score] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class EthicalFramework:
    id: str
    name: str
    decision_rules: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class EthicalEvaluation:
    id: str
    framework_id: str
    option_id: str
    score: Optional[Score] = None
    rationale: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class ReasoningStep:
    id: str
    rule_id: str
    description: str
    delta: float
    resulting_score: Optional[Score] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class UncertaintyMarker:
    id: str
    subject_id: str
    note: str
    severity: Optional[Score] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        return cls(**payload)


@dataclass
class ExplanationTrace:
    id: str
    subject_id: str
    steps: List[ReasoningStep] = field(default_factory=list)
    uncertainty_markers: List[UncertaintyMarker] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "subject_id": self.subject_id,
            "steps": [_asdict(step) for step in self.steps],
            "uncertainty_markers": [_asdict(marker) for marker in self.uncertainty_markers],
        }

    @classmethod
    def from_dict(cls: Type[T], payload: Dict[str, Any]) -> T:
        steps = [ReasoningStep.from_dict(item) for item in payload.get("steps", [])]
        markers = [UncertaintyMarker.from_dict(item) for item in payload.get("uncertainty_markers", [])]
        return cls(
            id=payload["id"],
            subject_id=payload["subject_id"],
            steps=steps,
            uncertainty_markers=markers,
        )


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
