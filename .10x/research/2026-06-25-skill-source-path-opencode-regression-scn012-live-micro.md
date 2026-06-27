Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-992-skill-source-path-opencode-regression-scn012-live-micro

## Experiment ID

EXP-20260625-992-skill-source-path-opencode-regression-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-skill-source-path-shape-v1` preserves governed
`.opencode/skills` mirroring while making the `.10x` source skill path
directory-shaped.

## Motivation

The source-path candidate improved no-native-dir source path shape, but
promotion requires regression controls for harness-native mirroring. OpenCode is
one of the target harnesses for 10x skill exposure and previously passed under
current canonical instructions.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-skill-source-path-shape-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-012: repeated Ledger import fixture replay procedure should become a
  governed, self-contained skill and `.opencode` mirror.

Seed:

- `autoresearch/trial-seeds/skill-authoring-opencode-mirror/raw.json`

Prompt:

```text
Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.

Before authoring any skill, inspect the subject workspace for existing skill-writing governance and follow it. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary. Expose any active skill to the harness-native skills directory if one exists.

Do not edit implementation files. This is a subject workspace only.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-992-skill-source-path-opencode-regression-scn012-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-skill-source-path-shape-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-skill-source-path-shape.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-opencode-mirror/raw.json",
      "prompt": "Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.\n\nBefore authoring any skill, inspect the subject workspace for existing skill-writing governance and follow it. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary. Expose any active skill to the harness-native skills directory if one exists.\n\nDo not edit implementation files. This is a subject workspace only."
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

Candidate should create
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, mirror equivalent content
to `.opencode/skills/ledger-import-fixture-replay/SKILL.md`, read the seeded
OpenCode governor, avoid prohibited `.10x` record references, and avoid
speculative `.claude` or `.agents` mirrors.

## Metrics To Score

Primary: manual source-path and `.opencode` mirror inspection. Supporting:
S008, S002, and S006.

## Quality Floors

Manual inspection is authoritative. Pass candidate only if it preserves every
manual floor from
`.10x/research/2026-06-24-skill-authoring-opencode-mirror-scn012-live-micro.md`
and uses the directory-shaped `.10x/skills/<slug>/SKILL.md` source path.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one skill
authoring turn.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/192-skill-source-path-opencode-regression-scn012-live-micro/`

## Promotion Rule

This regression alone cannot promote the candidate. It can only keep the
candidate alive for the remaining mirror regression and final promotion review.

## Execution Log

- 2026-06-25: Registered while EXP-991 was running, so the next mirror
  regression can begin immediately if the `.agents` gate passes.
- 2026-06-25: Ran live under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/192-skill-source-path-opencode-regression-scn012-live-micro/`.
  Automated first-pass scores tied candidate and current at `S002=85` and
  `S006=85`; no-10x-control scored `S002=80` and `S006=20`.
- 2026-06-25: Manual inspection found candidate preserved the `.opencode`
  mirror behavior: it read the seeded governor, created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`, mirrored byte-equivalent
  content to `.opencode/skills/ledger-import-fixture-replay/SKILL.md`, avoided
  prohibited `.10x` record references inside the skill, created no speculative
  `.agents` or `.claude` mirrors, and made no implementation edits.

## Result

Pass this regression, but do not promote yet. Candidate preserved the governed
`.opencode` mirror behavior while using the directory-shaped source skill path.
Current also passed the same mirror and source-path floor in this run, so this
experiment clears a regression gate rather than independently proving
promotion.

Supporting records:

- `.10x/evidence/2026-06-25-skill-source-path-opencode-regression-result.md`
- `.10x/reviews/2026-06-25-skill-source-path-opencode-regression-result.md`
