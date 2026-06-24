Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-925-record-rename-reference-repair-scn004-live-micro

## Experiment ID

EXP-20260624-925-record-rename-reference-repair-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can rename an active record, repair live
references, update the record title, and preserve historical references without
requiring a new instruction overlay.

## Motivation

The conformance map marks record graph lifecycle mechanics as partial. The
invalid-draft deletion MICRO passed, with a minor residual concern around
machine-header hygiene when an obsolete path remains in a descriptive header.
This MICRO probes the adjacent rename path: a valid active specification moves
to a better durable term while historical notes and captured search output must
remain historically honest.

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

- SCN-004: The ACME webhook retry behavior is valid, but the active spec path
  uses a misleading legacy term. The agent must rename the spec, repair live
  `.10x` references, update the title, and preserve historical mentions and
  fenced command-output blocks that mention the old path as history.

Seed:

- `autoresearch/fixtures/live-seeds/record-rename-reference-repair/raw.json`

Prompt:

```text
Rename `.10x/specs/acme-retry-window.md` to `.10x/specs/acme-webhook-retry-policy.md` because "retry window" is misleading and "webhook retry policy" is the ratified durable term. The behavior is unchanged. Move the record, update its title if needed, repair live `.10x` references that should follow the rename, and preserve historical notes and fenced command-output blocks that mention the old path as history. Do not edit source files and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-925-record-rename-reference-repair-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-rename-reference-repair/raw.json",
      "prompt": "Rename `.10x/specs/acme-retry-window.md` to `.10x/specs/acme-webhook-retry-policy.md` because \"retry window\" is misleading and \"webhook retry policy\" is the ratified durable term. The behavior is unchanged. Move the record, update its title if needed, repair live `.10x` references that should follow the rename, and preserve historical notes and fenced command-output blocks that mention the old path as history. Do not edit source files and do not run tests."
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

Current should move the spec to
`.10x/specs/acme-webhook-retry-policy.md`, update the heading/title, repair live
`Depends-On`, `Relates-To`, `Target`, scope, and acceptance references to the
new path, preserve explicitly historical body prose and fenced `rg` output, and
avoid source/test edits or test execution. No-10x may repair the concrete file
paths but is less likely to distinguish live authority from historical notes.

## Metrics To Score

Primary: manual record rename/reference repair inspection. Supporting: S002,
S003, and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm leaves live
headers pointing at the old spec path, leaves two active specs, broad-rewrites
historical notes or fenced output, edits source/tests, runs tests, or changes
the ratified behavior while renaming.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/125-record-rename-reference-repair-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` rename and reference repair edits.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/125-record-rename-reference-repair-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for rename/reference repair behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- moves `.10x/specs/acme-retry-window.md` to
  `.10x/specs/acme-webhook-retry-policy.md`;
- updates the spec heading or title to the ratified durable term;
- repairs live `Depends-On`, `Relates-To`, `Target`, scope, acceptance, and
  live authority body references to the new path;
- preserves historical body text and fenced command-output blocks when they
  mention the old path only as history;
- avoids duplicate active specs;
- avoids source/test edits and test execution;
- keeps the record graph understandable to a cold reader.

Fail or downgrade if it leaves dangling live references, silently keeps the old
path as active authority, broad-rewrites historical notes/code blocks, creates
unnecessary replacement specs or implementation tickets, edits source, or runs
tests.

## Promotion Rule

No behavioral candidate is under test; `candidate-variant` duplicates
`current-10x` only to satisfy the current runner's fixed arm contract. If
current fails, create a narrow candidate targeting the observed rename lifecycle
failure.

## Risks

- The no-10x control loses `.10x` under isolation, limiting control comparison.
- Rename has legitimate variation in body text; manual inspection should
  distinguish live authority references from historically accurate mentions.

## Execution Log

- 2026-06-24: Registered from the record graph lifecycle backlog after the
  invalid-draft deletion MICRO passed with a minor machine-header hygiene risk.
