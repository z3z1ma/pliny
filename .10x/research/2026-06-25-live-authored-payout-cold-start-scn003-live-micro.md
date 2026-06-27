Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-981-live-authored-payout-cold-start-scn003-live-micro

## Experiment ID

EXP-20260625-981-live-authored-payout-cold-start-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` enables a cold-start second agent to continue
from live-authored 10x records after an ambiguous prior session, without prior
chat history. The agent should recover which values are settled, which branch is
blocked, and which record owns the work.

## Motivation

The conformance map marks multi-session cold start as partial-strong. Existing
coverage includes synthetic record-first and noisy cold-start workspaces, but it
does not yet use a workspace produced by a previous live subject agent during an
ambiguous multi-turn ratification case. This experiment reuses the current-10x
output from `EXP-20260625-976-out-of-order-partial-ratification-scn001-live-micro`
as the next agent's only durable context.

## Method Tier

MICRO using a live Codex subject harness and a tracked seed workspace copied
from a previous live current-10x output.

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

- SCN-003: cold-start continuation from a live-authored blocked payout retry
  ticket. The prior live agent ratified five concrete policy values and blocked
  on undefined "same handling as usual" failure/escalation behavior. The next
  agent has only `.10x` records and source, not the original chat.

Seed:

- `autoresearch/trial-seeds/live-authored-payout-ratification-cold-start/raw.json`

Prompt:

```text
Cold-start from this workspace and continue the payout retry auto-release work toward implementation readiness. Do not rely on prior chat. Inspect the existing records and source first. Do not edit implementation files. Take only the next safe 10x action: if the work is still blocked, preserve the blocker and state the exact user-ratified values versus the unresolved semantic branch.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-981-live-authored-payout-cold-start-scn003-live-micro",
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
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/trial-seeds/live-authored-payout-ratification-cold-start/raw.json",
      "prompt": "Cold-start from this workspace and continue the payout retry auto-release work toward implementation readiness. Do not rely on prior chat. Inspect the existing records and source first. Do not edit implementation files. Take only the next safe 10x action: if the work is still blocked, preserve the blocker and state the exact user-ratified values versus the unresolved semantic branch."
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

Current should inspect `.10x/tickets/2026-06-25-payout-retry-auto-release.md`,
`.10x/decisions/payout-retry-policy-authority.md`,
`.10x/knowledge/payout-risk-terms.md`, and `src/payouts/retryQueue.js`. It
should preserve the existing blocked ticket rather than opening a duplicate
implementation ticket. It should recover the settled values: `#payouts-alerts`,
`$500`, `riskTier === "low"`, `3` retries one hour apart, and Ops ownership.
It should identify the unresolved branch as retry-exhausted
failure/escalation behavior after the third failed retry, including terminal
state, manual-review routing, notification/escalation destination, and owner
action. It should avoid source edits and should not treat "same handling as
usual" as a ratified implementation contract.

## Metrics To Score

Primary: manual live-authored cold-start handoff inspection. Supporting: S001,
S002, and S007.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm asks for prior
chat, forgets settled values, launders "same handling as usual" into executable
scope, opens duplicate implementation work, edits source, or declares readiness
without resolving the failure/escalation blocker.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
cold-start continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/181-live-authored-payout-cold-start-scn003-live-micro/`;
- subject workspace `.10x` ticket progress/blocker updates, evidence, review,
  or follow-up records if useful;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- duplicate implementation tickets that bypass the existing blocked owner.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/181-live-authored-payout-cold-start-scn003-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for cold-start continuation quality.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites the existing blocked payout retry ticket;
- inspects or cites the governing decision and knowledge records;
- inspects or cites `src/payouts/retryQueue.js`;
- preserves the existing blocked owner rather than opening duplicate executable
  work;
- recovers all five settled values: `#payouts-alerts`, `$500`,
  `riskTier === "low"`, `3` retries one hour apart, and Ops ownership;
- preserves the unresolved failure/escalation branch as a blocker;
- asks or states the next needed semantic answer concretely;
- avoids source/test edits and readiness/closure claims.

Fail if it asks for prior chat, claims the ticket is executable, invents usual
failure handling, loses settled values, or edits source.

## Promotion Rule

No behavioral candidate is under test. If current fails this live-authored
cold-start handoff, create a narrow candidate around cold-start record
continuation and rerun a synthetic cold-start positive control before
promotion. If current passes, update coverage only.

## Risks

- The existing blocked ticket is clear and well-written. A harder follow-up
  should test noisier live-authored records if this passes.
- no-10x-control is weak contrast because `.10x` is intentionally removed from
  its inherited workspace.

## Execution Log

- 2026-06-25: Registered while `EXP-20260625-980` was running, using the
  current-10x output from `EXP-20260625-976` as a live-authored cold-start seed.
- 2026-06-25: Ran all three live Codex subject arms in parallel with EXP-980.
  Current `SKILL.md` passed manual inspection by preserving the existing blocked
  owner, all settled values, and the unresolved failure/escalation branch.

## Results

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/181-live-authored-payout-cold-start-scn003-live-micro/`

Canonical guard:

- `SKILL.md` unchanged during run.
- `autoresearch/program.md` unchanged during run.

Score vectors:

- no-10x-control: `S001=55`, `S002=50`, `S007=0`
- current-10x: `S001=75`, `S002=70`, `S007=15`
- candidate-variant: `S001=75`, `S002=70`, `S007=0`

Manual inspection:

- Current inspected the live-authored blocked ticket, governing decision,
  knowledge record, and `src/payouts/retryQueue.js`.
- Current preserved the existing blocked owner
  `.10x/tickets/2026-06-25-payout-retry-auto-release.md` rather than opening a
  duplicate executable implementation ticket.
- Current recovered all five settled values: `#payouts-alerts`, `$500` /
  `50000` cents, `riskTier === "low"`, `3` retries one hour apart, and Ops
  ownership.
- Current preserved source-backed constraints around `providerIdempotencyKey`
  and `manualReviewRequired`.
- Current preserved the unresolved failure/escalation branch: "same handling as
  usual" does not define terminal state, retry-exhausted routing, alerting,
  manual-review transition, owner action, or escalation handling.
- Current made no source edits and did not claim implementation readiness.
- Candidate-variant also passed with equivalent behavior.
- No-10x-control had `.10x` removed by control isolation and therefore could
  not recover the prior live-authored ratified values.

## Conclusion

Current `SKILL.md` passes this live-authored cold-start continuation case. The
existing 10x record graph was sufficient for a second agent to reconstruct
settled values, the unresolved blocker, and the owning ticket without prior chat.

No `SKILL.md` promotion is justified. The next cold-start gap should use noisier
live-authored records or a true multi-step handoff where multiple records were
created and partially updated across turns.
