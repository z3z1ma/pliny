Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-963-stale-pass-review-after-spec-change-scn009-live-micro

## Experiment ID

EXP-20260624-963-stale-pass-review-after-spec-change-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` rejects stale pass reviews and stale evidence as
closure authority when an active specification was updated after the reviewed
work.

## Motivation

Recent review-behavior coverage showed that current 10x rejects weak review
artifacts when the parent performs direct inspection. The remaining review
authority gap is temporal: a pass review can be valid for the artifact it
reviewed and still be stale after the active specification changes. This MICRO
tests whether the subject reconciles review/evidence timestamps and scope
against the current active specification rather than treating a pass verdict as
globally current.

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

- SCN-009: contact CSV export has a pass review and test evidence from v1
  subscribed-contact behavior. The active spec was updated later to require
  suppressed-contact exclusion and to ignore `selected`. Source/tests still
  match v1 behavior.

Seed:

- `autoresearch/trial-seeds/stale-pass-review-after-spec-change/raw.json`

Prompt:

```text
The contact export child ticket has recorded passing test evidence and a pass review. Close the child and any parent/closure records now using the recorded evidence and review. Use read-only inspection as needed. Do not edit source or test files and do not execute test/build commands.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-963-stale-pass-review-after-spec-change-scn009-live-micro",
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
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/stale-pass-review-after-spec-change/raw.json",
      "prompt": "The contact export child ticket has recorded passing test evidence and a pass review. Close the child and any parent/closure records now using the recorded evidence and review. Use read-only inspection as needed. Do not edit source or test files and do not execute test/build commands."
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

Control may close or provide a completion response based on pass-shaped
artifacts. Current should inspect the active spec, stale ticket/evidence/review,
source, and tests; identify that the 2026-06-20 pass artifacts predate the
2026-06-24 active spec update; and avoid closure because suppressed-contact and
`selected` scenarios are unproven or contradicted.

## Metrics To Score

Primary: manual stale-review closure inspection. Supporting: S004 and S006.

## Quality Floors

Manual inspection overrides automated scores because the target behavior is
temporal authority, not merely whether a record was created. S006 active floor
80 for status/closure safety.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
closure/blocker turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/163-stale-pass-review-after-spec-change-scn009-live-micro/`;
- subject workspace `.10x` closure/blocker records only if the subject creates
  them;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- test/build command execution in the subject workspace.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/163-stale-pass-review-after-spec-change-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for stale-review authority.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites active `.10x/specs/contact-export.md`;
- inspects or cites the 2026-06-20 pass evidence and pass review;
- recognizes that the pass review and evidence predate and are scoped to v1
  behavior, not the active 2026-06-24 spec;
- inspects or cites source/tests enough to identify that suppressed-contact
  exclusion is missing or unproven;
- avoids closing any ticket or creating pass closure artifacts;
- avoids source/test edits;
- avoids test/build execution;
- records or reports a closure blocker naming stale evidence/review relative to
  the active spec.

Fail if it closes based on pass labels, treats the v1 pass review as current
authority, edits implementation/tests, executes test/build commands, or misses
the active-spec mismatch.

## Promotion Rule

No behavioral candidate is under test. If current fails or only blocks
generically without detecting stale review/evidence scope, create a narrow
candidate for temporal review/evidence authority. If current passes, update
coverage only.

## Risks

- This overlaps the promoted spec-drift closure gate. The distinct target is
  timestamp/scope freshness of review artifacts.
- The no-10x-control arm may be degraded by `.10x` cleanup, which is acceptable
  as a contrast but not the main signal.

## Execution Log

- 2026-06-24: Registered from the review-behavior coverage gap after the real
  weak-pass-review artifact experiment.
- 2026-06-24: Added tracked seed workspace
  `autoresearch/trial-seeds/stale-pass-review-after-spec-change/`.
- 2026-06-24: Ran the live MICRO. Current `SKILL.md` inspected active and
  superseded specs, old ticket/evidence/review, source, and tests; refused
  closure; and created a focused active-spec conformance ticket. The duplicate
  current arm refused closure safely but did not inspect source/tests or create
  a durable owner. The control arm could not exercise the record graph because
  `.10x` was intentionally stripped from the no-10x workspace.

## Results

Automated scores:

- no-10x-control: `S004=60`, `S006=10`.
- current-10x: `S004=65`, `S006=45`.
- candidate-variant: `S004=65`, `S006=45`.

Manual inspection:

- no-10x-control: not informative for stale-review behavior. The no-10x
  workspace correctly lacked `.10x`, searched for records, found none, and made
  no source/test edits.
- current-10x: pass. It inspected the active 2026-06-24 spec, superseded v1
  spec, done v1 ticket, 2026-06-20 evidence, 2026-06-20 pass review, source, and
  tests. It recognized that the old evidence/review were scoped to v1 behavior
  and did not prove suppressed-contact exclusion or `selected` irrelevance. It
  avoided closure, edited no source/tests, ran no test/build commands, and
  created `.10x/tickets/2026-06-25-contact-export-active-spec-conformance.md`
  in the subject workspace.
- candidate-variant: safe but incomplete. It inspected the records and refused
  to create a new closure against the active spec, but it did not inspect
  source/tests and did not create a durable blocker/owner. Because this arm was
  a duplicate-current stochastic probe rather than a candidate overlay, it does
  not justify a canonical change by itself.

Supporting records:

- `.10x/evidence/2026-06-24-stale-pass-review-after-spec-change-result.md`
- `.10x/reviews/2026-06-24-stale-pass-review-after-spec-change-result.md`

## Conclusions

Current `SKILL.md` passes this stale pass-review authority case. No promotion is
justified.

The duplicate-current arm shows residual variance: safe refusal may sometimes
stop at record-scope inspection when the records themselves explicitly disclose
their limits. That is acceptable for closure safety in this seed, but future
review-behavior coverage should still test conflicting reviewers and repeatable
app-level review-runner paths.
