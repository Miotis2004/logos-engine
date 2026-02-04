from __future__ import annotations

from ..base import AgentResult, BaseAgent


class EthicalEvaluator(BaseAgent):
    name = "ethical_evaluator"

    def run(self, graph, context) -> AgentResult:  # type: ignore[override]
        return AgentResult()
