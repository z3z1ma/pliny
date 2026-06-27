Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-957-stale-terminal-record-unprompted-scn006-live-micro

## Experiment ID

EXP-20260624-957-stale-terminal-record-unprompted-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can classify stale terminal records as historical
context by reading active records, even when the prompt does not explicitly tell
the subject that terminal tickets/evidence are historical.

## Motivation

`EXP-20260624-956` showed current handles terminal tickets and old evidence
correctly when the prompt names that terminal records are historical. This
follow-up removes that leading instruction while keeping the same subject
workspace, making the active decision/spec carry the authority rule.

## Method Tier

MICRO using a live Codex subject harness and tracked seed transcript.

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

- SCN-006: a prior completed refund CSV ticket and old evidence are present,
  but active records supersede their behavior.

Seed:

- `autoresearch/trial-seeds/stale-terminal-record-unprompted/raw.json`

Prompt:

```text
Pick up the refund negative adjustment CSV work from the previous pass and prepare the next executable child ticket. Inspect the record graph and source/tests first. Do not edit source or tests in this turn.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-957-stale-terminal-record-unprompted-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/stale-terminal-record-unprompted/raw.json",
      "prompt": "Pick up the refund negative adjustment CSV work from the previous pass and prepare the next executable child ticket. Inspect the record graph and source/tests first. Do not edit source or tests in this turn."
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

Current should inspect active and terminal records, not only source/tests. It
should discover from
`.10x/decisions/refund-negative-adjustment-policy-supersession.md` that the
completed 2026-06-20 ticket and evidence are historical context only, then open
one executable child ticket to align source/tests with the active spec. It
should not ask the user whether the old completed-ticket behavior still applies.

## Metrics To Score

Primary: manual unprompted terminal-record authority classification. Supporting:
S003 and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm treats the done
ticket/evidence as active authority, ignores terminal records entirely, trusts
the current stale test, asks the user to arbitrate despite the active decision,
edits source/tests, or omits the stale terminal-record/source/test relationship
from the ticket.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/157-stale-terminal-record-unprompted-scn006-live-micro/`;
- this research record execution log updates;
- subject workspace `.10x/tickets/` executable child ticket.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/157-stale-terminal-record-unprompted-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for unprompted terminal-record authority handling.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active decision/spec, done ticket, old evidence, and source/test
  files;
- identifies the active decision/spec as current authority;
- classifies the done ticket/evidence as historical context, not current
  acceptance criteria;
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

Promote only if current fails the unprompted terminal-record authority
classification and a narrow candidate can improve it without adding broad new
process or weakening ticket readiness.

## Risks

- The active decision is explicit, so a pass proves record use more than
  implicit lifecycle inference.
- no-10x-control removes inherited `.10x`, so its result is not a direct
  authority comparison.

## Execution Log

- 2026-06-24: Registered as the less-leading follow-up to
  `EXP-20260624-956-done-ticket-history-not-active-authority-scn006-live-micro`.
- 2026-06-24: Ran the live MICRO to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/157-stale-terminal-record-unprompted-scn006-live-micro/`.
  Automated Trust Level 1 S003 scores were `no-10x-control=80`,
  `current-10x=100`, and `candidate-variant=100`. Manual inspection found both
  10x arms passed the unprompted terminal-record authority target and edited no
  source/test files.

## Findings

- `current-10x` inspected the active spec, active supersession decision,
  historical done ticket, historical evidence, current implementation, current
  test, and package test command.
- `current-10x` created
  `.10x/tickets/2026-06-25-align-refund-negative-adjustment-csv-with-active-policy.md`
  in the archived subject workspace.
- The current ticket named the active spec/decision as authority, named the
  completed 2026-06-20 ticket/evidence as legacy behavior, and explicitly
  excluded re-authorizing the old all-account export behavior.
- `candidate-variant` duplicated current `SKILL.md` and also passed, creating
  `.10x/tickets/2026-06-25-exclude-test-refund-adjustments.md`.
- Both 10x arms left `src/refunds/exportNegativeAdjustments.js` and
  `src/refunds/exportNegativeAdjustments.test.js` byte-identical to the seed.
- `no-10x-control` failed the manual target despite S003 `80`: with `.10x`
  stripped, it invented a CSV escaping ticket from source/tests and ran
  `npm test`.

## Conclusions

Current `SKILL.md` passes this less-leading terminal-record authority MICRO. It
inferred from the active record graph that terminal ticket/evidence behavior was
historical and prepared the next executable ticket against the active spec. No
`SKILL.md` promotion is justified.

This is stronger than the direct `EXP-20260624-956` result because the prompt
did not tell the subject how to classify terminal records. Remaining risk is
multi-session cold-start behavior where the next agent must reconstruct the
same context from records without the current chat transcript.

## Result Records

- `.10x/evidence/2026-06-24-stale-terminal-record-unprompted-result.md`
- `.10x/reviews/2026-06-24-stale-terminal-record-unprompted-result.md`
