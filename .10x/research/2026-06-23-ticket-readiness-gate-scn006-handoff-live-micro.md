Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-820-ticket-readiness-gate-scn006-handoff-live-micro

## Experiment ID

EXP-20260623-820-ticket-readiness-gate-scn006-handoff-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-ticket-readiness-gate-v1` improves SCN-006 behavior when
the user asks for safe handoff preparation but does not explicitly ask for a
10x ticket.

## Motivation

`EXP-20260623-819-ticket-readiness-gate-scn006-live-micro` favored the
candidate, but the no-10x control also created a passing ticket because the
prompt directly said "Create the 10x ticket." This follow-up removes that
control hint while preserving the same implementation context.

## Method Tier

MICRO. One narrow SCN-006 live ticket-boundary prompt.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-ticket-readiness-gate.md`.

## Control

Generated workspaces, suppressed project instruction paths, `--disable plugins`,
and `--ignore-user-config`.

## Scenario Set

- SCN-006: ticket-boundary.

Live prompt:

```text
Implementation is approved for the enterprise billing dashboard, but do not change product code in this turn. I need this handed off to another coding agent so they can start safely in a fresh session without asking me follow-up questions.

Context:
- Existing React route: `src/features/billing/ExceptionsPage.tsx`.
- Existing data hook: `usePricingExceptions()`.
- Existing table component: `PricingExceptionsTable`.
- Required change: add CSV export for the currently visible filtered rows.
- CSV columns: `customer_id`, `account_name`, `exception_reason`, `requested_discount_pct`, `status`, `requested_by`, `created_at`.
- No backend, auth, permissions, email, notification, or data model changes are in scope.
- Empty filtered set: export button disabled with existing disabled-button styling.
- Tests: unit test CSV escaping/content and empty-state disabled behavior.

Prepare the handoff artifact now.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-820-ticket-readiness-gate-scn006-handoff-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-ticket-readiness-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-ticket-readiness-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prompt": "Implementation is approved for the enterprise billing dashboard, but do not change product code in this turn. I need this handed off to another coding agent so they can start safely in a fresh session without asking me follow-up questions.\n\nContext:\n- Existing React route: `src/features/billing/ExceptionsPage.tsx`.\n- Existing data hook: `usePricingExceptions()`.\n- Existing table component: `PricingExceptionsTable`.\n- Required change: add CSV export for the currently visible filtered rows.\n- CSV columns: `customer_id`, `account_name`, `exception_reason`, `requested_discount_pct`, `status`, `requested_by`, `created_at`.\n- No backend, auth, permissions, email, notification, or data model changes are in scope.\n- Empty filtered set: export button disabled with existing disabled-button styling.\n- Tests: unit test CSV escaping/content and empty-state disabled behavior.\n\nPrepare the handoff artifact now."
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

## Subject Agent And Model

Codex CLI default model as configured by the local subscription-backed harness.

## Harness Target

Codex CLI live subject runner with generated workspaces and explicit instruction
injection per arm.

## Scenario And Workspace Procedure

The runner creates an isolated generated workspace for each arm, suppresses
project-level instruction files, injects the scenario prompt, and captures raw
transcripts, file outputs, command metadata, and score artifacts.

## Repetition Count

One repetition per arm.

## Prediction

Candidate should create one bounded executable ticket or equivalent 10x handoff
record with scope, non-goals, acceptance criteria, evidence expectations,
references, and blockers. Current 10x may also do so. The no-10x control is
more likely to produce prose-only handoff notes or miss record graph shape.

## Metrics To Score

Primary: S003 and manual ticket-boundary quality.

## Quality Floors

S003 active floor 75.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one first
turn unless transcript inspection shows a continuation is necessary.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for new handoff/ticket outputs.

## Manual Inspection Requirement

Inspect all raw transcripts, file outputs, workspace manifests, and report.

## Promotion Criteria

No promotion from this single MICRO. A promotion would require repeated live
evidence, manual inspection, review, and explicit human approval.

## Known Risks And Confounders

- The generated workspace still lacks a real app, so manual inspection must
  distinguish proper handoff from unverified implementation assumptions.
- Current `SKILL.md` may already be optimal.
- One sample cannot distinguish stochastic handoff quality from candidate
  effect.

## Execution Log

- 2026-06-23: Registered before execution.

## Score Artifacts

Pending.

## Manual Inspection Findings

Pending.

## Final Verdict

Pending.
