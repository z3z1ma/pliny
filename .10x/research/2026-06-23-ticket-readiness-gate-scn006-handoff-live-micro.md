Status: done
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

The runner intended to create a generated workspace for each arm, suppress
project-level instruction files, inject the scenario prompt, and capture raw
transcripts, file outputs, command metadata, and score artifacts.

Manual inspection later found the generated arm workspaces were siblings under
the same artifact parent during live execution. That allowed a later arm to
discover earlier arm output by traversing `..`. This run is therefore
confounded for candidate-versus-current uplift.

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
- The candidate arm read a sibling current-arm generated workspace and reused
  its ticket as prior art, so its ticket quality cannot be attributed only to
  `candidate-ticket-readiness-gate-v1`.

## Execution Log

- 2026-06-23: Registered before execution.
- 2026-06-23: Live run completed with score vector
  `candidate:S003=100 current:S003=100 control:S003=10`.
- 2026-06-23: Manual inspection found the candidate ticket's progress notes
  stated it searched nearby generated workspaces and found a prior matching
  ticket at
  `../sha256-9c6faade8508609e9e1681b1aa51a27db254c904d70b56f29af1a56a18c424e5/.10x/tickets/2026-06-23-enterprise-billing-csv-export.md`.
  The run was marked confounded.
- 2026-06-23: Opened
  `.10x/tickets/done/2026-06-23-isolate-live-subject-workspaces.md` to fix the
  harness before reusing this scenario as promotion evidence.

## Score Artifacts

- no-10x-control:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/scores/sha256-902eb6fa2f15820c2c3e84c5ac632b4cadc133c31d8c3589c406762e89ebafec.score.json`
  scored `S003=10`.
- current-10x:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/scores/sha256-9c6faade8508609e9e1681b1aa51a27db254c904d70b56f29af1a56a18c424e5.score.json`
  scored `S003=100`.
- candidate-variant:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/scores/sha256-f53f6e8e54955bf51ec6aa5c9e5cb9ee433da0d5c3179b0d9a55d7010b6b8878.score.json`
  scored `S003=100`.

## Manual Inspection Findings

- no-10x-control wrote a prose handoff artifact and did not create a 10x ticket,
  so the `S003=10` floor is directionally correct.
- current-10x created a bounded `.10x/tickets/` ticket with scope, non-goals,
  acceptance criteria, test expectations, evidence expectations, and an
  implementation-time verification blocker.
- candidate-variant created a similarly strong ticket, but its own notes state
  it found and used the current arm's ticket in a nearby sibling generated
  workspace. Candidate output is therefore contaminated.

## Final Verdict

Confounded. This run is useful evidence that SCN-006 handoff prompts separate
10x from no-10x behavior, but it is not valid evidence that
`candidate-ticket-readiness-gate-v1` improves over current canonical `SKILL.md`.
Do not promote or reject the candidate from this run. Re-run after fixing live
subject workspace isolation.
