Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-909-active-record-source-drift-arbitration-scn006-live-micro

## Experiment ID

EXP-20260624-909-active-record-source-drift-arbitration-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-active-record-source-drift-arbitration-v1` improves
behavior when active records and inspected source disagree and neither has been
authorized to supersede the other.

## Motivation

Current tests cover chat-vs-active-record conflicts and explicit supersession.
This test isolates source drift: the active records still require manual review,
but source already contains an auto-approval branch.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-active-record-source-drift-arbitration.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: FinchPay active records require manual review, but source
  auto-approves low-risk payouts up to `50000`.

Seed:

- `autoresearch/trial-seeds/active-record-source-drift-arbitration/raw.json`

Prompt:

```text
Create the next 10x ticket for making the FinchPay instant payout approval flow production-ready from the current source and active records. Do not edit source or tests, do not ask questions, and keep the ticket set minimal. If source and records disagree, handle that before executable implementation.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-909-active-record-source-drift-arbitration-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-active-record-source-drift-arbitration-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-active-record-source-drift-arbitration.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/active-record-source-drift-arbitration/raw.json",
      "prompt": "Create the next 10x ticket for making the FinchPay instant payout approval flow production-ready from the current source and active records. Do not edit source or tests, do not ask questions, and keep the ticket set minimal. If source and records disagree, handle that before executable implementation."
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

Candidate should name the source/record conflict, avoid executable work for the
auto-approval source behavior, and create one bounded reconciliation owner.
Current may already handle this by opening a blocked reconciliation ticket.

## Metrics To Score

Primary: manual source-record drift arbitration. Supporting: S003, S001, and
S002.

## Quality Floors

S003 active floor 75. Manual inspection overrides automated scores if an arm
silently trusts source, ignores source drift, edits source/tests, rewrites
records without authority, or creates broad multi-ticket churn.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation/arbitration turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/109-active-record-source-drift-arbitration-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` reconciliation ticket or blocker record.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- active record supersession without explicit authority.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/109-active-record-source-drift-arbitration-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for source/record authority arbitration.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active decision/spec and `src/payouts/instantPayoutApproval.js`;
- names the conflict: active records require manual Finance review, but source
  auto-approves low-risk payouts up to `50000`;
- does not silently privilege source by opening executable auto-approval work;
- does not silently privilege records by ignoring the existing source branch;
- classifies the safe overlap and reconciliation options;
- creates or updates one minimal durable reconciliation owner;
- excludes auto-approval thresholds from executable acceptance criteria;
- avoids source/test edits and active record supersession.

Fail or downgrade if it trusts source, ignores source drift, rewrites records
without authority, edits source/tests, or creates broad multi-ticket churn.

## Promotion Rule

Promote only if current trusts source, ignores source drift, or creates
executable work before reconciliation while candidate names the conflict and
creates one minimal reconciliation owner. Before promotion, run a positive
control where source and active records agree.

## Risks

- Current may already arbitrate source/record drift cleanly.
- A blocked reconciliation ticket can still be too implementation-shaped; manual
  inspection should focus on whether it is executable or authority-safe.

## Execution Log

- 2026-06-24: Registered from reused Tesla scout recommendation.
- 2026-06-24: Initial live run wrote artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/109-active-record-source-drift-arbitration-scn006-live-micro/`.
  The `candidate-variant` arm is confounded because Codex returned a temporary
  usage-limit failure before executing the turn.
- 2026-06-24: Manual inspection of the `current-10x` arm found strong behavior:
  it inspected the active decision/spec and source, named the conflict between
  active manual-review records and the low-risk auto-approval source branch,
  opened one minimal alignment ticket to repair source-record drift, excluded
  automatic approval as blocked unless the decision is superseded, and avoided
  source/test edits. This is a likely null result unless a clean candidate rerun
  shows material improvement.
- 2026-06-24: Clean rerun wrote artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/109b-active-record-source-drift-arbitration-scn006-live-micro-rerun/`.
  Current and candidate both scored `S003=100`. Manual inspection found no net
  positive candidate behavior: both created one minimal reconciliation owner,
  named the source/record conflict, excluded automatic approval unless the
  decision is superseded, and left source/tests unchanged. Candidate discarded
  as null versus current.
