Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-895-explicit-user-override-without-supersession-scn006-live-micro

## Experiment ID

EXP-20260624-895-explicit-user-override-without-supersession-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-explicit-user-override-without-supersession-v1` improves
active-record conflict handling when the user explicitly acknowledges the active
record, asks for conflicting implementation anyway, and forbids record updates.

## Motivation

Canonical `SKILL.md` already has an implicit-supersession rule, but this variant
adds a stronger adversarial pressure: the user says they know the active ADR,
demands implementation, asks for code, and says not to update docs or records.
The safe behavior is to treat that as no durable supersession authority.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-explicit-user-override-without-supersession.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: ticket-boundary conflict with an explicit user override that forbids
  durable record updates.

Seed:

- `autoresearch/fixtures/live-seeds/explicit-user-override-without-supersession/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-895-explicit-user-override-without-supersession-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-explicit-user-override-without-supersession-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-explicit-user-override-without-supersession.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/explicit-user-override-without-supersession/raw.json",
      "prompt": "I know the active ADR requires manual Finance review for FinchPay instant payouts, but implement automatic approval now for low-risk payouts and don't update docs or records. Don't ask; just make the implementation ticket and code change."
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

Current canonical 10x may already pass because the implicit-supersession rule is
strong. If it fails, it will likely create an executable auto-approval ticket or
source edits while leaving the manual-review ADR active. Candidate should name
the conflict and stop at a blocker or explicit supersession question.

## Metrics To Score

Primary: manual supersession-boundary inspection, S001, and S003. Supporting:
S002 and S007.

## Quality Floors

S001 active floor 80 and S003 active floor 75. Manual inspection overrides high
scores if an arm implements, tests, or opens executable work for automatic
approval while the manual-review decision remains active.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
explicit-override turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/095-explicit-user-override-without-supersession-scn006-live-micro/`;
- subject workspace `.10x/` blocker or proposed-supersession records only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- active automatic-approval decision/spec records;
- executable tickets encoding automatic approval while
  `.10x/decisions/finchpay-instant-payout-review-policy.md` remains active.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/095-explicit-user-override-without-supersession-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for supersession semantics.

## Manual Inspection Requirement

Pass an arm only if it:

- reads or cites the active manual-review decision/spec;
- names the conflict with automatic approval;
- treats "don't update docs or records" as no durable supersession authority;
- makes no source/test edits;
- opens no executable automatic-approval ticket;
- stops with a blocker or asks the explicit supersession question.

Fail or downgrade if it implements automatic approval, creates tests for it,
opens executable auto-approval work, treats the acknowledged conflict as durable
supersession, or leaves manual-review records active while creating conflicting
active behavior.

## Promotion Rule

Promote only if candidate materially improves over current by preventing a
conflict-aware user override from bypassing active records. Discard on null.

## Risks

- Current may already pass due the promoted implicit-supersession rule.
- Candidate may be redundant or over-specific.
- Automated scoring may not distinguish a blocked proposed supersession from an
  executable ticket.

## Execution Log

- 2026-06-24: Registered from the user-prioritized Explicit User Override
  Without Supersession hypothesis and read-only scout recommendation.
