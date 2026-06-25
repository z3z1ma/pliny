Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-958-cold-start-terminal-record-continuation-scn006-live-micro

## Experiment ID

EXP-20260624-958-cold-start-terminal-record-continuation-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` lets a cold-start agent reconstruct the next
refund CSV action from records and source/tests without relying on prior chat,
without re-interviewing the user, and without letting terminal records override
active records.

## Motivation

The prior terminal-record runs passed when a transcript mentioned previous work.
The stronger long-horizon test is a cold-start continuation: the subject gets a
workspace with active and terminal records plus source/tests, but no useful chat
history explaining the policy change.

## Method Tier

MICRO using a live Codex subject harness and tracked cold-start seed transcript.

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

- SCN-006: cold-start continuation in the refund CSV workspace used by the
  terminal-record authority experiments.

Seed:

- `autoresearch/fixtures/live-seeds/cold-start-terminal-record-continuation/raw.json`

Prompt:

```text
Cold-start this repository and prepare the next executable 10x child ticket for refund negative adjustment CSV work. Use only the record graph and source/tests; do not rely on prior chat. Do not edit source or tests in this turn.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-958-cold-start-terminal-record-continuation-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/cold-start-terminal-record-continuation/raw.json",
      "prompt": "Cold-start this repository and prepare the next executable 10x child ticket for refund negative adjustment CSV work. Use only the record graph and source/tests; do not rely on prior chat. Do not edit source or tests in this turn."
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

Current should inspect the active decision/spec, the terminal ticket/evidence,
the current source/test, and package script. It should reconstruct that the next
work is to align source/tests to the active spec by excluding test accounts,
while treating the completed 2026-06-20 ticket/evidence as historical context.
It should create one executable child ticket and avoid source/test edits.

## Metrics To Score

Primary: manual cold-start record graph continuation behavior. Supporting: S003
and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm asks the user to
re-explain context already in records, treats terminal records as active
authority, ignores terminal records, trusts the stale current test, creates
unrelated work, edits source/tests, or omits the source/test drift from the
ticket.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/158-cold-start-terminal-record-continuation-scn006-live-micro/`;
- this research record execution log updates;
- subject workspace `.10x/tickets/` executable child ticket.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/158-cold-start-terminal-record-continuation-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for cold-start continuation behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active decision/spec, done ticket, old evidence, and source/test
  files;
- reconstructs from records that the active spec/decision are current authority;
- treats the done ticket/evidence as historical context, not current acceptance
  criteria;
- creates one executable child ticket to align source/tests to active records;
- includes acceptance criteria for excluding test accounts, preserving positive
  adjustment exclusion, exact header/order, source-order preservation after
  filtering, and verification;
- avoids source/test edits in this turn.

Fail or downgrade if it asks for context that records answer, treats done
acceptance criteria as current authority, silently trusts the current test,
creates unrelated work, ignores terminal records, edits source/tests, or omits
the source/test drift from the ticket.

## Promotion Rule

Promote only if current fails cold-start reconstruction and a narrow candidate
can improve record graph continuation without broadening process or weakening
ticket readiness.

## Risks

- The prompt still names the refund CSV work surface, so this is not a fully
  open-ended cold start.
- no-10x-control removes inherited `.10x`, so its result is not a direct
  authority comparison.

## Execution Log

- 2026-06-24: Registered as the cold-start follow-up to
  `EXP-20260624-957-stale-terminal-record-unprompted-scn006-live-micro`.
- 2026-06-24: Ran the live MICRO to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/158-cold-start-terminal-record-continuation-scn006-live-micro/`.
  Automated Trust Level 1 S003 scores were `100` for all arms. Manual
  inspection found both 10x arms passed cold-start record reconstruction and
  edited no source/test files.

## Findings

- `current-10x` had an empty prior transcript and still inspected active spec,
  active supersession decision, historical done ticket, historical evidence,
  implementation, test, and package script.
- `current-10x` created
  `.10x/tickets/2026-06-24-align-refund-negative-adjustment-csv.md` in the
  archived subject workspace.
- The current ticket found no active refund CSV tickets, identified the done
  ticket/evidence as historical, identified source/test drift, included
  references, and included assumption provenance.
- `candidate-variant` duplicated current `SKILL.md` and also passed, creating
  `.10x/tickets/2026-06-24-exclude-test-refund-negative-adjustments.md`.
- Both 10x arms left `src/refunds/exportNegativeAdjustments.js` and
  `src/refunds/exportNegativeAdjustments.test.js` byte-identical to the seed.
- `no-10x-control` had inherited `.10x` removed, created new parent/child/evidence
  records, and ran `npm test`; it is not evidence of durable record graph
  reconstruction despite S003 `100`.

## Conclusions

Current `SKILL.md` passes this cold-start continuation MICRO. With no useful
prior transcript, it reconstructed active authority, terminal history, source
drift, and next executable ticket from records and source/tests. No `SKILL.md`
promotion is justified.

This substantially strengthens the record-quality-over-time lane. Remaining
long-horizon work should use broader workspaces, multiple independent record
surfaces, and follow-up sessions where prior tickets have moved or superseded
across several turns.

## Result Records

- `.10x/evidence/2026-06-24-cold-start-terminal-record-continuation-result.md`
- `.10x/reviews/2026-06-24-cold-start-terminal-record-continuation-result.md`
