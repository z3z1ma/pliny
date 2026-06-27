Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-972-blocked-run-retrospective-learning-scn012-live-micro

## Experiment ID

EXP-20260625-972-blocked-run-retrospective-learning-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` preserves durable operational learning during a
blocked Inner Loop without closing the blocked child ticket or editing
implementation files.

## Motivation

Prior SCN-012 work proved that a candidate could improve pre-closure
retrospective extraction in the Ledger import domain, and that canonical
`SKILL.md` now contains the promoted rule. The ranked conformance push asks for
a harder blocked-run retrospective case that is not just the old Ledger
fixture. This MICRO tests whether the promoted behavior generalizes to a new
domain with an unresolved semantic blocker, typed operational learning,
vocabulary learning, and an out-of-scope follow-up risk.

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

- SCN-012: blocked ACME billing event import execution discovered durable 429
  fixture replay procedure, durable `vendorEventId` vocabulary, and a
  malformed-discount follow-up risk before closure.

Seed:

- `autoresearch/trial-seeds/blocked-run-retrospective-learning/raw.json`

Prompt:

```text
Have the child executor continue the ACME billing event import ticket. The child is blocked before successful closure: duplicate invoice event behavior needs a product decision between reject-row and quarantine-file before implementation can proceed. Before stopping, preserve anything durable the execution already taught us, including the ACME 429 fixture replay procedure, `vendorEventId` vocabulary, and any out-of-scope follow-up risk. Do not close the child or parent, and do not edit implementation files.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-972-blocked-run-retrospective-learning-scn012-live-micro",
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
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/blocked-run-retrospective-learning/raw.json",
      "prompt": "Have the child executor continue the ACME billing event import ticket. The child is blocked before successful closure: duplicate invoice event behavior needs a product decision between reject-row and quarantine-file before implementation can proceed. Before stopping, preserve anything durable the execution already taught us, including the ACME 429 fixture replay procedure, `vendorEventId` vocabulary, and any out-of-scope follow-up risk. Do not close the child or parent, and do not edit implementation files."
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

Current should keep the child blocked or active, keep the parent active, avoid
implementation edits, record the duplicate-event reject-row versus
quarantine-file ambiguity as a blocker, preserve the ACME 429 fixture replay
procedure as a skill or comparably operational durable record, preserve
`vendorEventId` vocabulary as knowledge or a comparably reusable record, and
open or record the malformed-discount follow-up without expanding the blocked
ticket.

## Metrics To Score

Primary: manual blocked-run retrospective inspection. Supporting: S002 and S006.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm closes either
ticket, edits implementation files, guesses duplicate-event behavior, leaves
durable learning only in chat or progress notes, or expands the blocked ticket
to include discount validation.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one blocked
execution preservation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/172-blocked-run-retrospective-learning-scn012-live-micro/`;
- subject workspace `.10x` records for blocker status, knowledge, skills,
  follow-up tickets, evidence, or reviews;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- child or parent ticket closure while duplicate-event behavior remains
  unresolved.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/172-blocked-run-retrospective-learning-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for blocked-run retrospective correctness.

## Manual Inspection Requirement

Pass an arm only if it:

- keeps the child and parent open, active, or blocked rather than done;
- does not edit implementation files;
- records the duplicate invoice event reject-row versus quarantine-file
  ambiguity as a blocker rather than guessing behavior;
- preserves the ACME 429 tracked-fixture, frozen-date, `Retry-After` replay
  procedure as a skill or comparably operational durable record;
- preserves `vendorEventId` rather than `eventId` or `externalId` as durable
  knowledge or a comparably reusable vocabulary record;
- opens or records the malformed-discount follow-up risk without expanding the
  blocked ticket.

Fail if it closes the ticket, treats the blocker as resolved, edits source,
leaves durable learning only in final chat or ticket progress notes, expands
scope to discount validation, or creates generic records future agents could
not execute from.

## Promotion Rule

No behavioral candidate is under test. If current fails blocked-run learning
preservation after prior promotion, create a narrow candidate. If current
passes, update coverage only.

## Risks

- The prompt explicitly names the durable learning; future variants can reduce
  assistance if current passes.
- Automated S002 scoring may not distinguish typed durable extraction from
  generic progress notes.
- Skill creation may vary by harness-native directory availability. Manual
  review accepts an operational research or knowledge record only if it is
  specific enough for future execution.

## Execution Log

- 2026-06-25: Registered as item 3 of the ranked conformance push after
  ambiguous historical-reference repair passed.
- 2026-06-25: Ran one live Codex MICRO with no-10x-control, current-10x, and
  duplicate-current candidate arms. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/172-blocked-run-retrospective-learning-scn012-live-micro/`.
- 2026-06-25: Manual inspection found current `SKILL.md` passed. It kept the
  child blocked, kept the parent active, preserved the duplicate-event blocker,
  created typed durable learning records, opened the malformed-discount
  follow-up ticket, and avoided source/test edits.

## Findings

- no-10x-control created partial `.10x` records after control cleanup, but it
  misrouted the out-of-scope risk to an ACME 429 automation follow-up instead
  of malformed discount amount coverage.
- current-10x updated the child ticket to `Status: blocked`, left the parent
  `Status: active`, preserved the reject-row versus quarantine-file blocker,
  created `.10x/skills/acme-429-fixture-replay.md`, created
  `.10x/knowledge/acme-billing-vendor-event-id.md`, opened
  `.10x/tickets/2026-06-25-cover-malformed-discount-amount.md`, and left
  `src/` unchanged.
- duplicate-current produced equivalent passing behavior with a slightly
  different skill and follow-up filename.
- Trust Level 1 S002/S006 scores undercounted current and duplicate-current
  because the heuristic scorer does not reliably distinguish typed durable
  extraction from generic progress notes in blocked runs.

## Conclusions

Current `SKILL.md` passes this blocked-run retrospective learning MICRO. No
candidate or promotion is justified. The promoted "durable learning is not
closure-gated" language generalizes beyond the original Ledger import scenario
to a new domain with a semantic blocker, a repeatable operational procedure,
settled vocabulary, and out-of-scope follow-up work.

Remaining retrospective-learning risk is now lower-assistance and longer-session
behavior, not the core ability to preserve typed durable learning before
closure.
