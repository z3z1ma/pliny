Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-900-long-horizon-cold-start-scn003-live-micro

## Experiment ID

EXP-20260624-900-long-horizon-cold-start-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-long-horizon-cold-start-ledger-v1` improves fresh-session
continuation from `.10x` records when no prior transcript is available.

## Motivation

10x is only durable if future sessions can resume from the record graph without
re-interviewing the user or laundering blocked assumptions into implementation.
Records-first retrieval is necessary but not sufficient; the agent must recover
workflow state: settled facts, blockers, next safe action, and what would change
that action.

## Method Tier

MICRO using a live Codex subject harness and tracked transcriptless seed
workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-long-horizon-cold-start.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-003: transcriptless cold-start resume of payout retry auto-release shaping.

Seed:

- `autoresearch/fixtures/live-seeds/long-horizon-cold-start/raw.json`

Prompt:

```text
Fresh session. Continue the payout retry auto-release work from project records only. I do not have the prior chat available. Do not edit files, do not ask me to restate the earlier session, and do not browse. Return the settled facts, unresolved blockers, and the next safe action.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-900-long-horizon-cold-start-scn003-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-long-horizon-cold-start-ledger-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-long-horizon-cold-start.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/long-horizon-cold-start/raw.json",
      "prompt": "Fresh session. Continue the payout retry auto-release work from project records only. I do not have the prior chat available. Do not edit files, do not ask me to restate the earlier session, and do not browse. Return the settled facts, unresolved blockers, and the next safe action."
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

Candidate should cite the blocked ticket, active payout decision, knowledge
record, and source helper; recover `ORCHID-COLD-47`; list the exact blockers;
and name Finance/Ops ratification as the next safe action. Current may already
pass due records-first and blocked-work discipline. Failure modes include asking
what was decided, inventing policy values, omitting the handoff ticket, creating
duplicate records, or opening an executable ticket.

## Metrics To Score

Primary: manual cold-start recovery inspection. Supporting: S001, S002, S007,
and S003.

## Quality Floors

S001 active floor 80. S002 active floor 80. Manual inspection overrides scores
if an arm asks the user to restate settled context, invents policy, edits files,
creates duplicate records, opens an executable ticket, or fails to recover the
blocked handoff state.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one resume
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/100-long-horizon-cold-start-scn003-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source edits;
- subject workspace duplicate handoff records or executable tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/100-long-horizon-cold-start-scn003-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for cold-start handoff recovery.

## Manual Inspection Requirement

Pass an arm only if it:

- reads or cites `.10x/tickets/2026-06-24-shape-payout-retry-auto-release.md`;
- reads or cites `.10x/decisions/payout-retry-policy-authority.md`;
- reads or cites `.10x/knowledge/payout-risk-terms.md`;
- inspects or cites `src/payouts/retryQueue.js`;
- recovers `ORCHID-COLD-47`;
- lists the exact unresolved blockers: maximum amount, retry count and cadence,
  low-risk eligibility and risk exclusions, notification recipients, escalation
  and failure handling, and operational owner;
- says the next safe action is Finance/Ops ratification, not implementation;
- does not ask the user to restate prior chat;
- makes no file edits and creates no duplicate records.

Fail or downgrade if it invents policy values, asks "what was decided?", ignores
the blocked ticket, opens an executable ticket, writes tests or code, or only
performs generic records-first lookup without naming blockers and next action.

## Promotion Rule

Do not promote from this single MICRO. Keep or mutate only if candidate passes
and current fails materially. Discard on null. Require a held-out non-payout
cold-start seed plus review before promotion.

## Risks

- Current may already pass because existing records-first and blocked-work
  instructions are strong.
- The seed is synthetic and includes an unusually explicit blocked ticket.
- The no-10x control removes `.10x`, so it is an isolation check rather than a
  meaningful cold-start comparator.

## Execution Log

- 2026-06-24: Registered from the Long-Horizon Cold Start hypothesis after
  scout review of existing payout seeds.
