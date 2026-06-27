Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-960-cancelled-ticket-history-not-active-authority-scn006-live-micro

## Experiment ID

EXP-20260624-960-cancelled-ticket-history-not-active-authority-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` treats cancelled tickets and their old evidence
as historical context, not active authority, when preparing the next executable
ticket from a cold record/source workspace.

## Motivation

Recent terminal-record experiments covered stale done tickets and old evidence.
Cancelled tickets are a distinct lifecycle state: they may contain tempting
implementation details and passing prototype evidence, but they should not
authorize current behavior unless a new active decision resurrects them.

## Method Tier

MICRO using a live Codex subject harness and tracked cold-start seed workspace.

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

- SCN-006: customer credit export active records include all approved production
  US customers, while a cancelled ticket, old evidence, source, and current test
  encode a stale enterprise-only filter.

Seed:

- `autoresearch/trial-seeds/cancelled-ticket-history-not-active-authority/raw.json`

Prompt:

```text
Cold-start this repository and prepare the next executable 10x child ticket for customer credit export work. Use only the record graph and source/tests; do not rely on prior chat. Do not edit source or tests in this turn.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-960-cancelled-ticket-history-not-active-authority-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/cancelled-ticket-history-not-active-authority/raw.json",
      "prompt": "Cold-start this repository and prepare the next executable 10x child ticket for customer credit export work. Use only the record graph and source/tests; do not rely on prior chat. Do not edit source or tests in this turn."
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

Current should inspect the active customer credit export spec, active
supersession decision, cancelled enterprise-only ticket, old evidence, source,
test, and package script. It should create one executable child ticket to align
source/tests to active records by removing the enterprise-only filter, adding
non-enterprise production coverage, excluding test/non-US/pending rows, and
preserving header/order. It should treat the cancelled ticket/evidence as
historical and avoid source/test edits.

## Metrics To Score

Primary: manual cancelled-record authority behavior. Supporting: S003 and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm treats the
cancelled ticket/evidence as active authority, silently trusts the stale current
test, asks the user for context records already contain, edits source/tests, or
creates broad unrelated work.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/160-cancelled-ticket-history-not-active-authority-scn006-live-micro/`;
- this research record execution log updates;
- subject workspace `.10x/tickets/` executable child ticket.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/160-cancelled-ticket-history-not-active-authority-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for cancelled-record authority behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active spec, active decision, cancelled ticket, old evidence, source,
  test, and package script;
- reconstructs active authority from the spec/decision;
- treats the cancelled ticket/evidence as historical, not current acceptance
  criteria;
- creates one executable child ticket to align source/tests to active records;
- includes acceptance criteria for approved production US enterprise and
  non-enterprise rows, test-account exclusion, non-US exclusion, pending-row
  exclusion, exact header/order, source-order preservation, and verification;
- avoids source/test edits in this turn.

Fail or downgrade if it asks for context that records answer, treats cancelled
acceptance criteria as current authority, silently trusts the current stale
test, creates unrelated work, ignores cancelled records, edits source/tests, or
omits source/test drift from the ticket.

## Promotion Rule

Promote only if current fails cancelled-record authority and a narrow candidate
can improve lifecycle-state handling without weakening ticket readiness or
overblocking coherent active records.

## Risks

- The prompt names the customer credit export work surface, so this is focused
  cold-start coverage rather than open-ended repository triage.
- no-10x-control removes inherited `.10x`, so its result is not a direct
  record-graph authority comparison.

## Execution Log

- 2026-06-24: Registered as a cancelled-ticket lifecycle complement to the
  stale done-ticket and cold-start terminal-record experiments.
- 2026-06-24: Ran the live MICRO to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/160-cancelled-ticket-history-not-active-authority-scn006-live-micro/`.
  Automated Trust Level 1 S003 scores were `100` for all arms. Manual
  inspection found both 10x arms passed cancelled-record authority and edited no
  source/test files.

## Findings

- `current-10x` inspected the active specification, active supersession
  decision, cancelled ticket, old evidence, implementation, test, and package
  script.
- `current-10x` created
  `.10x/tickets/2026-06-24-align-customer-credit-export.md` in the archived
  subject workspace.
- The current ticket treated the cancelled enterprise-only ticket and prototype
  evidence as historical, identified current source/test drift, and scoped one
  executable child ticket to align source/tests to active records.
- `candidate-variant` duplicated current `SKILL.md` and also passed, creating
  `.10x/tickets/2026-06-24-align-customer-credit-export-with-active-spec.md`.
- Direct `diff -u` checks confirmed both 10x arms left
  `src/credits/exportCredits.js` and `src/credits/exportCredits.test.js`
  byte-identical to the seed.
- `no-10x-control` had inherited `.10x` removed and created an unrelated CSV
  escaping child ticket that preserved current stale enterprise-only filtering.
  Its S003 `100` is not evidence of record graph lifecycle authority.

## Conclusions

Current `SKILL.md` passes this cancelled-ticket lifecycle authority MICRO. It
reconstructed the active customer credit export behavior from records and
source/tests, treated cancelled work as historical context, and opened one
alignment ticket without editing source/tests. No `SKILL.md` promotion is
justified.

This strengthens record quality over time for a lifecycle state distinct from
done/superseded records. Remaining record lifecycle work should combine
cancelled, done, superseded, and stale research surfaces in one broader
multi-surface cold-start workspace.

## Result Records

- `.10x/evidence/2026-06-24-cancelled-ticket-history-not-active-authority-result.md`
- `.10x/reviews/2026-06-24-cancelled-ticket-history-not-active-authority-result.md`
