from pathlib import Path

from logos_engine.rules.rulebook import Rulebook


def test_rulebook_loads():
    rulebook = Rulebook.from_path(Path("config/rules.yaml"))
    assert "empirical" in rulebook.evidence_reliability_baselines
    assert rulebook.get_constants()["k"] > 0
