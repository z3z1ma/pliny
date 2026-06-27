Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-998-skill-record-backed-identity-weak-request-regression-scn012-live-micro

## Experiment ID

EXP-20260625-998-skill-record-backed-identity-weak-request-regression-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-skill-record-backed-identity-v1` preserves the
weak-request slug-stability behavior that canonical `SKILL.md` already passed in
`EXP-20260625-995`, while adding no duplicate or speculative skill owners.

## Motivation

The record-backed identity candidate improved the explicit closure-completeness
scenario in `EXP-20260625-997`. Before promotion, it must prove it does not
regress the weaker retrospective request that current already handled correctly.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and three
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-skill-record-backed-identity-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

No `writable_add_dirs` are configured. The subject workspace intentionally has
no harness-native skill directory.

## Scenario Set

- SCN-012: weakly phrased Ledger import retrospective request. Existing records
  name repeated fixture replay friction, `sourceRef` vocabulary, and an archive
  malformed-currency follow-up. The prompt asks the agent to wrap up the parent
  without spelling the desired skill slug.

Seed:

- `autoresearch/trial-seeds/skill-authoring-no-native-dir/raw.json`

Prompt:

```text
Wrap up the Ledger import parent now. The child surfaced one reusable replay habit, one naming convention, and one archive-import gap. Preserve each in the right durable place, using the existing records to choose names and record types. Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-998-skill-record-backed-identity-weak-request-regression-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 3,
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
      "instruction_source": "SKILL.md plus candidate-skill-record-backed-identity-v1",
      "instruction_path": "autoresearch/candidates/2026-06-25-skill-record-backed-identity.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-no-native-dir/raw.json",
      "prompt": "Wrap up the Ledger import parent now. The child surfaced one reusable replay habit, one naming convention, and one archive-import gap. Preserve each in the right durable place, using the existing records to choose names and record types. Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should create `.10x/skills/ledger-import-fixture-replay/SKILL.md` in
all repetitions, create no alternate skill slug or flat source skill, preserve
`sourceRef` as knowledge, open or update archive malformed-currency follow-up
ownership, avoid speculative mirror directories, and avoid implementation
edits.

## Metrics To Score

Primary: manual skill identity and retrospective routing inspection. Supporting:
S008, S002, S006.

## Quality Floors

Manual inspection is authoritative. Pass candidate only if it preserves every
manual floor from
`.10x/research/2026-06-25-skill-weak-request-slug-stability-scn012-live-micro.md`.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after three
repetitions for each arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/198-skill-record-backed-identity-weak-request-regression-scn012-live-micro/`

## Promotion Rule

This regression alone cannot promote the candidate. It can only keep the
candidate alive for no-native source-path and harness-native mirror regressions.

## Execution Log

- 2026-06-25: Registered after `EXP-20260625-997` made the record-backed skill
  identity candidate promising but not promotable.
- 2026-06-25: Ran nine live Codex subject samples under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/198-skill-record-backed-identity-weak-request-regression-scn012-live-micro/`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found candidate and current both created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md` in all three 10x
  repetitions, while no-10x-control created flat or near-synonym skill files.

## Result

Passed target regression with residual lifecycle risk.

Manual inspection found:

- candidate-variant: 3/3 exact source skill identity,
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- current-10x: 3/3 exact source skill identity,
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- no-10x-control: 0/3 exact directory-shaped source skill identity, with flat
  or near-synonym skill files such as
  `.10x/skills/ledger-import-replay-fixtures.md`,
  `.10x/skills/stable-ledger-import-replay.md`, and
  `.10x/skills/ledger-import-replay-fixtures.md`;
- candidate-variant: 0/3 speculative `.claude`, `.agents`, or `.opencode`
  mirror directories in the no-native workspace;
- candidate-variant: 0/3 forbidden `.10x` record references inside generated
  skill bodies;
- candidate-variant: 0/3 implementation file edits.

Automated Trust Level 1 telemetry tied candidate and current:

- candidate-variant: `S002=85`, `S006=65` average;
- current-10x: `S002=85`, `S006=65` average;
- no-10x-control: `S002=70`, `S006=30` average.

Residual lifecycle risk remains outside the candidate's target behavior. Current
moved both the parent and child tickets into `done/` in all three repetitions.
Candidate did so in one repetition, left the already-`done` child at the
top-level in one repetition, and left both done-status tickets at the top-level
in one repetition. This does not show identity regression, but future closure
experiments should continue testing terminal-status path maintenance.

The candidate remains active for the no-native source-path and harness-native
mirror identity regressions.

Supporting records:

- `.10x/evidence/2026-06-25-skill-record-backed-identity-weak-request-regression-result.md`
- `.10x/reviews/2026-06-25-skill-record-backed-identity-weak-request-regression-result.md`
