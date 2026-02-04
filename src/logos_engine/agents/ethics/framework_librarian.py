from __future__ import annotations

from ..base import AgentResult, BaseAgent


class FrameworkLibrarian(BaseAgent):
    name = "framework_librarian"

    def run(self, graph, context) -> AgentResult:  # type: ignore[override]
        return AgentResult()
