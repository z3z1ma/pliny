Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-819-ticket-readiness-gate-scn006-live-micro

## Experiment ID

EXP-20260623-819-ticket-readiness-gate-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-ticket-readiness-gate-v1` improves SCN-006 ticket-boundary
behavior by creating a bounded executable ticket once enough implementation
context is known, while preserving no-implementation discipline.

## Motivation

The promoted upstream-gated blocker rule improves ambiguous first turns, but the
main residual risk is under-questioning or over-questioning near the
ticket-boundary. SCN-006 isolates whether the subject can recognize that the
next safe action is ticket creation.

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
We have approved the product decision for the enterprise billing dashboard.
Prepare execution, but do not implement.

Context:
- Existing React route: `src/features/billing/ExceptionsPage.tsx`.
- Existing data hook: `usePricingExceptions()`.
- Existing table component: `PricingExceptionsTable`.
- Required change: add CSV export for the currently visible filtered rows.
- CSV columns: `customer_id`, `account_name`, `exception_reason`, `requested_discount_pct`, `status`, `requested_by`, `created_at`.
- No backend, auth, permissions, email, notification, or data model changes are in scope.
- Empty filtered set: export button disabled with existing disabled-button styling.
- Tests: unit test CSV escaping/content and empty-state disabled behavior.

Create the 10x ticket a subagent should execute.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-819-ticket-readiness-gate-scn006-live-micro",
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
      "prompt": "We have approved the product decision for the enterprise billing dashboard.\nPrepare execution, but do not implement.\n\nContext:\n- Existing React route: `src/features/billing/ExceptionsPage.tsx`.\n- Existing data hook: `usePricingExceptions()`.\n- Existing table component: `PricingExceptionsTable`.\n- Required change: add CSV export for the currently visible filtered rows.\n- CSV columns: `customer_id`, `account_name`, `exception_reason`, `requested_discount_pct`, `status`, `requested_by`, `created_at`.\n- No backend, auth, permissions, email, notification, or data model changes are in scope.\n- Empty filtered set: export button disabled with existing disabled-button styling.\n- Tests: unit test CSV escaping/content and empty-state disabled behavior.\n\nCreate the 10x ticket a subagent should execute."
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

Candidate should create one bounded executable ticket with scope, non-goals,
acceptance criteria, evidence expectations, references, and blockers. It should
not implement and should not ask more questions because the prompt supplies the
ticket-critical context.

## Metrics To Score

Primary: S003 and S007.

## Quality Floors

S003 active floor 75.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one first
turn unless transcript inspection shows a continuation is necessary.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for new ticket outputs and S007.

## Manual Inspection Requirement

Inspect all raw transcripts, file outputs, workspace manifests, and report.

## Promotion Criteria

No promotion from this single MICRO. A promotion would require live evidence,
manual inspection, review, and explicit human approval.

## Known Risks And Confounders

- The prompt supplies code paths but the generated workspace does not include a
  real app, so manual inspection must distinguish correct ticket creation from
  false blocker behavior caused by harness limitations.
- Current `SKILL.md` may already be optimal on this scenario.
- One sample cannot distinguish stochastic ticket quality from candidate effect.

## Execution Log

- 2026-06-23: Registered before execution.
- 2026-06-23: Ran live Codex MICRO with three arms. Candidate scored `S003=100`;
  current scored `S003=80`; no-10x control scored `S003=80`.
- 2026-06-23: Manual inspection found the candidate created the strongest ticket
  by adding explicit evidence expectations and a real implementation-time
  blocker to verify referenced code paths before changing code.
- 2026-06-23: Regenerated report with campaign metadata and appended
  `results.tsv` with status `keep`.

## Score Artifacts

- Raw artifacts:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro/raw/`
- Score artifacts:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro/scores/`
- Report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro/report.md`
- Campaign metadata:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro/campaign.json`
- Evidence:
  `.10x/evidence/2026-06-23-ticket-readiness-gate-scn006-live-micro.md`

## Manual Inspection Findings

- Candidate ticket included scope, non-goals, acceptance criteria, evidence
  expectations, references, and an implementation-time blocker for missing local
  source files.
- Current 10x ticket was mostly good but omitted explicit evidence expectations
  and recorded no known blockers despite the generated workspace lacking the
  real source tree.
- No-10x control also created a passing ticket, so the scenario's control
  discrimination is weak.
- No arm implemented or created a broad parent ticket.

## Final Verdict

`keep-testing`, not promoted. The candidate improved SCN-006 ticket readiness in
this run, but one sample with a passing control arm is not promotion-grade.
