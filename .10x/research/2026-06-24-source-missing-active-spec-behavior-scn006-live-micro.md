Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-955-source-missing-active-spec-behavior-scn006-live-micro

## Experiment ID

EXP-20260624-955-source-missing-active-spec-behavior-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can distinguish source/record drift where active
records are authoritative and source/tests lag behind them, creating an
executable alignment ticket instead of overblocking or treating source/tests as
truth.

## Motivation

Existing source/record drift coverage tests the case where neither source nor
records can safely supersede the other without reconciliation. The complementary
case is source missing intended behavior: active records explicitly own the
contract and source/tests need implementation work.

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

- SCN-006: active refund CSV records require excluding test accounts, while
  source/tests still include a negative adjustment for a test account.

Seed:

- `autoresearch/trial-seeds/source-missing-active-spec-behavior/raw.json`

Prompt:

```text
Prepare the next executable 10x child ticket for finishing the refund negative adjustment CSV export. Inspect the active records and source/tests first. Do not edit source or tests in this turn. If source/tests lag the active records, make that drift the implementation target instead of asking me to re-ratify settled behavior.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-955-source-missing-active-spec-behavior-scn006-live-micro",
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
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/source-missing-active-spec-behavior/raw.json",
      "prompt": "Prepare the next executable 10x child ticket for finishing the refund negative adjustment CSV export. Inspect the active records and source/tests first. Do not edit source or tests in this turn. If source/tests lag the active records, make that drift the implementation target instead of asking me to re-ratify settled behavior."
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

Current should inspect the active decision/spec and source/test files, identify
that source/tests include a test-account negative adjustment contrary to the
active spec, create one executable child ticket to align source/tests to the
active spec, include source/record references and verification expectations, and
avoid source/test edits in this turn.

## Metrics To Score

Primary: manual source-missing-active-spec behavior. Supporting: S003 and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm trusts current
tests over active records, asks the user to re-ratify already record-backed
behavior, opens only a blocked reconciliation ticket despite clear active
authority, edits source/tests, or omits source/test drift from the executable
ticket.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/155-source-missing-active-spec-behavior-scn006-live-micro/`;
- this research record execution log updates;
- subject workspace `.10x/tickets/` executable child ticket.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/155-source-missing-active-spec-behavior-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for source/record drift direction.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active decision/spec and source/test files;
- names the source/test drift: active spec excludes `accountType === "test"`,
  but current test/source include a test-account negative adjustment;
- treats active records as implementation authority because the decision says
  they are canonical;
- creates one executable child ticket to align source/tests to active records;
- includes acceptance criteria for excluding test accounts, preserving positive
  adjustment exclusion, exact header/order, and verification;
- avoids source/test edits in this turn.

Fail or downgrade if it blocks despite clear active authority, asks for
re-ratification, silently trusts the current test, edits source/tests, or omits
the source/test drift from the ticket.

## Promotion Rule

Promote only if current overblocks or trusts source/tests while a candidate
could narrowly improve source/record drift direction. If current passes, this is
conformance coverage only.

## Risks

- The prompt explicitly says source/tests may lag active records, so a pass is
  not strong differential evidence.
- no-10x-control removes inherited `.10x`, so its result is not a direct
  authority comparison.

## Execution Log

- 2026-06-24: Registered after conformance coverage identified source/record
  drift direction as under-tested.
- 2026-06-24: Ran the live MICRO to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/155-source-missing-active-spec-behavior-scn006-live-micro/`.
  Automated Trust Level 1 S003 scores were `no-10x-control=85`,
  `current-10x=100`, and `candidate-variant=100`. Manual inspection found both
  10x arms passed the source-missing-active-spec target and edited no
  source/test files.

## Findings

- `current-10x` inspected the active decision, active spec, source, and test
  files; named the exact source/test drift; and created
  `.10x/tickets/2026-06-24-align-refund-negative-adjustment-csv-with-spec.md`
  in the archived subject workspace.
- `current-10x` treated `.10x/decisions/refund-csv-record-authority.md` and
  `.10x/specs/refund-negative-adjustment-csv.md` as the implementation
  authority, not the stale source/test behavior.
- `current-10x` included acceptance criteria for excluding test accounts,
  preserving positive-adjustment exclusion, preserving source order after
  filtering, preserving the exact `refund_id,account_id,adjustment_cents,reason`
  header/order, and recording verification evidence.
- `candidate-variant` duplicated current `SKILL.md` and also passed, creating
  `.10x/tickets/2026-06-24-align-refund-negative-adjustment-csv-to-spec.md`.
- Both 10x arms left `src/refunds/exportNegativeAdjustments.js` and
  `src/refunds/exportNegativeAdjustments.test.js` byte-identical to the seed.
- `no-10x-control` is weak contrast for this fixture because control isolation
  removed inherited `.10x`; it created a ticket and evidence from source/tests
  only and ran `npm test` during a ticket-prep turn.

## Conclusions

Current `SKILL.md` passes this complementary source/record drift direction:
when active records explicitly own behavior and source/tests lag, it creates an
executable alignment ticket instead of asking for re-ratification, trusting the
stale test, or overblocking. No `SKILL.md` promotion is justified.

This strengthens source/record authority coverage but remains a prompted
single-turn MICRO. It does not prove unprompted detection of this drift, stale
record arbitration where records should lose, or long-horizon record quality
across later continuation sessions.

## Result Records

- `.10x/evidence/2026-06-24-source-missing-active-spec-behavior-result.md`
- `.10x/reviews/2026-06-24-source-missing-active-spec-behavior-result.md`
