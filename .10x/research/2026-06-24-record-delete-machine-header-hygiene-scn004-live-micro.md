Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-938-record-delete-machine-header-hygiene-scn004-live-micro

## Experiment ID

EXP-20260624-938-record-delete-machine-header-hygiene-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can delete an invalid draft record and remove
the deleted path from all live machine-readable headers while preserving
historical body prose and fenced output.

## Motivation

`EXP-20260624-921-record-delete-invalid-draft-reference-repair-scn004-live-micro`
passed the core deletion behavior but exposed a residual header-hygiene risk:
the current arm kept the deleted spec path in a review `Target:` header as a
descriptive "formerly at" phrase. This follow-up makes live header hygiene the
primary target.

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
  The agent must delete the draft, repair live references, and keep the deleted
  path out of `Depends-On`, `Relates-To`, `Target`, and `Parent` headers.

Seed:

- `autoresearch/trial-seeds/record-delete-invalid-draft-reference-repair/raw.json`

Prompt:

```text
Security has invalidated `.10x/specs/zeus-webhook-retry.md`. Delete the draft spec and repair the record graph. No live machine-readable header (`Depends-On`, `Relates-To`, `Target`, `Parent`) may keep the deleted path after the repair. Preserve the deleted path only in historical body prose or fenced output where it is clearly historical. Cancel or block dependent active work instead of leaving it executable against deleted behavior. Do not edit source files and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-938-record-delete-machine-header-hygiene-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/record-delete-invalid-draft-reference-repair/raw.json",
      "prompt": "Security has invalidated `.10x/specs/zeus-webhook-retry.md`. Delete the draft spec and repair the record graph. No live machine-readable header (`Depends-On`, `Relates-To`, `Target`, `Parent`) may keep the deleted path after the repair. Preserve the deleted path only in historical body prose or fenced output where it is clearly historical. Cancel or block dependent active work instead of leaving it executable against deleted behavior. Do not edit source files and do not run tests."
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

Current may now pass because the prompt explicitly calls out machine-readable
headers. Failure would mean a narrow instruction candidate is justified near
record reference repair rules.

## Metrics To Score

Primary: manual deleted-path live-header hygiene inspection. Supporting: S002,
S003, and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm leaves the
deleted path in any live `Depends-On`, `Relates-To`, `Target`, or `Parent`
header; treats the deleted spec as authority; broad-rewrites historical prose or
fenced output; edits source/tests; or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/138-record-delete-machine-header-hygiene-scn004-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/138-record-delete-machine-header-hygiene-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for deleted-path live-header hygiene.

## Manual Inspection Requirement

Pass an arm only if it:

- deletes `.10x/specs/zeus-webhook-retry.md`;
- removes `.10x/specs/zeus-webhook-retry.md` from every live `Depends-On`,
  `Relates-To`, `Target`, and `Parent` header;
- preserves deleted-path mentions only in historical body prose or fenced output
  where the path is clearly historical;
- blocks or cancels dependent implementation work rather than leaving it
  executable against deleted behavior;
- avoids source/test edits and test execution;
- leaves the record graph understandable to a cold reader.

Fail or downgrade if any live header still contains the deleted path, even in a
"formerly at" phrase.

## Promotion Rule

No behavioral candidate is under test; `candidate-variant` duplicates
`current-10x` only to satisfy the fixed runner arm contract. If current fails
and duplicate-current also tends to fail, create a narrow live-header hygiene
candidate and rerun with a historical-prose preservation regression.

## Risks

- The prompt is explicit, so a pass proves the behavior under direct pressure
  more than spontaneous header hygiene.
- The no-10x control loses `.10x` under isolation, limiting control comparison.

## Execution Log

- 2026-06-24: Registered from the residual risk in
  `.10x/research/2026-06-24-record-delete-invalid-draft-reference-repair-scn004-live-micro.md`
  and the record-graph scout recommendation.
- 2026-06-24: Ran live under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/138-record-delete-machine-header-hygiene-scn004-live-micro/`.
  Automated Trust Level 1 scores were low for all arms (`S002=30` for
  current and duplicate-current, `S002=15` for no-10x-control), but manual
  inspection found current and duplicate-current passed the stricter
  deleted-path header-hygiene behavior.

## Result

Current `SKILL.md` passes this stricter deleted-path live-header hygiene MICRO.
Current and duplicate-current deleted `.10x/specs/zeus-webhook-retry.md`,
cancelled and moved the dependent ticket, cleared the deleted path from live
`Depends-On`, `Relates-To`, `Target`, and `Parent` headers, preserved historical
body/fenced-output mentions, avoided source/test edits, and did not run tests.

No canonical `SKILL.md` promotion is justified. This run instead strengthens
record graph lifecycle conformance evidence and exposes another case where the
offline scorer underestimates successful record maintenance.

Supporting records:

- `.10x/evidence/2026-06-24-record-delete-machine-header-hygiene-result.md`
- `.10x/reviews/2026-06-24-record-delete-machine-header-hygiene-result.md`
