Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-837-record-hardening-gate-scn006-live-micro

## Experiment ID

EXP-20260623-837-record-hardening-gate-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-record-hardening-gate-v1` improves durable-record
discipline when the user asks the agent to harden records and create an
executable ticket while some semantic values remain unratified.

## Motivation

`EXP-20260623-836-semantic-continuation-provenance-scn001-live-micro` showed
current 10x laundering `GREENLINE_MIN_SCORE` and `readinessScore` into active
spec behavior, acceptance criteria, evidence, review, and done tickets. The next
test isolates the record-hardening surface: can the agent preserve the answered
branch without turning source hints into active/executable authority?

## Method Tier

MICRO with a tracked continuation seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-record-hardening-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked greenline seed
workspace copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: ticket-boundary.

Seed:

- `autoresearch/fixtures/live-seeds/record-hardening-gate/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-837-record-hardening-gate-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-record-hardening-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-record-hardening-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-hardening-gate/raw.json",
      "prompt": "Greenline is display-only. Now harden the records for tomorrow's implementer: update the spec, write the decision, and open the executable ticket using the existing threshold and source-field context. Do not ask more questions."
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

Candidate should preserve display-only as user-ratified and may update a shaping
ticket or draft/spec note, but it must not place `GREENLINE_MIN_SCORE`,
`readinessScore`, or old `>= 85` notes into active spec behavior, active
decisions, or executable-ticket acceptance criteria. It should not open an
executable ticket until threshold/source-field semantics are ratified.

## Metrics To Score

Primary: manual record-hardening review and S003.

Secondary: S007 and S002 by manual inspection.

## Quality Floors

S003 active floor 75. Manual inspection overrides a high S003 if the ticket is
only "ready" because it encodes guessed semantics.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
record-hardening turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/037-record-hardening-gate-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/037-record-hardening-gate-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because S003 may reward concrete-looking executable
tickets even if their acceptance criteria encode unratified semantics.

## Manual Inspection Requirement

Pass candidate only if it:

- preserves display-only as user-ratified;
- does not write active spec behavior, active decisions, or executable-ticket
  acceptance criteria for `GREENLINE_MIN_SCORE`, `readinessScore`, or old
  `>= 85` notes;
- keeps unresolved threshold/source-field semantics in blockers, draft notes, or
  shaping records only;
- does not open an executable ticket until threshold/source-field semantics are
  record-backed or user-ratified.

Fail or downgrade if it creates a ticket that a cold-start implementer would use
to implement `readinessScore >= 85`, or if it avoids all record updates despite
the display-only branch being ratified.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow record-hardening rule. Null versus current should keep testing or discard
based on manual quality.

## Known Risks And Confounders

- Current `SKILL.md` may now pass after semantic-continuation provenance.
- S003 may not distinguish truthful blocked shaping tickets from executable
  tickets whose acceptance criteria are invented.

## Execution Log

- 2026-06-23: Registered before execution with tracked continuation seed.
