Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/specs/10x-autoresearch-loop.md, .10x/evidence/2026-06-23-autoresearch-micro-runner.md, .10x/evidence/2026-06-23-autoresearch-codex-full-harness.md, .10x/evidence/2026-06-23-autoresearch-reporting.md

# Simplify Autoresearch Around Program-Owned Loop

## Scope

Correct the autoresearch architecture so it follows the Karpathy-style model:
a human-owned `program.md` tells the LLM researcher how to run the loop, while
repository tooling runs exactly one experiment iteration and emits scores. The
LLM reasoning engine, not Python state-management code, owns the loop,
mutation decisions, branching, keep/discard decisions, and indefinite
continuation.

Included:

- Add a human-owned `autoresearch/program.md` that is read by the LLM researcher
  and is not edited by the LLM during research runs.
- Make `program.md` define the autonomous research protocol:
  - establish baseline;
  - mutate only candidate instruction artifacts, not canonical `SKILL.md`;
  - run exactly one MICRO or FULL experiment at a time;
  - extract numeric scores;
  - append a simple result ledger;
  - keep, discard, branch, or mutate based on score vectors and simplicity;
  - continue until manually interrupted.
- Add a one-shot `autoresearch/run_once.py` wrapper that runs exactly one
  registered MICRO or FULL experiment and writes score artifacts plus an optional
  report. It must not maintain resumable loop state, event logs, stop files, or
  candidate-generation state.
- Preserve useful existing components:
  - score and scenario catalogs;
  - offline scorer;
  - MICRO fixture runner;
  - FULL Codex fixture-smoke runner;
  - report generator and campaign metadata rendering;
  - scorer calibration diagnostics;
  - Codex isolation battery as an optional diagnostic.
- Delete Python-owned loop/controller artifacts:
  - `autoresearch/run_loop.py`;
  - `autoresearch/run_codex_candidate.py`;
  - `autoresearch/templates/long-run-loop.json`;
  - `autoresearch/templates/long-run-live-candidates.json`;
  - tests dedicated to those deleted modules.
- Remove README guidance that presents Python as the autonomous loop controller
  and replace it with `program.md` plus `run_once.py` guidance.
- Delete or replace stale long-run readiness records created by the prior
  overbuilt direction so future agents do not treat that architecture as the
  accepted plan.
- Update affected tickets whose parent pointed at the deleted long-run readiness
  ticket.
- Record evidence and review for the simplification.

Excluded:

- Rewriting the scorer catalog or scenario catalog.
- Deleting MICRO/FULL runners, report generation, scorer calibration, or Codex
  isolation diagnostics.
- Changing canonical `SKILL.md`.
- Implementing live subject-agent evaluation beyond the existing FULL
  fixture-smoke slice.
- Building dashboards, schedulers, daemons, resumable controllers, or queue
  systems.
- Automatically promoting any candidate into canonical 10x instructions.

## Architectural Constraint

The core loop is a prompt/program discipline, not an application loop. If a
future researcher needs to run forever, the LLM should repeatedly:

1. read `autoresearch/program.md`;
2. make or adjust a candidate artifact;
3. run one experiment through `autoresearch/run_once.py`;
4. read the scores/report/logs;
5. decide the next candidate or revert/keep action;
6. repeat.

Python utilities may produce scores, reports, validation, and diagnostics. They
must not own autonomous research strategy or long-running control flow.

## Acceptance Criteria

- AC-001: `autoresearch/program.md` exists and explicitly states that it is the
  human-owned research program; autoresearch agents read it but do not edit it
  unless a human specifically requests a program change.
- AC-002: `program.md` contains a concrete autonomous loop protocol with setup,
  editable/non-editable surfaces, MICRO/FULL usage, score extraction, results
  ledger, keep/discard/revert guidance, simplicity tradeoff guidance, and
  indefinite continuation until human interruption.
- AC-003: `autoresearch/run_once.py` exists, accepts a registered experiment,
  runs exactly one MICRO or FULL iteration through existing runners, writes
  artifacts under a caller-provided output directory, optionally writes a report,
  prints a JSON summary, and performs no loop/state/resume/event orchestration.
- AC-004: `run_once.py` refuses unsupported tiers and invalid mode combinations
  with clear non-zero CLI errors.
- AC-005: `autoresearch/run_loop.py`, `autoresearch/run_codex_candidate.py`,
  `autoresearch/templates/long-run-loop.json`,
  `autoresearch/templates/long-run-live-candidates.json`,
  `autoresearch/tests/test_run_loop.py`, and
  `autoresearch/tests/test_run_codex_candidate.py` are deleted.
- AC-006: README no longer documents `run_loop.py`, live candidate-generation
  controllers, resumable state, stop files, or Python-owned long-running loops
  as the core path.
- AC-007: README documents `program.md` and `run_once.py` as the core
  autoresearch usage path.
- AC-008: Useful support files remain available and tested:
  `offline_score.py`, `run_micro.py`, `run_full_codex.py`, `report.py`,
  `calibrate_scorer.py`, and `run_codex_isolation.py`.
- AC-009: Stale long-run readiness records and reviews created by the overbuilt
  controller direction are deleted or superseded so no active/done record still
  claims Python-owned loop readiness as the accepted architecture.
- AC-010: Existing completed follow-up tickets that pointed at the deleted
  long-run readiness parent are repaired so their `Parent:` headers do not point
  at a deleted record.
- AC-011: Unit tests cover `run_once.py` MICRO execution, FULL fixture-smoke
  execution, report generation, unsupported tiers, and CLI validation.
- AC-012: `python3 autoresearch/validate.py` and
  `python3 -m unittest discover -s autoresearch/tests` pass.
- AC-013: Evidence records the deleted controller files, new core usage path,
  validation output, and residual limits.

## Progress And Notes

- 2026-06-23: Opened after user clarified that Python loop/state controllers
  should be deleted, not demoted. The retained design is a Karpathy-style
  human-owned `program.md` plus one-shot experiment runner; the LLM reasoning
  engine owns repeated iteration.
- 2026-06-23: Added `autoresearch/program.md`, `autoresearch/run_once.py`, and
  tests; deleted Python loop/candidate controllers, long-run templates, their
  tests, and stale long-run readiness records; repaired references; updated the
  README; validated with `python3 autoresearch/validate.py` and
  `python3 -m unittest discover -s autoresearch/tests`. Evidence:
  `.10x/evidence/2026-06-23-simplify-autoresearch-program-loop.md`. Review:
  `.10x/reviews/2026-06-23-simplify-autoresearch-program-loop.md`.

## Blockers

None.
