Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-854-fish-before-opening-scn005-live-micro

## Experiment ID

EXP-20260623-854-fish-before-opening-scn005-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-fish-before-opening-pressure-v1` improves record economy
when the user explicitly asks to open a ticket for an issue that already has an
active ticket owner.

## Motivation

10x already says to fish before opening tickets. This MICRO tests whether that
rule holds under direct "open a ticket" wording, where an agent might satisfy
the surface instruction by creating a duplicate durable owner.

## Method Tier

MICRO using a tracked ticket-deduplication seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-fish-before-opening-pressure.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-005: one active ticket already owns the requested CSV quote/newline
  follow-up; the prompt asks to open a follow-up ticket for the same issue.

Seed:

- `autoresearch/fixtures/live-seeds/fish-before-opening/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-854-fish-before-opening-scn005-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-fish-before-opening-pressure-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-fish-before-opening-pressure.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-005",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/fish-before-opening/raw.json",
      "prompt": "Open a follow-up ticket for the CSV export quote/newline coverage gap. Do not touch source code."
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

Current may already pass because canonical `SKILL.md` says to fish before
opening and not duplicate work the record graph already owns. Candidate should
pass by making the pressure case explicit.

## Metrics To Score

Primary: manual duplicate-ticket inspection, S002, and S005.

## Quality Floors

S002 active floor 80. Manual inspection overrides scores because the intended
pass is a single existing-ticket update rather than a new ticket.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
ticket-tracking turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/054-fish-before-opening-scn005-live-micro/`;
- one update to the existing active ticket in the subject workspace;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files;
- duplicate tickets for the same CSV quote/newline gap.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/054-fish-before-opening-scn005-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for duplicate-ticket behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or identifies the existing active CSV quote/newline ticket;
- creates no duplicate ticket for the same issue;
- updates the existing ticket if the prompt adds durable context;
- does not touch source files;
- explains in the final answer that the existing ticket is the durable owner.

Fail if it creates a second ticket for the same gap, edits source files, or
leaves new durable context only in chat.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow fish-before-opening pressure rule. Null versus current should discard.

## Known Risks And Confounders

- Current `SKILL.md` already contains a fish-before-opening rule, so this may be
  a null regression run.
- The active ticket is strongly named, making it easier to find.
- The no-10x control has inherited `.10x` removed and therefore cannot inspect
  the existing owner in the same way.

## Execution Log

- 2026-06-23: Registered after the skill mirror exposure null result. This
  tests duplicate-ticket prevention under explicit "open a ticket" pressure.

## Results

Pending.

## Conclusions

Pending.
