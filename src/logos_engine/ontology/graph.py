from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple, Type, Union

from .models import MODEL_REGISTRY, Argument, Assumption, Claim, Evidence, Source

Entity = Union[Source, Claim, Evidence, Assumption, Argument]


@dataclass
class OntologyGraph:
    entities: Dict[str, Dict[str, Entity]] = field(default_factory=lambda: defaultdict(dict))
    relations: List[Tuple[str, str, str]] = field(default_factory=list)

    def add_entity(self, entity: Entity) -> None:
        entity_type = type(entity).__name__
        self.entities[entity_type][entity.id] = entity

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        for entities in self.entities.values():
            if entity_id in entities:
                return entities[entity_id]
        return None

    def add_relation(self, src_id: str, relation: str, dst_id: str) -> None:
        self.relations.append((src_id, relation, dst_id))

    def get_relations(
        self,
        src_id: Optional[str] = None,
        relation: Optional[str] = None,
        dst_id: Optional[str] = None,
    ) -> List[Tuple[str, str, str]]:
        results = []
        for edge in self.relations:
            if src_id is not None and edge[0] != src_id:
                continue
            if relation is not None and edge[1] != relation:
                continue
            if dst_id is not None and edge[2] != dst_id:
                continue
            results.append(edge)
        return results

    def validate(self) -> List[str]:
        errors: List[str] = []
        known_ids = {entity.id for bucket in self.entities.values() for entity in bucket.values()}
        for src_id, _, dst_id in self.relations:
            if src_id not in known_ids:
                errors.append(f"Missing src id {src_id}")
            if dst_id not in known_ids:
                errors.append(f"Missing dst id {dst_id}")
        for entity in self.entities.get("Claim", {}).values():
            if entity.source_id and entity.source_id not in known_ids:
                errors.append(f"Claim {entity.id} missing source {entity.source_id}")
        for entity in self.entities.get("Evidence", {}).values():
            if entity.source_id and entity.source_id not in known_ids:
                errors.append(f"Evidence {entity.id} missing source {entity.source_id}")
        return errors

    def to_dict(self) -> Dict[str, List[Dict[str, object]]]:
        return {
            entity_type: [entity.to_dict() for entity in bucket.values()]
            for entity_type, bucket in self.entities.items()
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Iterable[Dict[str, object]]]) -> "OntologyGraph":
        graph = cls()
        for entity_type, entities in payload.items():
            model: Optional[Type[Entity]] = MODEL_REGISTRY.get(entity_type)
            if model is None:
                continue
            for item in entities:
                graph.add_entity(model.from_dict(item))
        return graph
