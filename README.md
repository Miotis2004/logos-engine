# logos-engine

Local Agentic Platform for Academic Argument Evaluation & Ethical Decision Reasoning
Overview

This project is a local, explainable AI platform designed to evaluate academic arguments and reason through ethical decision scenarios using agentic workflows and symbolic logic.

The system combines:

Local large language models (LLMs) for bounded extraction and hypothesis generation

A symbolic ontology for claims, evidence, assumptions, and values

Deterministic scoring rules for argument strength and ethical evaluation

Full explanation traces for transparency and auditability

All processing occurs entirely on the local machine. The platform is domain-agnostic and does not perform prediction, optimization, or real-world decision execution.

Important Disclaimer

This project is an independent engineering prototype intended to explore local agentic AI architectures and symbolic reasoning mechanisms for academic argument evaluation and ethical decision analysis.

It is not part of any approved doctoral research study, does not involve applied forecasting, and does not target smart city, infrastructure, or operational decision-making domains.

Core Capabilities
1. Academic Argument Evaluation

Extracts claims from scholarly text

Maps supporting and challenging evidence

Identifies explicit and implicit assumptions

Computes conservative confidence estimates

Produces structured argument maps

Surfaces uncertainty explicitly

2. Ethical Decision Reasoning

Structures ethical dilemmas into decision options

Applies multiple ethical frameworks symbolically

Evaluates trade-offs without issuing recommendations

Produces framework-relative justifications

Highlights value conflicts and constraints

3. Explainability by Design

Every score change is rule-based

Every conclusion has a traceable reasoning chain

No opaque confidence scores

No hidden model decisions

Design Philosophy

LLMs propose, symbols decide
Language models generate candidates; symbolic rules evaluate them.

Transparency over performance
Interpretability is prioritized over aggressive scoring.

Conservative confidence
Missing evidence and hidden assumptions reduce confidence.

Local-first
No cloud APIs, no data leakage.

System Architecture
High-Level Layers

User Interface

Document upload

Argument and decision visualization

Explanation trace inspection

Agent Orchestration Layer

Role-bounded agents

Deterministic execution order

Hard guardrails on agent authority

Reasoning & Scoring Layer

Symbolic rules for evidence, assumptions, and coherence

Ethical framework rule engines

Audit and consistency checks

Knowledge & Ontology Layer

Claims, evidence, assumptions, values

Explicit relationships and provenance

Storage Layer

Local JSON graph

SQLite indexing

Append-only reasoning logs

Ontology Summary
Core Entities

Claim – Declarative statement under evaluation

Evidence – Support or challenge for a claim

Assumption – Required premise for a claim

Source – Origin of information

Argument – Structured grouping of claims and support

Ethical Entities

Value – Moral or social principle

EthicalFramework – Rule-based ethical model

Constraint – Legal, practical, or ethical limitation

DecisionOption – Possible course of action

EthicalEvaluation – Framework-specific assessment

Explainability Entities

ReasoningStep – Atomic inference

ExplanationTrace – Ordered reasoning chain

UncertaintyMarker – Explicit uncertainty annotation

Agent Roles
Agent	Responsibility
Orchestrator	Controls workflow and enforces constraints
Document Ingestor	Chunks text and creates sources
Claim Extractor	Identifies candidate claims
Evidence Mapper	Links evidence with polarity
Assumption Detector	Finds explicit and implicit assumptions
Argument Builder	Structures arguments
Counterargument Generator	Produces hypothetical challenges
Dilemma Structurer	Builds ethical decision structures
Framework Librarian	Provides ethical rule sets
Ethical Evaluator	Applies frameworks symbolically
Logic Auditor	Validates consistency and scoring
Citation Auditor	Ensures provenance integrity
Explanation Composer	Generates user-facing explanations

Agents never issue final conclusions independently.

Symbolic Scoring Model (Summary)
Evidence

Reliability and relevance scored independently

Rule-based adjustments only

Supports and challenges treated symmetrically

Assumptions

Penalize hidden assumptions

Penalize unsupported premises

Cap total penalty to avoid collapse

Claims

Evidence balance normalized

Evidence volume limits confidence inflation

Explicit uncertainty markers added

Arguments

Primary claim dominates

Coherence matters but cannot override weak evidence

All scoring decisions generate traceable reasoning steps.

What This System Does Not Do

No prediction or forecasting

No optimization or recommendations

No real-time decision execution

No applied policy analysis

No domain-specific infrastructure modeling

Repository Structure
/src
  /agents
  /ontology
  /rules
  /reasoning
  /audit
  /ui

/data
  /documents
  /synthetic_cases

/config
  rules.yaml
  frameworks.yaml

/logs
  reasoning_traces/

README.md
LICENSE

Setup (Planned)

This repository is designed to run fully locally.

Expected stack (subject to implementation phase):

Python 3.11+

Local LLM runtime (e.g., llama.cpp / Ollama)

SQLite

Optional desktop UI framework

Detailed setup instructions will be added once the initial implementation phase begins.

Usage (Conceptual)

Load academic documents or ethical scenarios

Select evaluation mode (Argument or Ethics)

Run agent pipeline

Inspect:

Argument maps

Ethical framework comparisons

Explanation traces

Uncertainty markers

No outputs are presented without provenance.

Status

Current Phase: Architecture and design finalized
Next Phase: Implementation of ontology, scoring engine, and minimal agent pipeline

License

License to be determined.
Recommended: permissive license for code, separate notice for datasets.

Roadmap (High Level)

v0.1: Ontology + scoring engine

v0.2: Academic argument pipeline

v0.3: Ethical reasoning pipeline

v0.4: Visualization and trace inspection

v1.0: Stable local platform

Final Notes

This project is intentionally conservative, explainable, and bounded.
Its value lies in how reasoning is performed, not in producing answers faster or louder than existing tools.
