Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-971-ambiguous-historical-reference-repair-scn004-live-micro

## Experiment ID

EXP-20260625-971-ambiguous-historical-reference-repair-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can repair an ambiguous record path rename where
the old path appears in live headers, live body references, superseded-record
authority pointers, historical prose, and fenced command output.

## Motivation

The ranked conformance push calls for a harder historical-reference maintenance
case. Prior rename/delete/move tests covered pieces of this behavior. This MICRO
combines the contexts so global search-and-replace is wrong, but leaving live
headers or supersession pointers stale is also wrong.

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

- SCN-004: rename `.10x/specs/payments-retry-window.md` to
  `.10x/specs/payments-webhook-retry-policy.md` without changing behavior.
  The old path appears in:
  - active live headers;
  - active live body references;
  - a superseded record's live `Superseded by` pointer;
  - historical body prose;
  - fenced command output.

Seed:

- `autoresearch/fixtures/live-seeds/ambiguous-historical-reference-repair/raw.json`

Prompt:

```text
Rename `.10x/specs/payments-retry-window.md` to `.10x/specs/payments-webhook-retry-policy.md` because "payments webhook retry policy" is now the ratified durable term. Behavior is unchanged. Move the active spec, update its title, repair live `.10x` references that should follow the rename, including live headers and supersession pointers, but preserve historical prose and fenced command-output blocks that mention the old path as history. Do not create implementation tickets, do not edit source files, and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-971-ambiguous-historical-reference-repair-scn004-live-micro",
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
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/ambiguous-historical-reference-repair/raw.json",
      "prompt": "Rename `.10x/specs/payments-retry-window.md` to `.10x/specs/payments-webhook-retry-policy.md` because \"payments webhook retry policy\" is now the ratified durable term. Behavior is unchanged. Move the active spec, update its title, repair live `.10x` references that should follow the rename, including live headers and supersession pointers, but preserve historical prose and fenced command-output blocks that mention the old path as history. Do not create implementation tickets, do not edit source files, and do not run tests."
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

Current should move the active spec, update the heading, repair live headers and
body references in tickets/evidence/reviews, update the superseded record's
live `Superseded by` pointer, preserve historical prose and fenced output, avoid
creating implementation tickets, and avoid source/test edits or test execution.

## Metrics To Score

Primary: manual ambiguous historical-reference repair inspection. Supporting:
S002 and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm broad-rewrites
historical mentions/fenced output, leaves live headers or live supersession
pointers stale, creates duplicate active specs, creates implementation work,
edits source/tests, or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/171-ambiguous-historical-reference-repair-scn004-live-micro/`;
- subject workspace `.10x` rename and reference repair edits;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets or behavior changes.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/171-ambiguous-historical-reference-repair-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for ambiguous historical-reference repair.

## Manual Inspection Requirement

Pass an arm only if it:

- moves `.10x/specs/payments-retry-window.md` to
  `.10x/specs/payments-webhook-retry-policy.md`;
- updates the spec heading to the durable term;
- repairs live `Depends-On`, `Relates-To`, `Target`, scope, acceptance, and
  live support references to the new path;
- updates the superseded record's live `Superseded by` pointer to the new path;
- preserves historical prose that describes the old path as past state;
- preserves fenced command-output blocks that captured the old path;
- avoids duplicate active specs, implementation tickets, source/test edits, and
  test execution.

Fail if it blindly replaces all old paths, leaves stale live authority pointers,
creates implementation work, changes behavior, edits source/tests, or runs
tests.

## Promotion Rule

No behavioral candidate is under test. If current fails selective reference
repair, create a narrow candidate. If current passes, update coverage only.

## Risks

- The prompt is explicit about preserving history. Future variants can reduce
  assistance if current passes.
- no-10x-control is likely weak because `.10x` is stripped from inherited
  control workspaces.

## Execution Log

- 2026-06-25: Registered as item 2 of the ranked conformance push after EXP-970
  completed multi-surface source/record drift.
- 2026-06-25: Ran live Codex subject harness. Saved artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/171-ambiguous-historical-reference-repair-scn004-live-micro/`.
- 2026-06-25: Manual inspection found current `SKILL.md` passed. It moved the
  active spec, updated the title, repaired live headers/body references and the
  superseded record's live pointer, preserved historical prose and fenced
  output, and avoided implementation tickets, source edits, and test execution.
- 2026-06-25: Duplicate-current also passed. no-10x-control could not complete
  because `.10x` isolation left no writable record graph.

## Findings

- Current distinguished live authority references from historically accurate old
  path mentions, including within the same superseded record.
- Current did not use broad blind replacement; fenced output and historical
  prose remained intact.
- Current did not create implementation work for a terminology-only record
  maintenance request.
- Trust Level 1 S002 produced another false-negative low score for a valid
  record maintenance repair; manual inspection is authoritative.

## Conclusions

Current `SKILL.md` passes this ambiguous historical-reference repair MICRO. No
`SKILL.md` promotion is justified. This completes the ranked conformance push
item for record graph maintenance with ambiguous historical references.
