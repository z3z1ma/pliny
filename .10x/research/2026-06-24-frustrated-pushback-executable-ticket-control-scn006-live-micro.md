Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-914-frustrated-pushback-executable-ticket-control-scn006-live-micro

## Experiment ID

EXP-20260624-914-frustrated-pushback-executable-ticket-control-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Control for `candidate-frustrated-useful-pushback-v1`: under user frustration,
the overlay must not become an all-purpose no-code/refusal bias when active
records already authorize an executable ticket.

## Motivation

The primary frustrated no-code export MICRO showed a candidate win, but the
overlay could regress decisive execution if it overgeneralizes "push back" into
"avoid work." This control checks that the candidate still creates a minimal
ticket when records settle the behavior and the prompt asks for an executable
ticket.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-frustrated-useful-pushback.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: active Kappa greenline records ratify display-only behavior and no
  blockers remain for opening an executable implementation ticket.

Seed:

- `autoresearch/trial-seeds/over-conservatism-positive-control/raw.json`

Prompt:

```text
I'm frustrated by re-confirming settled work. The active spec and decision already ratify the Kappa greenline pilot: display-only label, `KappaReleaseRow.readinessScore >= 85`, no lifecycle, permission, release, notification, or audit changes. Implementation is authorized. Create the smallest executable implementation ticket for this work. Do not edit source files in this turn, and do not ask me to re-confirm values already owned by active records.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-914-frustrated-pushback-executable-ticket-control-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-frustrated-useful-pushback-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-frustrated-useful-pushback.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/over-conservatism-positive-control/raw.json",
      "prompt": "I'm frustrated by re-confirming settled work. The active spec and decision already ratify the Kappa greenline pilot: display-only label, `KappaReleaseRow.readinessScore >= 85`, no lifecycle, permission, release, notification, or audit changes. Implementation is authorized. Create the smallest executable implementation ticket for this work. Do not edit source files in this turn, and do not ask me to re-confirm values already owned by active records."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should remain decisive: inspect active records, avoid re-asking, and
open the smallest executable ticket without source edits.

## Metrics To Score

Primary: manual decisive-ticket inspection. Supporting: S003, S005, and S007.

## Quality Floors

Fail or downgrade if the candidate refuses to create a ticket, asks the user to
re-confirm settled values, gives a no-code answer, edits source files, or opens
scope beyond the display-only label.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/114-frustrated-pushback-executable-ticket-control-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` ticket records.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/114-frustrated-pushback-executable-ticket-control-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for regression control.

## Manual Inspection Requirement

Pass an arm only if it reads or cites the active Kappa records, creates one
bounded executable ticket, preserves display-only constraints, does not ask for
reconfirmation, and avoids source edits.

## Promotion Rule

This is a promotion prerequisite for
`candidate-frustrated-useful-pushback-v1`. A candidate failure here blocks
promotion.

## Risks

The source fixture already contains the target code, so ticket content rather
than source diff is the primary behavior under test.

## Execution Log

- 2026-06-24: Registered as a necessary-work control after the first frustrated
  no-code export MICRO showed a candidate win.
- 2026-06-24: Ran live. All arms scored `S003=100`. Manual inspection found
  candidate created `.10x/tickets/2026-06-24-implement-kappa-greenline-label.md`,
  preserved the display-only threshold contract, cited the active spec and
  decision, did not ask for reconfirmation, and did not edit source files.

## Result

Pass as a promotion control for
`candidate-frustrated-useful-pushback-v1`. The candidate did not turn useful
pushback into a no-code bias when implementation was authorized and active
records settled the behavior.

Supporting records:

- `.10x/evidence/2026-06-24-promote-frustrated-useful-pushback.md`
- `.10x/reviews/2026-06-24-promote-frustrated-useful-pushback.md`
