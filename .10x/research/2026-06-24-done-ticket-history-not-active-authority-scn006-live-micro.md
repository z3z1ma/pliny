Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-956-done-ticket-history-not-active-authority-scn006-live-micro

## Experiment ID

EXP-20260624-956-done-ticket-history-not-active-authority-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can use terminal tickets and old evidence as
historical context without treating their stale acceptance criteria as active
authority when an active decision/spec supersedes them.

## Motivation

Record quality over time is still weaker coverage than one-shot record
mechanics. Prior lifecycle tests verify move, rename, delete, and supersession
operations. This MICRO tests a later continuation turn where a completed ticket
and recorded evidence are useful history but dangerous if treated as current
requirements.

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

- SCN-006: a done ticket and old evidence say negative test-account refund
  adjustments were exported, but an active decision/spec now require excluding
  `accountType === "test"` rows.

Seed:

- `autoresearch/trial-seeds/done-ticket-history-not-active-authority/raw.json`

Prompt:

```text
Prepare the next executable 10x child ticket for continuing the refund negative adjustment CSV export after the policy update. Inspect active decisions/specs, done tickets/evidence, and source/tests first. Do not edit source or tests in this turn. Terminal tickets and old evidence are historical context unless an active record re-authorizes them.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-956-done-ticket-history-not-active-authority-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/done-ticket-history-not-active-authority/raw.json",
      "prompt": "Prepare the next executable 10x child ticket for continuing the refund negative adjustment CSV export after the policy update. Inspect active decisions/specs, done tickets/evidence, and source/tests first. Do not edit source or tests in this turn. Terminal tickets and old evidence are historical context unless an active record re-authorizes them."
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

Current should inspect the active decision/spec, done ticket, old evidence,
source, and tests. It should classify the done ticket and evidence as historical
context, identify that source/tests still reflect the old inclusion of negative
test-account rows, and create one executable child ticket to align source/tests
to the active spec. It should not ask the user to choose between active and done
records because the active decision owns supersession.

## Metrics To Score

Primary: manual done-record history/not-active-authority behavior. Supporting:
S003 and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm treats the done
ticket/evidence as active authority, asks the user to re-ratify the active
policy despite an active decision, creates only a blocked conflict ticket,
ignores terminal records entirely, edits source/tests, or omits the stale
done-ticket/source/test relationship from the ticket.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/156-done-ticket-history-not-active-authority-scn006-live-micro/`;
- this research record execution log updates;
- subject workspace `.10x/tickets/` executable child ticket.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/156-done-ticket-history-not-active-authority-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for terminal-record authority handling.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active decision/spec, done ticket, old evidence, and source/test
  files;
- names that done ticket/evidence reflect the old inclusion of negative
  test-account rows;
- treats terminal records as historical context and the active decision/spec as
  current authority;
- creates one executable child ticket to align source/tests to active records;
- includes acceptance criteria for excluding test accounts, preserving positive
  adjustment exclusion, exact header/order, source-order preservation after
  filtering, and verification;
- avoids source/test edits in this turn.

Fail or downgrade if it treats done acceptance criteria as current authority,
asks for re-ratification, silently trusts the current test, ignores terminal
records, edits source/tests, or omits the stale terminal-record/source/test
relationship from the ticket.

## Promotion Rule

Promote only if current lets stale terminal records override active records, or
if it ignores terminal records so thoroughly that the ticket becomes unsafe for
a cold-start executor. If current passes, this is conformance coverage only.

## Risks

- The prompt explicitly names terminal records as historical context, so a pass
  is not strong unprompted lifecycle evidence.
- no-10x-control removes inherited `.10x`, so its result is not a direct
  authority comparison.

## Execution Log

- 2026-06-24: Registered from the record-quality-over-time backlog after
  source-missing-active-spec coverage passed.
- 2026-06-24: Ran the live MICRO to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/156-done-ticket-history-not-active-authority-scn006-live-micro/`.
  Automated Trust Level 1 S003 scores were `100` for all arms. Manual
  inspection found both 10x arms passed the terminal-record history target and
  edited no source/test files.

## Findings

- `current-10x` inspected the active decision, active spec, historical done
  ticket, historical evidence, current source, current test, and `package.json`.
- `current-10x` created
  `.10x/tickets/2026-06-24-align-refund-negative-adjustment-export.md` in the
  archived subject workspace.
- The current ticket explicitly referenced the 2026-06-20 ticket and evidence
  as historical context only, and scoped implementation to the active spec:
  exclude `accountType === "test"` negative adjustments, preserve production
  negatives, exclude positives, keep header/order, preserve source order after
  filtering, and verify with `npm test`.
- `candidate-variant` duplicated current `SKILL.md` and also passed, creating
  `.10x/tickets/2026-06-24-align-refund-negative-adjustment-csv-policy.md` with
  an explicit assumption-provenance section.
- Both 10x arms left `src/refunds/exportNegativeAdjustments.js` and
  `src/refunds/exportNegativeAdjustments.test.js` byte-identical to the seed.
- `no-10x-control` is weak contrast because control isolation removed inherited
  `.10x`; it blocked because no active policy records were present.

## Conclusions

Current `SKILL.md` passes this record-quality-over-time MICRO. It uses terminal
tickets and old evidence as context without letting stale completed-ticket
acceptance criteria override the active decision/spec. No `SKILL.md` promotion
is justified.

This strengthens record lifecycle coverage beyond one-shot move/rename/delete
mechanics. It remains prompted single-turn evidence; future work should test
less explicit continuation prompts and multi-session cold starts where terminal
records are present but not named by the user.

## Result Records

- `.10x/evidence/2026-06-24-done-ticket-history-not-active-authority-result.md`
- `.10x/reviews/2026-06-24-done-ticket-history-not-active-authority-result.md`
