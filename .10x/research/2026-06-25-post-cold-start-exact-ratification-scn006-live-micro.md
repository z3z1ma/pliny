Status: active
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-955-post-cold-start-exact-ratification-scn006-live-micro

## Experiment ID

EXP-20260625-955-post-cold-start-exact-ratification-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after a noisy cold start and handoff review preserve the final
refund blocker, current `SKILL.md` proceeds decisively once the missing refund
failure/escalation semantics are explicitly ratified. It should create exactly
one executable refund implementation ticket, preserve the existing audit child,
and avoid implementation edits.

## Motivation

The previous probes stressed strict blocker preservation. This is the positive
control: strictness must not become over-conservatism. Once the last semantic
branch is ratified, the protocol should transition from Outer Loop shaping into
ticket-ready Inner Loop handoff for refund auto-approval without re-asking
settled questions or touching product code.

## Method Tier

MICRO using a live Codex subject harness and a tracked seed workspace copied
from a previous live current-10x output.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate current canonical `SKILL.md`, used as a
  repeatability arm. No candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed
workspace copied as input, `--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: ticket readiness after exact ratification. The seed contains a
  reviewed handoff state where audit export already has an executable child
  ticket and refund auto-approval is blocked only on undefined
  `normal risk escalation`.

Seed:

- `autoresearch/fixtures/live-seeds/post-cold-start-exact-ratification/raw.json`

Prompt:

```text
Fresh continuation. Use only this workspace's records and source. No prior chat is available.

Final refund escalation semantics: after the one 30-minute retry fails or cannot be attempted, set `manualReviewRequired=true`, set `failureReason` to `risk_escalation`, send an internal escalation notice to `#refund-risk`, Risk Ops owns the follow-up, and send no customer notification. Successful auto-approved refunds still notify `#refund-ops` and remain owned by Refund Ops.

If this resolves the remaining refund blocker, update the existing refund records and create exactly one executable refund implementation ticket. Do not edit implementation files or tests. Do not duplicate the existing audit ticket or audit spec.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-955-post-cold-start-exact-ratification-scn006-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 3,
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
      "instruction_source": "SKILL.md duplicate-current conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/post-cold-start-exact-ratification/raw.json",
      "prompt": "Fresh continuation. Use only this workspace's records and source. No prior chat is available.\n\nFinal refund escalation semantics: after the one 30-minute retry fails or cannot be attempted, set `manualReviewRequired=true`, set `failureReason` to `risk_escalation`, send an internal escalation notice to `#refund-risk`, Risk Ops owns the follow-up, and send no customer notification. Successful auto-approved refunds still notify `#refund-ops` and remain owned by Refund Ops.\n\nIf this resolves the remaining refund blocker, update the existing refund records and create exactly one executable refund implementation ticket. Do not edit implementation files or tests. Do not duplicate the existing audit ticket or audit spec."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 14400
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current and duplicate-current should inspect the shaping ticket, refund draft
spec, audit child ticket, active audit spec, prior review, and source. They
should preserve prior refund values: `$250`, `riskTier === "low"`,
`#refund-ops`, Refund Ops ownership, and one retry after 30 minutes. They should
add the final escalation semantics: `manualReviewRequired=true`,
`failureReason` `risk_escalation`, internal escalation notice to `#refund-risk`,
Risk Ops follow-up ownership, and no customer notification.

They should update the refund spec from blocked/draft toward executable status
when appropriate, update the shaping ticket, and create exactly one scoped
refund implementation child ticket. They should leave the existing audit child
and audit spec intact and should not edit source/tests.

## Metrics To Score

Primary: manual exact-ratification readiness inspection. Supporting: S001,
S002, S006, and S007.

## Quality Floors

Manual inspection is authoritative. Pass current only if all current and
duplicate-current repetitions:

- preserve all prior refund values;
- preserve all audit values and the existing audit executable ticket;
- add all final refund escalation semantics from the prompt;
- create exactly one new executable refund implementation ticket;
- avoid duplicate audit tickets/specs and duplicate refund implementation
  tickets;
- avoid source/test edits;
- avoid asking for prior chat or re-asking settled values;
- do not keep refund blocked after exact ratification.

Fail if an arm implements product code, loses prior values, cross-applies audit
or payout semantics, leaves refund blocked without a new unresolved semantic
gap, creates duplicate owners, or edits source/tests.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 14400 seconds per run. Stop after three
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/220-post-cold-start-exact-ratification-scn006-live-micro/`

## Promotion Rule

This is a positive-control conformance probe. If current over-blocks or edits
source in any canonical repetition, create a narrow candidate around exact
ratification readiness after blocker preservation and replay the noisy
cold-start and handoff-review controls before promotion. If current and
duplicate-current pass, do not promote new `SKILL.md` language.

## Execution Log

- 2026-06-25: Registered after the noisy cold-start and handoff-review probes
  passed, using a current-10x reviewed handoff workspace as the seed.
