Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-702-control-fixture-record-graph-preservation-scn004-live-micro

## Experiment ID

EXP-20260625-702-control-fixture-record-graph-preservation-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after `fix(autoresearch): preserve fixture record graphs for
controls`, no-10x-control live workspaces preserve fixture `.10x` records when
those records are the task surface, while still suppressing project-level 10x
instruction loading.

## Motivation

EXP-701 exposed a harness flaw: no-10x-control removed `.10x` from seed
workspaces, making record-maintenance controls unable to attempt the task.

The control arm should remove inherited 10x memory from continuation workspaces
when needed, but it must not delete the mock repository records that define a
scenario. Otherwise record-graph tests compare current/candidate behavior
against a control that has no subject matter.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspaces.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay. This arm
  exists only to satisfy the comparative live runner shape.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, fixture `seed-workspace` `.10x` records preserved for all
arms, inherited continuation `.10x` cleanup still enabled for no-10x-control,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-004: ambiguous historical reference repair. Rename the active payments
  retry spec to the ratified durable term, repair live headers/body references
  and supersession pointers, and preserve historical prose plus fenced command
  output.

Seed:

- `autoresearch/trial-seeds/ambiguous-historical-reference-repair/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-702-control-fixture-record-graph-preservation-scn004-live-micro",
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
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for harness sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/trial-seeds/ambiguous-historical-reference-repair/raw.json",
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

No-10x-control should now see the fixture `.10x` record graph. It may still
perform worse than current/candidate, but it should not report the task surface
as missing.

Current and no-op candidate should remain safe. This experiment is not a
promotion candidate and should not change `SKILL.md`.

## Metrics To Score

Primary: manual harness sanity inspection. Supporting: S002.

## Quality Floors

Manual inspection is authoritative.

Pass if:

- no-10x-control manifest has no `.10x` removal for the seed workspace;
- no-10x-control archived workspace contains fixture `.10x` records;
- no-10x-control attempts the requested rename/reference task instead of
  reporting `.10x` missing;
- current and no-op candidate retain normal behavior;
- canonical `SKILL.md` and `autoresearch/program.md` remain unchanged during
  the run.

Fail if:

- no-10x-control deletes fixture `.10x`;
- no-10x-control cannot see the requested record graph;
- current/candidate behavior is confounded by the no-op overlay;
- canonical files mutate during the run.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/179-control-fixture-record-graph-preservation-scn004-live-micro/`;
- subject workspace `.10x` reference repair for each scenario arm;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- subject workspace implementation tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/179-control-fixture-record-graph-preservation-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for harness validity.

## Promotion Rule

No `SKILL.md` promotion. If the harness sanity check fails, fix
`autoresearch/run_codex_subject.py` before running more record-graph controls.

## Risks

- No-10x-control may do the task poorly. That is acceptable for this run if it
  can see and attempt the fixture record graph.
- The no-op candidate is not a real candidate arm and must not be interpreted
  as instruction evidence.

## Execution Log

- 2026-06-25: Registered after EXP-701 found no-10x-control could not access
  fixture `.10x` records and the runner was patched to preserve
  `seed-workspace` record graphs.
- 2026-06-25: Ran all three live Codex samples. Raw artifacts are stored under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/179-control-fixture-record-graph-preservation-scn004-live-micro/`.
- 2026-06-25: Manual inspection recorded in
  `.10x/evidence/2026-06-25-control-fixture-record-graph-preservation-result.md`
  and
  `.10x/reviews/2026-06-25-control-fixture-record-graph-preservation-result.md`.

## Findings

- no-10x-control preserved the fixture `.10x` task surface:
  `pre_run_removed_control_record_dirs` was `[]`.
- no-10x-control saw the active spec, renamed it to
  `.10x/specs/payments-webhook-retry-policy.md`, repaired live references, and
  preserved historical old-path mentions.
- current-10x and the no-op candidate arm produced the expected equivalent
  changed-file set.
- canonical `SKILL.md` and `autoresearch/program.md` stayed unchanged.
- Trust Level 1 S002 remained low for all arms because the scorer cannot
  distinguish historical old-path preservation from stale live references.

## Conclusions

The harness fix is valid for seed workspaces: no-10x-control can now participate
in `.10x` record-graph scenarios without deleting the fixture records that
define the task. Future record-maintenance experiments can use no-10x controls
again, provided the seed raw artifact marks the fixture as `seed-workspace`.
