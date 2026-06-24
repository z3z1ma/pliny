Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-916-record-move-done-historical-reference-trap-scn009-live-micro

## Experiment ID

EXP-20260624-916-record-move-done-historical-reference-trap-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can close an active ticket by moving it to
`tickets/done/` and repairing live record references without broad-rewriting
historical mentions or touching source.

## Motivation

The conformance map marks record graph maintenance mechanics as partial-weak.
Prior supersession testing covered decisions. This MICRO tests the simpler but
common terminal ticket move path: move the completed child ticket, repair
evidence/review/parent links, and preserve historical context.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: completed invoice retry child ticket has pass evidence/review and
  should be moved to `tickets/done/` with coherent references.

Seed:

- `autoresearch/fixtures/live-seeds/record-reference-integrity-closure/raw.json`

Prompt:

```text
The invoice retry child ticket is complete and its evidence/review are pass. Close `.10x/tickets/2026-06-23-align-invoice-retry-schedule.md`: move it to `.10x/tickets/done/`, repair live `.10x` references that should follow the terminal move, and update the parent only as needed for coherent closure. Do not broad-rewrite historical notes, quoted output, or fenced code blocks that mention the old path as history. Do not edit source files and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-916-record-move-done-historical-reference-trap-scn009-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-reference-integrity-closure/raw.json",
      "prompt": "The invoice retry child ticket is complete and its evidence/review are pass. Close `.10x/tickets/2026-06-23-align-invoice-retry-schedule.md`: move it to `.10x/tickets/done/`, repair live `.10x` references that should follow the terminal move, and update the parent only as needed for coherent closure. Do not broad-rewrite historical notes, quoted output, or fenced code blocks that mention the old path as history. Do not edit source files and do not run tests."
    }
  ],
  "budget": {
    "max_harness_runs": 2,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should move the ticket, repair live references in evidence/review/parent
records, avoid source/test edits, and not run tests. No-10x may fail record
reference repair or leave status/path incoherent.

## Metrics To Score

Primary: manual record graph lifecycle inspection. Supporting: S002, S006, and
S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm leaves dangling
live references, broad-rewrites historical examples, edits source/tests, runs
tests, or marks closure without coherent evidence/review references.

## Budget And Stop Conditions

Maximum 2 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/116-record-move-done-historical-reference-trap-scn009-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` ticket/evidence/review/parent closure records.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/116-record-move-done-historical-reference-trap-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for lifecycle/reference behavior.

## Manual Inspection Requirement

Pass an arm only if it moves the active child ticket to `tickets/done/`, keeps
the moved ticket status coherent, repairs live evidence/review/parent references
that should point to the terminal path, preserves historical body text where
appropriate, and avoids source/test edits and test execution.

## Promotion Rule

No behavioral candidate is under test; `candidate-variant` duplicates
`current-10x` only to satisfy the current runner's fixed arm contract. If
current fails and no-10x also fails, create a narrow candidate targeting the
observed record lifecycle failure.

## Risks

The fixture may not contain enough historical path mentions to fully stress
blind replacement. Treat this as a terminal-move mechanics MICRO, not complete
coverage of historical-reference traps.

## Execution Log

- 2026-06-24: Registered from the conformance map and scout recommendations.
- 2026-06-24: Added duplicate `candidate-variant` arm after the runner rejected
  two-arm live definitions.
