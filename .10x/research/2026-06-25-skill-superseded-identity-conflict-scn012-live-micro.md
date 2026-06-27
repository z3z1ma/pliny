Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-966-skill-superseded-identity-conflict-scn012-live-micro

## Experiment ID

EXP-20260625-966-skill-superseded-identity-conflict-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: promoted canonical `SKILL.md` preserves the current record-backed
skill identity without reviving a superseded near-synonym skill slug.

## Motivation

`candidate-skill-record-backed-identity-v1` was promoted with wording narrowed
to the current workstream or non-superseded records. Its residual risk is stale
or superseded identity conflict. This MICRO directly probes that risk.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and three
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate current canonical `SKILL.md`, used as a
  repeatability arm after promotion.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

No `writable_add_dirs` are configured. The subject workspace intentionally has
no harness-native skill directory.

## Scenario Set

- SCN-012: active knowledge and parent ticket establish
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`; superseded research
  mentions the stale near-synonym
  `.10x/skills/replay-ledger-import-fixtures/SKILL.md`.

Seed:

- `autoresearch/trial-seeds/skill-authoring-superseded-identity/raw.json`

Prompt:

```text
Wrap up the Ledger import parent now. The child surfaced a reusable fixture replay procedure, and the workspace contains both a superseded old skill-name note and active records naming the replacement identity.

Use the current non-superseded records to choose the skill identity. Preserve the fixture replay procedure as the correct source skill if appropriate. Do not revive superseded skill names. Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-966-skill-superseded-identity-conflict-scn012-live-micro",
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
      "instruction_source": "SKILL.md duplicate-current post-promotion",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-superseded-identity/raw.json",
      "prompt": "Wrap up the Ledger import parent now. The child surfaced a reusable fixture replay procedure, and the workspace contains both a superseded old skill-name note and active records naming the replacement identity.\n\nUse the current non-superseded records to choose the skill identity. Preserve the fixture replay procedure as the correct source skill if appropriate. Do not revive superseded skill names. Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one."
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

Current and duplicate-current should create
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, avoid
`.10x/skills/replay-ledger-import-fixtures/SKILL.md`, create no native mirrors,
and avoid implementation edits.

## Metrics To Score

Primary: manual skill identity conflict inspection. Supporting: S008, S002, and
S006.

## Quality Floors

Manual inspection is authoritative. Pass current only if every current and
duplicate-current repetition uses the current source skill identity, creates no
superseded skill path, creates no native mirror, and avoids implementation
edits.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after three
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/206-skill-superseded-identity-conflict-scn012-live-micro/`

## Promotion Rule

This is a post-promotion conformance gate. It cannot promote a new candidate,
but a failure should open or revive a targeted stale-identity candidate.

## Execution Log

- 2026-06-25: Registered after promoting record-backed skill identity with
  non-superseded-record wording.
- 2026-06-25: Ran nine live Codex subject samples into
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/206-skill-superseded-identity-conflict-scn012-live-micro/`.
- 2026-06-25: Manual inspection passed the post-promotion identity gate. All
  current and duplicate-current repetitions created the current source skill
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`, created no
  `.10x/skills/replay-ledger-import-fixtures*` path, created no native mirror
  directory, avoided implementation edits, and generated no forbidden
  non-knowledge `.10x` record references inside the skill body.

## Result

Current canonical `SKILL.md` passed this conformance gate. The promoted
record-backed identity wording did not revive the superseded near-synonym slug
when active records and superseded research disagreed.

Trust Level 1 telemetry still marked S006 below floor for current and
duplicate-current because the heuristic does not understand this skill-wrap-up
shape. Manual inspection is authoritative for this MICRO.

Residual risk: one current repetition left done-status parent and child tickets
at top-level instead of moving them to `.10x/tickets/done/`. That is a terminal
ticket path-maintenance gap, not a stale identity failure, and should be tested
separately.
