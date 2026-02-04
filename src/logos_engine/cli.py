from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .agents.orchestrator import Orchestrator
from .config.settings import Settings
from .ontology.graph import OntologyGraph
from .reasoning.scoring import compute_argument_strength, compute_claim_confidence
from .reasoning.trace import TraceLogger
from .rules.rulebook import Rulebook
from .storage.audit_log import AuditLog


console = Console()


def cmd_init() -> None:
    settings = Settings()
    settings.ensure_dirs()
    console.print("Initialized data/ and logs/ directories.")


def cmd_ingest(path: str) -> None:
    settings = Settings()
    settings.ensure_dirs()
    graph = OntologyGraph()
    orchestrator = Orchestrator()
    context = {"path": path}
    orchestrator.run(graph, context)
    console.print(f"Ingested source {context.get('source_id')}")


def _print_claims(graph: OntologyGraph, rulebook: Rulebook, logger: TraceLogger) -> None:
    table = Table(title="Claim Confidence")
    table.add_column("Claim ID")
    table.add_column("Text")
    table.add_column("Confidence")
    for claim in graph.entities.get("Claim", {}).values():
        confidence, trace = compute_claim_confidence(claim.id, graph, rulebook)
        logger.add_trace(trace)
        table.add_row(claim.id, claim.text, f"{confidence:.2f}")
    console.print(table)


def cmd_evaluate_argument(doc_id: str) -> None:
    settings = Settings()
    settings.ensure_dirs()
    graph = OntologyGraph()
    orchestrator = Orchestrator()
    context = {"path": doc_id}
    orchestrator.run(graph, context)

    rulebook = Rulebook.from_path(settings.config_dir / "rules.yaml")
    logger = TraceLogger(settings.logs_dir / "reasoning_traces")
    _print_claims(graph, rulebook, logger)

    for argument in graph.entities.get("Argument", {}).values():
        strength, trace = compute_argument_strength(argument.id, graph, rulebook)
        logger.add_trace(trace)
        console.print(f"Argument {argument.id} strength: {strength:.2f}")
        break

    exported = logger.export()
    audit = AuditLog(settings.logs_dir / "audit_log.jsonl")
    for path in exported:
        audit.append({"event": "trace_export", "path": str(path)})
    if exported:
        console.print(f"Trace saved to {exported[0]}")


def cmd_evaluate_ethics(scenario_file: str) -> None:
    settings = Settings()
    settings.ensure_dirs()
    console.print(
        f"Ethics evaluation stub for {scenario_file}. Framework reasoning to be implemented.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="logos-engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init")

    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("path")

    eval_parser = subparsers.add_parser("evaluate-argument")
    eval_parser.add_argument("doc_id")

    ethics_parser = subparsers.add_parser("evaluate-ethics")
    ethics_parser.add_argument("scenario_file")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "ingest":
        cmd_ingest(args.path)
    elif args.command == "evaluate-argument":
        cmd_evaluate_argument(args.doc_id)
    elif args.command == "evaluate-ethics":
        cmd_evaluate_ethics(args.scenario_file)


if __name__ == "__main__":
    main()
