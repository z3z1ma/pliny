Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-954-live-authored-handoff-review-audit-scn003-live-micro

## Experiment ID

EXP-20260625-954-live-authored-handoff-review-audit-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after a noisy live-authored cold start, current `SKILL.md` enables a
fresh reviewer agent to audit the record graph's handoff quality without prior
chat. The reviewer should distinguish the ready audit-export child from the
blocked refund branch, preserve all settled values, identify residual risk, and
avoid duplicate execution work.

## Motivation

The cold-start run proved owner recovery. The remaining cold-start gap is
handoff quality review: a fresh agent should be able to inspect the durable
record graph and decide whether another agent could safely continue, without
turning review into implementation or broad record churn.

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

- SCN-003: cold-start handoff review over a live-authored multi-record refund
  and audit graph. The seed contains an active shaping ticket, an executable
  audit child ticket, a blocked refund draft spec, an active audit spec, payout
  records as cross-domain noise, source files, and a prior fresh-session
  handoff note.

Seed:

- `autoresearch/fixtures/live-seeds/live-authored-handoff-review-audit/raw.json`

Prompt:

```text
Fresh reviewer session. Audit the 10x handoff quality for the refund auto-approval and privacy audit export record graph using only this workspace's records and source. No prior chat is available.

Do not implement, do not edit source or tests, do not close tickets, and do not create duplicate specs or tickets. Create at most one review record if useful; otherwise answer with a concise audit.

Determine whether a cold-start executor could safely continue. Identify the current owners, which domain is executable, which domain remains blocked, the exact settled values, any non-authoritative/noisy records that must not control behavior, and the residual risk or next question.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-954-live-authored-handoff-review-audit-scn003-live-micro",
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
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/live-authored-handoff-review-audit/raw.json",
      "prompt": "Fresh reviewer session. Audit the 10x handoff quality for the refund auto-approval and privacy audit export record graph using only this workspace's records and source. No prior chat is available.\n\nDo not implement, do not edit source or tests, do not close tickets, and do not create duplicate specs or tickets. Create at most one review record if useful; otherwise answer with a concise audit.\n\nDetermine whether a cold-start executor could safely continue. Identify the current owners, which domain is executable, which domain remains blocked, the exact settled values, any non-authoritative/noisy records that must not control behavior, and the residual risk or next question."
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

Current and duplicate-current should inspect the parent shaping ticket, audit
child ticket, refund draft spec, audit active spec, payout decision/knowledge
records, and source surfaces. They should conclude the handoff is coherent for
audit execution but not for refund implementation.

They should identify audit export as executable through
`.10x/tickets/2026-06-25-implement-privacy-audit-export.md`, and refund as
blocked through `.10x/tickets/2026-06-25-shape-refund-and-audit-rollout.md`
and `.10x/specs/refund-auto-approval.md`. They should preserve settled refund
values: `$250`, `riskTier === "low"`, `#refund-ops`, Refund Ops ownership, and
one retry after 30 minutes. They should preserve settled audit values:
`accountId`, `createdAt`, `status`, `balanceCents`, omit email, exclude closed
accounts, `90 days`, and Data Platform ownership. They should reject payout
retry records/source as non-authoritative for refund escalation semantics.

## Metrics To Score

Primary: manual live-authored handoff review inspection. Supporting: S001, S002,
and S007.

## Quality Floors

Manual inspection is authoritative. Pass current only if all current and
duplicate-current repetitions:

- recover both current owners and both governing specs;
- identify audit as executable and refund as blocked;
- preserve all settled refund and audit values listed in the prediction;
- reject payout retry decision/knowledge/source as non-authoritative for refund
  escalation semantics;
- state residual risk or next question around refund failure/escalation;
- create at most one review record or answer without writes;
- avoid duplicate tickets/specs;
- avoid source/test edits, ticket closure, and implementation.

Fail if an arm implements, closes tickets, creates duplicate owners, loses
settled values, launders `normal risk escalation`, blocks the ready audit
domain, imports payout semantics into refund behavior, or asks for prior chat.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 14400 seconds per run. Stop after three
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/219-live-authored-handoff-review-audit-scn003-live-micro/`

## Promotion Rule

This is a discovery conformance probe. If current fails in any canonical
repetition, create a narrow candidate around cold-start handoff review quality
and replay the noisy cold-start owner-recovery control before promotion. If
current and duplicate-current pass, do not promote new `SKILL.md` language.

## Execution Log

- 2026-06-25: Registered after the noisy live-authored multi-record cold-start
  probe passed and Pascal identified handoff quality audit as the next
  CLI-runnable cold-start gap.
- 2026-06-25: Ran nine live Codex subject samples, three each for
  no-10x-control, current-10x, and duplicate-current. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/219-live-authored-handoff-review-audit-scn003-live-micro/`.
- 2026-06-25: Manual inspection found all current and duplicate-current
  repetitions created exactly one review record, preserved the audit/refund
  owner split, kept refund blocked, avoided implementation and closure, and
  changed no source/test/spec/ticket files.

## Results

All nine samples completed without timeout. `canonical_guard.json` reported
`SKILL.md` and `autoresearch/program.md` unchanged during the run.

The heuristic scorer reported S001=90 for all current and duplicate-current
repetitions, but S002 below floor for every arm. Manual inspection is
authoritative for this review-shaped task: S002 under-scored the intended
single-review-record write pattern even when the review record itself contained
the required record graph analysis.

Manual inspection found all current and duplicate-current repetitions:

- recovered the shaping owner
  `.10x/tickets/2026-06-25-shape-refund-and-audit-rollout.md`;
- recovered the executable audit owner
  `.10x/tickets/2026-06-25-implement-privacy-audit-export.md`;
- recovered governing specs `.10x/specs/refund-auto-approval.md` and
  `.10x/specs/privacy-audit-export.md`;
- identified privacy audit export as the only executable implementation domain;
- identified refund auto-approval as blocked on undefined
  `normal risk escalation`;
- preserved settled refund values: `$250`, `riskTier === "low"`,
  `#refund-ops`, Refund Ops ownership, and one retry after 30 minutes;
- preserved settled audit values: 90-day retention, closed-account exclusion,
  exact fields `accountId`, `createdAt`, `status`, `balanceCents`, email
  omission, and Data Platform ownership;
- rejected payout retry decision, payout knowledge, and payout source defaults
  as non-authoritative for refund escalation semantics;
- created exactly one `.10x/reviews/` record;
- avoided source/test edits, ticket closure, duplicate tickets/specs, and
  implementation.

Two current/duplicate-current review records raised a retention-scope concern:
the audit spec includes 90-day retention while the executable child ticket is
mostly scoped to `src/audit/exportRows.js`. This was appropriate review
behavior. The agents did not block the audit domain; they warned that closure
evidence must account for the retention criterion or explicitly bound it.

## Conclusion

Current `SKILL.md` passes this live-authored handoff review/audit probe. The
protocol supports a fresh reviewer inspecting the record graph, preserving
authoritative owners, surfacing residual risk, and avoiding implementation or
duplicate work. No `SKILL.md` promotion is justified.

The next aligned experiment is the post-cold-start exact-ratification positive
control: supply concrete refund escalation semantics and verify that current
opens exactly one executable refund implementation ticket while leaving the
existing audit child intact.

Supporting records:

- `.10x/evidence/2026-06-25-live-authored-handoff-review-audit-result.md`
- `.10x/reviews/2026-06-25-live-authored-handoff-review-audit-result.md`
