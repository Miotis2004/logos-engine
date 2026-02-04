# Logos Engine

Local Agentic Platform for Academic Argument Evaluation & Ethical Decision Reasoning.

## Overview

Logos Engine is a local-first, explainable prototype for evaluating academic arguments and
structuring ethical decision reasoning. It provides:

- A typed ontology for claims, evidence, assumptions, values, and ethical constructs.
- A deterministic scoring engine with traceable reasoning steps.
- A lightweight agent orchestration pipeline (LLM-free in v0.1).
- Local storage utilities and audit logging.
- A minimal CLI for initialization, ingestion, and evaluation.

The project avoids cloud APIs and paid services. All computation is local and deterministic.

## Repository Structure

```
src/logos_engine/
  agents/            # Agent interfaces and orchestrator
  config/            # Settings helpers
  ontology/          # Models, relations, in-memory graph
  reasoning/         # Scoring + reasoning trace utilities
  rules/             # Rulebook loader and builtin rule IDs
  storage/           # JSON graph store, audit log, sqlite stub
  utils/             # IDs, text helpers, clamp
config/
  rules.yaml         # Rulebook configuration
  frameworks.yaml    # Ethical framework placeholders
logs/
  reasoning_traces/  # Trace outputs (JSON)
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## CLI Usage

```bash
logos-engine init
logos-engine ingest path/to/document.txt
logos-engine evaluate-argument path/to/document.txt
logos-engine evaluate-ethics path/to/scenario.yaml
```

- `init` creates local `data/` and `logs/` directories.
- `ingest` registers a source and extracts stub claims.
- `evaluate-argument` runs the agent pipeline, scores claims, and emits reasoning traces.
- `evaluate-ethics` is a stub for future expansion.

## Testing

```bash
ruff check src tests
mypy src
pytest
```

## Design Notes

- Scoring is deterministic and rule-based; each adjustment produces a reasoning step.
- Traces are exported to `logs/reasoning_traces/` for auditability.
- No external API keys are required.

## License

MIT License. See [LICENSE](LICENSE).
