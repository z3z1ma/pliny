Status: active
Created: 2026-06-23
Updated: 2026-06-27

# 10x Autoresearch Loop Specification

## Purpose And Scope

This specification defines the 10x autoresearch loop: a simple scientific
environment for proving and improving `SKILL.md` through live subject-agent
trials.

The loop has two simultaneous purposes:

- test a registered hypothesis about current or candidate 10x behavior;
- grow a reusable evaluation and regression suite that proves the accepted skill
  still works.

The LLM reasoning engine is the scientist. It designs the experiment, registers
the hypothesis, runs clean-room trials through subject agents or subprocesses,
inspects the artifacts, and records the verdict. Python utilities support that
scientist by running one registered trial, preserving artifacts, validating
static contracts, and rendering reports. Python utilities do not own the loop,
invent verdicts, promote candidates, or hide scientific judgment behind a single
aggregate.

This spec covers:

- the required experiment contract;
- live-trial runner behavior;
- records and artifact preservation;
- controls, arms, repetitions, and method tiers;
- inspection, verdict, and promotion boundaries;
- failure modes the loop must reveal instead of rewarding.

This spec does not require static canned-output packs, answer keys, numeric
transcript grading, or automatic promotion.

## Related Records

- Active decision:
  `.10x/decisions/autoresearch-live-trial-scientist-inspection.md`
- Current protocol under test: `SKILL.md`
- Human program: `autoresearch/program.md`
- Tooling README: `autoresearch/README.md`
- Trial seeds: `autoresearch/trial-seeds/`

## Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY are normative
and use their RFC 2119 meanings.

When this spec says "the loop", it means the whole autoresearch process:
records, experiment definitions, trial execution, artifacts, inspection,
verdicts, and promotion boundaries. It does not imply any specific daemon or
autonomous Python controller.

## Operating Model

The loop is scientist-led and tool-assisted.

The scientist MUST:

- state a question or hypothesis before execution;
- choose the cheapest method tier that can honestly answer the question;
- define the exact arms to run;
- define the scenario and workspace procedure;
- inspect raw artifacts before recording a verdict;
- preserve negative, null, surprising, and confounded results.

The runner MUST:

- run exactly the registered experiment definition it was given;
- preserve the plan, command metadata, prompts, raw artifacts, workspace
  manifests, archived workspaces, summaries, and reports;
- refuse ambiguous or obsolete definition shapes;
- leave canonical `SKILL.md` and `autoresearch/program.md` guarded.

The runner MUST NOT:

- infer hidden arms;
- run an unregistered trial;
- decide whether a candidate is promoted;
- replace scientist inspection with canned output checks.

## Core Records

Durable truth lives in `.10x/`. Raw artifacts that support claims live under
`.10x/evidence/.storage/`. Exploratory source material that is not claim support
lives under `.10x/research/.storage/`.

The loop uses these record categories:

- Research: experiment design, findings, tradeoffs, rejected paths, and
  follow-up hypotheses.
- Evidence: observed outputs, command results, summaries, reports, raw artifact
  references, and inspection notes.
- Reviews: adversarial assessment of experiments, candidates, reports, or
  promotion claims.
- Decisions: durable choices about policy, promotion, budget, or canonical
  instruction changes.
- Tickets: bounded implementation or experiment execution work.
- Knowledge and skills: stable lessons and reusable procedures.

## Experiment Definition

Every MICRO or FULL run MUST have exactly one registered experiment definition
before execution. The definition MAY be embedded in a research record or stored
as local JSON, but it MUST be durable enough for a future scientist to rerun or
audit.

An experiment definition MUST include:

- `experiment_id`;
- `method_tier`;
- `model`;
- `harness`;
- `repetitions`;
- `arms`;
- `scenarios`;
- `budget`;
- `scientific_contract`.

The `scientific_contract` MUST include:

- `question`;
- `hypothesis`;
- `expected_behavior`;
- `inspection_criteria`;
- `quality_floor`;
- `verdict_record_path`.

The scientific contract is the pre-registration. It tells the future reader
what the run was meant to prove, what behavior should appear, what observations
matter, which floor would make the result unacceptable, and where the final
scientist verdict will be recorded.

## Arms

The `arms` array is exact. It is the complete ordered list of subject variants
the runner must execute.

Comparative experiments SHOULD list controls and candidates explicitly, for
example `no-10x-control`, `current-10x`, and `candidate-variant`.

Current-skill regression or smoke experiments SHOULD list one arm, usually
`current-10x`. No extra mode flag is required for a one-arm run.

The runner MUST reject obsolete definition fields that imply hidden arm
selection or static evaluation.

## Scenarios And Workspaces

Each scenario MUST provide either:

- a `prompt` or `prompts_by_arm`; and
- a `prior_raw_path`, `prior_raw_paths`, or `workspace_procedure`.

Trial seed workspaces under `autoresearch/trial-seeds/` are starting states for
live trials. They are not answer keys. `autoresearch/trial-seeds/index.json` is
the seed selection registry and MUST describe each seed's scenario, target
rubrics, conditions, traps, material records, material source files, raw path,
workspace manifest, and workspace procedure. The runner copies a seed workspace
into a private temporary workspace, runs the subject, then archives the
resulting workspace under the experiment output directory.

Continuation scenarios MUST point at prior raw artifacts with `prior_raw_path`
or `prior_raw_paths`. The scientist decides the next user message after reading
the transcript. Fixed arrays of prewritten follow-ups are not part of the active
method.

## Method Tiers

MINE, MICRO, and FULL are method tiers.

- MINE is source inspection, record review, or lightweight planning without a
  subject-agent run.
- MICRO is a narrow live trial that isolates one behavior or failure mode.
- FULL is broader live trial coverage across multiple scenarios, arms, or
  repetitions.

The scientist SHOULD use MINE before MICRO and MICRO before FULL whenever the
cheaper tier can honestly answer the question.

MICRO and FULL are scenario breadth tiers. Both MAY execute the same live
subject harness.

## Runner Contract

`autoresearch/run_once.py` MUST run exactly one registered MICRO or FULL trial.
It delegates live subject execution to `autoresearch/run_codex_subject.py` and
renders a report unless asked otherwise.

A successful run writes, at minimum:

- `plan.json`;
- `summary.json`;
- `raw/*.json`;
- command metadata and process output under `codex/`;
- prompt artifacts under `prompts/`;
- workspace manifests and archived workspaces under `workspaces/`;
- `canonical_guard.json`;
- `report.md` when reporting is enabled.

The report is a secondary view. It MUST make the scientific contract, arm and
scenario coverage, command results, raw artifact references, changed files, and
archived workspace paths easy to inspect. It MUST NOT be treated as the verdict
itself.

## Inspection And Verdicts

The scientist records the verdict in `.10x/`, using direct references to raw
artifacts and reports.

Verdicts MAY include:

- confirmed;
- refuted;
- backfired;
- inconclusive;
- already optimal;
- confounded;
- candidate;
- promoted;
- cancelled;
- regression-pass.

Promotion is separate from verdict. A candidate can be promising or confirmed
without being promotion-ready.

Promotion of canonical `SKILL.md`, accepted decisions, active specifications,
or release artifacts requires explicit human approval unless a future accepted
decision delegates that authority.

## Requirements

### REQ-001 Durable Local Index

The loop MUST keep durable truth in `.10x/`, with raw claim-supporting artifacts
under `.10x/evidence/.storage/`.

### REQ-002 Registered Scientific Contract

Each MICRO or FULL run MUST pre-register its question, hypothesis, expected
behavior, inspection criteria, quality floor, and verdict record path.

### REQ-003 Cheapest Honest Tier

The scientist SHOULD choose the cheapest tier that can honestly answer the
registered question.

### REQ-004 Visible Rubric Criteria

Each experiment MUST declare the criteria used for inspection. Criteria MAY
reference score IDs, but the verdict MUST remain grounded in observed behavior.

### REQ-005 Component Judgments Visible

Reports and verdict records MUST expose important component observations instead
of hiding them behind one final label.

### REQ-006 Quality Floors

Experiments MUST name any floor that would make an apparent win unacceptable,
such as unsafe writes, missing evidence, scope narrowing, or excess complexity.

### REQ-007 Explicit Arms And Controls

The registered `arms` array MUST be the exact ordered run list. Controls,
baselines, current skill runs, and candidates MUST be explicit.

### REQ-008 Repetition And Variance

The definition MUST state repetition count. Single-run results SHOULD be labeled
preliminary unless the registered question only needs a smoke or regression
check.

### REQ-009 Judgment Trust And Limits

Any delegated or automated judgment aid MUST declare its limits. Scientist
inspection remains required for promotion-supporting claims unless an accepted
decision says otherwise.

### REQ-010 Manual Inspection

Manual inspection MUST compare actual subject behavior to the registered
criteria and scenario intent, not to quoted instructions or templates.

### REQ-011 Seed State Provenance

Each run MUST preserve enough seed, prompt, prior raw artifact, and workspace
manifest information to explain what state the subject saw.

The seed registry MUST cover every checked-in trial seed with enough metadata
for a fresh scientist to choose an appropriate seed without directory
archaeology.

### REQ-012 Raw Artifact Preservation

Raw transcripts, command metadata, prompts, process output, manifests, summaries,
reports, and archived workspaces MUST be preserved for claim-supporting runs.

### REQ-013 Negative Result Preservation

Null, negative, surprising, confounded, and backfiring results MUST be recorded
when they affect research direction or future evaluation quality.

### REQ-014 Promotion Separation

Verdict, candidate retention, and canonical promotion MUST remain separate
decisions.

### REQ-015 Human Authority

Canonical instruction changes and governance changes MUST require explicit human
approval unless already delegated by an accepted decision.

### REQ-016 Safe Autonomy

Autonomous runs MUST have bounded write paths, budgets, stop conditions, and
artifact destinations.

### REQ-017 Privacy And Secret Handling

The loop MUST avoid preserving secrets in durable records. Redactions MUST keep
enough context for audit without exposing private data.

### REQ-018 Gaming Resistance

Experiments MUST detect attempts to win by echoing templates, narrowing scope,
weakening evidence, or exploiting seed state instead of improving behavior.

### REQ-019 Scenario Coverage

The reusable suite SHOULD cover the major 10x behavior surfaces: ambiguity,
records, evidence, tickets, closure, minimalism, skill authoring, and research
method discipline.

### REQ-020 Evidence-Gated Closure

No experiment, ticket, or promotion claim SHOULD be closed without evidence that
matches the claim being made.

### REQ-021 Cost Subordination

Cost and speed matter, but they are subordinate to correctness, evidence
integrity, and honest confidence.

### REQ-022 Delegated Judgment Before Trust

Delegated judgment aids MAY help triage, but promotion-supporting authority
requires repeated evidence, documented limits, adversarial review, and an
accepted decision.

## Rubric Catalog

The score catalog uses stable IDs `S001` through `S009` as rubric labels. These
IDs help future experiments talk about the same behavior surfaces. They do not
require the active runner to emit numeric grades.

The active rubric surfaces are:

- S001: outer-loop ambiguity handling;
- S002: source and answerability discipline;
- S003: durable record retrieval and use;
- S004: evidence integrity;
- S005: ticket decomposition and follow-up hygiene;
- S006: active-record authority and conflict handling;
- S007: implementation minimalism;
- S008: autoresearch method discipline;
- S009: closure coherence.

## Scenario Catalog

The scenario catalog uses stable IDs `SCN-001` through `SCN-015`. Scenarios are
clean-room situations for live subject-agent trials and reusable regression
coverage. They are not answer keys.

## Anti-Goals

The active loop MUST NOT reintroduce:

- static pass/fail answer packs as the main evaluation method;
- hidden default arms;
- unregistered continuation scripts;
- automatic promotion;
- reports that omit durable archived workspaces;
- artifact summaries that force the scientist to guess the hypothesis or floor.

## Acceptance Criteria

The active tooling satisfies this spec when:

- `python3 autoresearch/validate.py` passes;
- unit tests for the runner and report pass;
- a one-arm current-skill smoke run can be registered without special mode
  flags;
- a comparative run can be registered by listing each arm explicitly;
- each report exposes the scientific contract and archived workspace paths;
- old static-evaluation-only paths are absent from the active
  tooling surface.
