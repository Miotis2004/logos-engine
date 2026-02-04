from __future__ import annotations

from ..base import AgentResult, BaseAgent


class DilemmaStructurer(BaseAgent):
    name = "dilemma_structurer"

    def run(self, graph, context) -> AgentResult:  # type: ignore[override]
        return AgentResult()
