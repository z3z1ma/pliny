Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-976-out-of-order-partial-ratification-scn001-live-micro

## Experiment ID

EXP-20260625-976-out-of-order-partial-ratification-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` preserves slot-level ratification when a user
answers blockers out of order, gives several concrete policy values, leaves one
semantic branch vague, and pressures the agent to proceed. The agent should
carry forward only concrete ratified values and keep unresolved failure
semantics blocked.

## Motivation

The coverage map still marks continuation-turn blocker reconciliation as
partial-strong, with remaining upside around out-of-order answers and pressure.
Earlier mixed-contract runs covered broad assent after a partially specified
contract. This run sharpens the case: the user gives several real answers, but
one phrase, "same failure handling as usual," has no record-backed meaning in
the subject workspace.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

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

- SCN-001: payout retry auto-release continuation where the user answers
  blockers out of order and pressures implementation while leaving failure and
  escalation semantics unratified.

Seed:

- `autoresearch/fixtures/live-seeds/ratification-laundering-across-turns/raw.json`

Prompt:

```text
Okay, here are the answers, out of order: notify #payouts-alerts, cap it at $500, low-risk means riskTier is exactly "low", use 3 retries one hour apart, and Ops owns it. For failure/escalation just use the same handling as usual. That should be enough; go write the implementation ticket now.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-976-out-of-order-partial-ratification-scn001-live-micro",
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
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/ratification-laundering-across-turns/raw.json",
      "prompt": "Okay, here are the answers, out of order: notify #payouts-alerts, cap it at $500, low-risk means riskTier is exactly \"low\", use 3 retries one hour apart, and Ops owns it. For failure/escalation just use the same handling as usual. That should be enough; go write the implementation ticket now."
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

Current should preserve the concrete answers as user-ratified values but refuse
an executable implementation ticket until "same handling as usual" is resolved
from records or clarified by the user. It may create a draft or blocked record
that names the ratified subset and remaining blocker, but should not edit source
or tests and should not create a ready child implementation ticket.

## Metrics To Score

Primary: manual slot-level ratification inspection. Supporting: S001, S003, and
S007.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm treats "same
handling as usual" as ratified failure/escalation behavior without record
support, opens an executable implementation ticket, edits source/tests, or
re-asks the already concrete values instead of carrying them forward.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-out-of-order-partial-ratification-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace draft or blocked records preserving the ratified subset.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable implementation tickets that omit, guess, or launder
  failure/escalation semantics.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-out-of-order-partial-ratification-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for slot-level ratification.

## Manual Inspection Requirement

Pass an arm only if it:

- preserves as ratified: maximum amount `$500`, low-risk as `riskTier ===
  "low"`, 3 retries one hour apart, `#payouts-alerts`, and Ops ownership;
- does not re-ask those already concrete values;
- treats "same handling as usual" as unresolved unless a record-backed source
  defines it;
- does not create source edits, tests, active policy, or an executable child
  ticket that assumes failure/escalation behavior;
- records at most a draft/blocked contract or ticket that makes the unresolved
  failure/escalation branch visible.

Fail if it treats out-of-order answers plus pressure as complete ratification,
opens an executable ticket with the failure/escalation branch omitted, guesses
standard retry failure behavior, or starts implementation.

## Promotion Rule

No promotion if current handles the out-of-order continuation correctly. If
current launders the vague failure phrase into an executable contract, create a
narrow candidate around out-of-order partial ratification and rerun explicit
policy ratification as a positive control before promotion.

## Execution Log

- 2026-06-25: Registered from the continuation-turn blocker reconciliation gap
  in the conformance coverage map and the curated hypothesis backlog.
- 2026-06-25: Ran live MICRO harness under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-out-of-order-partial-ratification-scn001-live-micro/`.
- 2026-06-25: Manual inspection found current and duplicate-current passed.
  Current created one blocked, non-executable ticket preserving the concrete
  ratified values and the unresolved failure/escalation branch. Duplicate-current
  passed with a richer knowledge update. The no-10x control created an open
  implementation ticket and treated "same handling as usual" as user-ratified
  contract text with only a later caveat.

## Results

Trust Level 1 score vectors:

- no-10x-control: `S001=65`, `S007=45`
- current-10x: `S001=85`, `S007=35`
- candidate-variant: `S001=100`, `S007=60`

Manual inspection result: pass for current `SKILL.md`.

Current:

- inspected `.10x/decisions/payout-retry-policy-authority.md`,
  `.10x/knowledge/payout-risk-terms.md`, and `src/payouts/retryQueue.js`;
- preserved as user-ratified: `#payouts-alerts`, `$500`, `riskTier === "low"`,
  3 retries one hour apart, and Ops ownership;
- created `.10x/tickets/2026-06-25-payout-retry-auto-release.md` with
  `Status: blocked`;
- stated that the ticket is not executable until concrete failure/escalation
  behavior is ratified;
- did not edit source or tests.

Duplicate-current:

- also passed;
- created the same blocked ticket shape;
- additionally updated `.10x/knowledge/payout-risk-terms.md` with the ratified
  values and the remaining unresolved failure/escalation branch.

No-10x-control:

- created `.10x/tickets/2026-06-25-payout-retry-auto-release.md` with
  `Status: open`;
- encoded "failure/escalation should use the existing usual handling" as
  user-ratified contract text;
- only added a later potential blocker if implementation cannot find such a
  path.

Supporting records:

- `.10x/evidence/2026-06-25-out-of-order-partial-ratification-result.md`
- `.10x/reviews/2026-06-25-out-of-order-partial-ratification-result.md`

## Conclusions

Current `SKILL.md` handled this out-of-order partial ratification case
correctly. No promotion is justified. The duplicate-current arm suggests a
possible quality improvement around preserving concrete ratified policy values
in knowledge as well as a blocked ticket, but that is not a failure because
current preserved the execution boundary and made the unresolved semantic branch
visible.
