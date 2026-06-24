Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-921-record-delete-invalid-draft-reference-repair-scn004-live-micro

## Experiment ID

EXP-20260624-921-record-delete-invalid-draft-reference-repair-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can delete an invalid draft record, repair live
references, and preserve historical notes without needing a new instruction
overlay.

## Motivation

The conformance map marks record lifecycle mechanics as partial. Prior runs
covered terminal ticket moves and decision supersession. This MICRO covers the
remaining deletion path: an invalid draft spec must be removed while dependent
records stop treating its path as live authority.

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

- SCN-004: Security has explicitly invalidated a draft Zeus webhook retry spec.
  The agent must delete the draft, repair live references, and avoid broad
  rewriting historical notes or command-output blocks.

Seed:

- `autoresearch/fixtures/live-seeds/record-delete-invalid-draft-reference-repair/raw.json`

Prompt:

```text
Security has explicitly invalidated `.10x/specs/zeus-webhook-retry.md`: the draft retry semantics are wrong and must not remain in the record graph as a live specification. Delete that draft spec, repair live `.10x` references so no active dependency/header treats the deleted spec as authority, and update or move the dependent implementation ticket only as needed for coherent blocker/cancellation state. Preserve historical notes and fenced command-output blocks that mention the deleted path as history. Do not edit source files and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-921-record-delete-invalid-draft-reference-repair-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-delete-invalid-draft-reference-repair/raw.json",
      "prompt": "Security has explicitly invalidated `.10x/specs/zeus-webhook-retry.md`: the draft retry semantics are wrong and must not remain in the record graph as a live specification. Delete that draft spec, repair live `.10x` references so no active dependency/header treats the deleted spec as authority, and update or move the dependent implementation ticket only as needed for coherent blocker/cancellation state. Preserve historical notes and fenced command-output blocks that mention the deleted path as history. Do not edit source files and do not run tests."
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

Current should delete the draft spec, remove or rewrite live header references,
mark the dependent implementation ticket as blocked or cancelled, preserve
historical path mentions in body text or fenced output, and avoid source/test
edits. No-10x may be unable to act because control isolation removes `.10x`.

## Metrics To Score

Primary: manual record deletion/reference repair inspection. Supporting: S002,
S003, and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm leaves live
headers pointing at the deleted spec, treats the deleted spec as implementation
authority, broad-rewrites historical notes or fenced output, edits source/tests,
or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/121-record-delete-invalid-draft-reference-repair-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` deletion, reference repair, blocker, or cancellation
  records.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/121-record-delete-invalid-draft-reference-repair-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for deletion/reference repair behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- deletes `.10x/specs/zeus-webhook-retry.md`;
- ensures live `Depends-On`, `Relates-To`, `Target`, and acceptance authority do
  not keep pointing at the deleted spec path;
- blocks or cancels the dependent implementation ticket rather than leaving it
  executable against deleted behavior;
- preserves historical body text and fenced command-output blocks when they
  mention the deleted path only as history;
- avoids source/test edits and test execution;
- keeps the record graph understandable to a cold reader.

Fail or downgrade if it leaves dangling live references, silently keeps the
deleted spec as authority, broad-rewrites historical notes/code blocks, creates
unnecessary replacement specs or implementation tickets, edits source, or runs
tests.

## Promotion Rule

No behavioral candidate is under test; `candidate-variant` duplicates
`current-10x` only to satisfy the current runner's fixed arm contract. If
current fails, create a narrow candidate targeting the observed deletion
lifecycle failure.

## Risks

- The no-10x control loses `.10x` under isolation, limiting control comparison.
- Deletion has legitimate variation: a blocked ticket, cancelled ticket, or
  minimal invalidation note may all be acceptable if live authority is removed
  and the cold-reader graph stays coherent.

## Execution Log

- 2026-06-24: Registered from the researcher backlog and conformance coverage
  map deletion gap.
