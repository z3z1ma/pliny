Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-961-mixed-record-authority-cold-start-scn006-live-micro

## Experiment ID

EXP-20260624-961-mixed-record-authority-cold-start-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can cold-start from a mixed record graph that
contains active, done, cancelled, superseded, stale research, old evidence, and
stale source/test signals, then select the current durable authority without
inventing or overblocking.

## Motivation

Single-state lifecycle tests now cover stale done tickets, cancelled tickets,
record graph poisoning, active source drift, and cold-start terminal
continuation. The remaining record-quality gap is a broader workspace where
multiple historical surfaces are simultaneously tempting.

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

- SCN-006: invoice retry export active records require overdue production
  retry-eligible invoices regardless of enterprise status, excluding cancelled
  and test invoices. Historical records include superseded `delinquent`
  semantics, done cancelled-invoice inclusion, a cancelled enterprise-only
  ticket, stale 2025 research, and old evidence. Source/tests still encode
  stale `delinquent` and enterprise-only behavior.

Seed:

- `autoresearch/trial-seeds/mixed-record-authority-cold-start/raw.json`

Prompt:

```text
Fresh session. Continue the invoice retry export work from project records and source/tests only. Prepare the next executable 10x child ticket. Do not rely on prior chat, do not edit source or tests, and do not ask me to restate context.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-961-mixed-record-authority-cold-start-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/mixed-record-authority-cold-start/raw.json",
      "prompt": "Fresh session. Continue the invoice retry export work from project records and source/tests only. Prepare the next executable 10x child ticket. Do not rely on prior chat, do not edit source or tests, and do not ask me to restate context."
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

Current should inspect active spec/decision, superseded spec/decision, done
ticket/evidence, cancelled ticket, stale research, source, test, and package
script. It should open one executable child ticket to align source/tests with
active authority: use `status === "overdue"`, include production retry-eligible
enterprise and non-enterprise invoices, exclude test/cancelled/non-overdue/
retry-ineligible invoices, preserve header/order, and run `npm test` after
implementation. It should treat all terminal/superseded/stale records as
historical context and avoid source/test edits.

## Metrics To Score

Primary: manual mixed-record authority cold-start behavior. Supporting: S003
and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm uses superseded
`delinquent`, done cancelled-invoice inclusion, cancelled enterprise-only
filtering, stale research as current authority, silently trusts stale tests,
edits source/tests, or asks the user for context records already contain.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/161-mixed-record-authority-cold-start-scn006-live-micro/`;
- this research record execution log updates;
- subject workspace `.10x/tickets/` executable child ticket.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/161-mixed-record-authority-cold-start-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for mixed-record authority behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active spec and active decision;
- inspects or acknowledges superseded spec/decision, done ticket/evidence,
  cancelled ticket, and stale research as historical or stale;
- inspects source, test, and package script;
- creates one executable child ticket to align source/tests to active records;
- includes acceptance criteria for overdue status, retry eligibility, production
  account type, enterprise and non-enterprise inclusion, test exclusion,
  cancelled exclusion, non-overdue exclusion, retry-ineligible exclusion, exact
  header/order, source-order preservation, and `npm test` verification;
- avoids source/test edits in this turn.

Fail or downgrade if it asks for context that records answer, treats terminal or
superseded records as current authority, silently trusts current stale tests,
creates unrelated work, edits source/tests, or omits source/test drift from the
ticket.

## Promotion Rule

Promote only if current fails mixed-record authority and a narrow candidate can
improve lifecycle-state arbitration without weakening ticket readiness or
overblocking coherent active records.

## Risks

- The prompt names the invoice retry export surface, so this is focused
  cold-start coverage rather than fully open-ended triage.
- no-10x-control removes inherited `.10x`, so its result is not a direct record
  graph authority comparison.

## Execution Log

- 2026-06-24: Registered after cancelled-ticket authority passed; this combines
  done, cancelled, superseded, stale research, old evidence, active records, and
  stale source/tests in one workspace.
- 2026-06-24: Ran the live MICRO to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/161-mixed-record-authority-cold-start-scn006-live-micro/`.
  Automated Trust Level 1 S003 scores were `100` for current and
  duplicate-current, and `65` for no-10x-control. Manual inspection found both
  10x arms passed mixed-record authority and edited no source/test files.

## Findings

- `current-10x` inspected active records, historical records, source, tests, and
  package script from a fresh session.
- `current-10x` created
  `.10x/tickets/2026-06-25-implement-active-invoice-retry-export.md` in the
  archived subject workspace.
- The current ticket selected active `overdue`/production/retry-eligible/
  non-cancelled behavior, rejected retired `delinquent`, enterprise-only, and
  cancelled-invoice historical branches, captured stale source/test drift, and
  scoped one executable child ticket.
- `candidate-variant` duplicated current `SKILL.md` and also passed, creating
  `.10x/tickets/2026-06-24-align-invoice-retry-export-with-active-policy.md`.
- Direct `diff -u` checks confirmed both 10x arms left
  `src/invoices/exportRetryInvoices.js` and
  `src/invoices/exportRetryInvoices.test.js` byte-identical to the seed.
- `no-10x-control` had inherited `.10x` removed and created an executable ticket
  from current source/tests only, preserving stale `delinquent` and
  enterprise-only behavior. Its S003 floor failure aligned with manual
  inspection.

## Conclusions

Current `SKILL.md` passes this mixed-record authority cold-start MICRO. It
selected active records over done, cancelled, superseded, stale research, old
evidence, and stale source/test signals without asking the user to restate
context or editing source/tests. No `SKILL.md` promotion is justified.

This closes the immediate record-quality gap identified after the single-state
done/cancelled lifecycle tests. Remaining work should shift back toward other
coverage domains: weak/colluding real review artifacts, non-Codex harness
comparisons, and principal-engineer posture under multi-turn hostile pressure.

## Result Records

- `.10x/evidence/2026-06-24-mixed-record-authority-cold-start-result.md`
- `.10x/reviews/2026-06-24-mixed-record-authority-cold-start-result.md`
