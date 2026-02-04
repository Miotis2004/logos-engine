from logos_engine.reasoning.trace import TraceLogger, make_trace
from logos_engine.reasoning.trace import make_step, make_uncertainty


def test_trace_export(tmp_path):
    logger = TraceLogger(tmp_path)
    step = make_step("rule", "desc", 0.1, 0.2)
    uncertainty = make_uncertainty("subject", "note", 0.5)
    trace = make_trace("subject", [step], [uncertainty])
    logger.add_trace(trace)
    exported = logger.export()
    assert exported
    assert exported[0].exists()
