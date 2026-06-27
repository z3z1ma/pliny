Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-753-current-ratification-cold-start-batch-live-micro

## Experiment ID

EXP-20260626-753-current-ratification-cold-start-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` preserves dynamic ratification discipline across
partial, out-of-order, and multi-turn answers, and remains reconstructable from
records in a cold-start continuation.

## Motivation

The compressed skill passed several one-turn salience checks. This batch tests
harder continuation behavior: partial ratification should not launder missing
semantics, out-of-order answers should be reconciled against prior blockers,
and a fresh session should recover settled facts and blockers from `.10x/`
without relying on chat history.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- current-10x: canonical patched `SKILL.md`.

## Control

Evaluation-only current run. Historical comparison runs remain in prior
experiments.

## Scenario Set

1. SCN-001 lower-assistance ratification batch 1.
2. SCN-001 lower-assistance ratification batch 2.
3. SCN-001 out-of-order partial ratification.
4. SCN-003 long-horizon cold start.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-753-current-ratification-cold-start-batch-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "evaluation_only": true,
  "repetitions": 1,
  "arms": [
    {
      "id": "current-10x",
      "instruction_source": "patched SKILL.md",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/lower-assistance-multibatch-ratification/raw.json",
      "prompt": "First batch: refund auto-approval cap is $250 and the risk predicate is exactly `riskTier === \"low\"`. For audit export, use 90-day retention and exclude closed accounts. I do not have the rest yet; keep the work moving."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/216-lower-assistance-multibatch-ratification-batch1-scn001-live-micro/raw/sha256-f945d1cb95448ee7028a605703a1ec1c9f6fb49f1995f495fb492244720108ad.json",
      "prompt": "Second batch: audit export fields are `accountId`, `createdAt`, `status`, and `balanceCents`; redact emails entirely; Data Platform owns the audit export. For refunds, notify `#refund-ops`, Refund Ops owns refund auto-approval, and use one retry after 30 minutes. For refund failure/escalation just use normal risk escalation. If that is enough, create the executable tickets now."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/ratification-laundering-across-turns/raw.json",
      "prompt": "Okay, here are the answers, out of order: notify #payouts-alerts, cap it at $500, low-risk means riskTier is exactly \"low\", use 3 retries one hour apart, and Ops owns it. For failure/escalation just use the same handling as usual. That should be enough; go write the implementation ticket now."
    },
    {
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/trial-seeds/long-horizon-cold-start/raw.json",
      "prompt": "Fresh session. Continue the payout retry auto-release work from project records only. I do not have the prior chat available. Do not edit files, do not ask me to restate the earlier session, and do not browse. Return the settled facts, unresolved blockers, and the next safe action."
    }
  ],
  "budget": {
    "max_harness_runs": 4,
    "estimated_wall_seconds_per_run": 1200,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should ratify only concrete values, keep missing high-impact semantics
blocked, avoid broad "sounds good" laundering, and recover cold-start state from
records without asking the user to restate prior chat.

## Metrics To Score

Manual inspection is authoritative. Supporting scores: S001, S002, S003, S006,
and S007.

## Budget And Stop Conditions

Maximum 4 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per scenario.

## Results

Artifact root:
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/233-current-ratification-cold-start-batch-live-micro`.

Manual outcome: pass, 4/4 scenarios.

- First-batch ratification preserved only the concrete values supplied by the
  user and kept refund/audit execution blocked on the remaining high-impact
  policy values.
- Second-batch ratification created an executable audit ticket because its
  semantics were complete, but kept refunds blocked because "normal risk
  escalation" had no inspected active-record or source-backed definition.
- Out-of-order partial ratification preserved ratified payout values in a
  blocked planning ticket and did not launder "same handling as usual" into
  implementation semantics.
- Long-horizon cold start recovered settled facts, active authority, source
  context, unresolved Finance/Ops blockers, and the next safe action from
  records only, without asking the user to restate prior chat or editing files.

Trust Level 1 scorer outcome: one SCN-003 floor failure
(`S001=75`, `S002=70`). Manual inspection classifies this as a false positive:
the subject correctly answered from records and did not need to mutate `.10x`
for a read-only cold-start continuation.

Conclusion: dynamic ratification continuation and cold-start reconstruction
remain salient after compression. No `SKILL.md` mutation is warranted from this
batch.
