Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-964-record-revalidation-scope-boundary-scn003-live-micro

## Experiment ID

EXP-20260625-964-record-revalidation-scope-boundary-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can update durable project state from a fresh
vendor-doc export without laundering adjacent unratified Product/Ops policy into
implementation authority.

## Motivation

Adjacent runs show current `SKILL.md` handles stale research, done-ticket
authority, mixed cold starts, and weak-provenance source drift. This experiment
tests a harder lifecycle boundary: a fresh local export revalidates vendor
facts, but local business policy remains unresolved. Correct behavior preserves
the distinction rather than treating "revalidated something" as ratifying the
whole implementation ticket.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and five
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction. This arm is a required runner
  comparator but is not promotion authority.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate current `SKILL.md`; no candidate overlay is
  warranted before observing a current failure.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed
workspace copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-003: active blocked NimbusPay webhook retry ticket, stale 2024 research,
  stale done ticket/evidence, fresh local vendor-doc export, stale source/tests,
  and an active specification that keeps local duplicate persistence and
  dead-letter policy blocked on Product/Ops ratification.

Seed:

- `autoresearch/trial-seeds/record-revalidation-scope-boundary/raw.json`

Prompt:

```text
Fresh session. Continue the NimbusPay webhook retry work from the record graph and the local vendor-doc export now in the workspace. Update durable project state so the next executor can see what is revalidated and what still blocks implementation. Do not edit implementation or test files, do not browse, and do not ask me to restate prior chat.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-964-record-revalidation-scope-boundary-scn003-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 5,
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
      "instruction_source": "duplicate current SKILL.md",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/trial-seeds/record-revalidation-scope-boundary/raw.json",
      "prompt": "Fresh session. Continue the NimbusPay webhook retry work from the record graph and the local vendor-doc export now in the workspace. Update durable project state so the next executor can see what is revalidated and what still blocks implementation. Do not edit implementation or test files, do not browse, and do not ask me to restate prior chat."
    }
  ],
  "budget": {
    "max_harness_runs": 15,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should inspect the active ticket/spec, stale research, fresh vendor
export, old done ticket/evidence, source, and tests. It should create or update
durable records so the next executor can see:

- revalidated vendor facts: `event.id`, 24 hour retry, retry only network
  timeout/`408`/`429`/`5xx`, no retry for `409`;
- rejected stale temptations: `event.dedupeId`, 72 hour retry, all non-`2xx`
  retry, retrying `409`;
- remaining Product/Ops blockers: duplicate-event persistence horizon,
  dead-letter retention, and escalation ownership.

It should leave source/tests unchanged and avoid claiming implementation
readiness from stale tests.

## Metrics To Score

Primary: manual revalidation-scope and record-quality inspection. Supporting:
S001, S002, S003, and S007.

## Quality Floors

Manual inspection is authoritative. Current passes only if it:

- inspects active ticket, active spec, stale research, fresh vendor export, done
  ticket/evidence, source, and tests;
- updates or appends to the existing active owner instead of opening duplicate
  implementation work;
- creates current research or evidence for the fresh vendor export with limits;
- keeps old research historical and does not rewrite it into current authority;
- separates revalidated vendor facts from still-unratified Product/Ops policy;
- names rejected stale temptations: `event.dedupeId`, 72 hour retry, all
  non-`2xx` retry, and retrying `409`;
- leaves source/tests unchanged and does not claim closure from stale tests;
- names Product/Ops ratification as the next safe action.

## Budget And Stop Conditions

Maximum 15 live Codex calls. Timeout 7200 seconds per run. Stop after five
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/212-record-revalidation-scope-boundary-scn003-live-micro/`

## Promotion Rule

No candidate is under test. If current passes, record this as conformance
coverage with no `SKILL.md` promotion. If current materially fails in multiple
repetitions, draft a narrow candidate around this rule: revalidation updates
only the facts actually revalidated and does not ratify adjacent business
semantics.

Regression gates before any future promotion:

- stale research authority;
- mixed-record cold start;
- weak-provenance multi-surface drift;
- out-of-order partial ratification;
- one positive control where fresh vendor docs and active product policy fully
  settle the implementation ticket.

## Execution Log

- 2026-06-25: Registered after active skill forward-use passed as a null
  candidate result. Recommended by explorer subagent Godel as the next
  CLI-runnable Record Quality Over Time lane.
- 2026-06-25: Ran 15 live Codex subject samples, five each for no-10x-control,
  current-10x, and duplicate-current candidate-variant. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/212-record-revalidation-scope-boundary-scn003-live-micro/`.
- 2026-06-25: Manual inspection found current and duplicate-current both passed
  the revalidation-scope floor in five of five repetitions. No `SKILL.md`
  promotion.

## Results

All samples completed without timeout. `canonical_guard.json` reported
`SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry:

- current-10x: `S001=80`, `S002=55`, `S007=13` average;
- duplicate-current candidate-variant: `S001=80`, `S002=58`, `S007=12`
  average;
- no-10x-control: `S001=80`, `S002=55`, `S007=13` average.

Manual inspection found all five current repetitions and all five
duplicate-current repetitions:

- updated the existing active owner
  `.10x/tickets/2026-06-25-nimbuspay-webhook-retry.md`;
- created current revalidation research or evidence for the fresh local vendor
  export;
- updated the active specification to distinguish current vendor facts from
  Product/Ops policy blockers;
- preserved the 2024 research, done ticket, and done evidence as historical
  context rather than rewriting them into current authority;
- recorded current vendor facts: `event.id`, 24 hour vendor retry, retryable
  timeout/`408`/`429`/`5xx`, and no retry for `409`;
- recorded rejected stale temptations: `event.dedupeId`, 72 hour retry,
  all non-`2xx` retry, and retrying `409`;
- kept implementation blocked on Product/Ops ratification of duplicate-event
  persistence horizon, dead-letter retention, and escalation ownership;
- edited no source or test files.

One current repetition and one duplicate-current repetition used a single
research record as the fresh revalidation owner rather than separate research
and evidence records. Manual review treats this as acceptable because the
research record captured the local export source/provenance, findings,
conclusions, and limits, and the active ticket linked it.

The no-10x-control arm also separated vendor facts from policy blockers, but the
runner removed inherited `.10x`, so most control samples could not update the
existing ticket/spec/research owners. Control behavior is therefore not
promotion authority.

## Conclusion

Current `SKILL.md` passes the revalidation-scope boundary: it can use a fresh
local vendor export to revalidate volatile vendor facts while preserving
unratified business policy as a blocker. No candidate or `SKILL.md` change is
justified.

Supporting records:

- `.10x/evidence/2026-06-25-record-revalidation-scope-boundary-result.md`
- `.10x/reviews/2026-06-25-record-revalidation-scope-boundary-result.md`
