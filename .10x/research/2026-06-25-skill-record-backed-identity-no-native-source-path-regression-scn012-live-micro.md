Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-999-skill-record-backed-identity-no-native-source-path-regression-scn012-live-micro

## Experiment ID

EXP-20260625-999-skill-record-backed-identity-no-native-source-path-regression-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-skill-record-backed-identity-v1` preserves no-native
source skill path shape while stabilizing the record-backed skill identity.

## Motivation

The candidate improved exact source skill identity in EXP-997 and passed the
weak-request identity regression in EXP-998. Before promotion it must also clear
the no-native source-path gate that previously justified the canonical
directory-shaped source skill sentence.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and two
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

- SCN-012: repeated Ledger import fixture replay procedure should become a
  self-contained source skill under `.10x/skills/<skill-slug>/SKILL.md` without
  creating speculative native mirrors.

Seed:

- `autoresearch/trial-seeds/skill-authoring-no-native-dir/raw.json`

Prompt:

```text
Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.

Use the existing records to choose the correct skill identity and record type. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary.

Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one. This is a subject workspace only.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-999-skill-record-backed-identity-no-native-source-path-regression-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 2,
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
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-skill-record-backed-identity.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-no-native-dir/raw.json",
      "prompt": "Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.\n\nUse the existing records to choose the correct skill identity and record type. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary.\n\nDo not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one. This is a subject workspace only."
    }
  ],
  "budget": {
    "max_harness_runs": 6,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should create `.10x/skills/ledger-import-fixture-replay/SKILL.md` in
both repetitions, create no flat source skill, create no alternate skill owner,
avoid prohibited `.10x` record references inside the skill, avoid speculative
native mirrors, and avoid implementation edits.

## Metrics To Score

Primary: manual source-path and identity inspection. Supporting: S008, S002, and
S006.

## Quality Floors

Manual inspection is authoritative. Pass candidate only if every candidate
repetition uses the exact directory-shaped source skill path
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, creates no duplicate skill
owner, creates no native mirror in the no-native workspace, and avoids
implementation edits.

## Budget And Stop Conditions

Maximum 6 live Codex calls. Timeout 7200 seconds per run. Stop after two
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/199-skill-record-backed-identity-no-native-source-path-regression-scn012-live-micro/`

## Promotion Rule

This regression alone cannot promote the candidate. It can only keep the
candidate alive for harness-native mirror identity regressions.

## Execution Log

- 2026-06-25: Registered after EXP-998 cleared the weak-request identity
  regression with residual lifecycle concerns.
- 2026-06-25: Ran six live Codex subject samples under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/199-skill-record-backed-identity-no-native-source-path-regression-scn012-live-micro/`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found candidate and current both created the
  exact directory-shaped `.10x/skills/ledger-import-fixture-replay/SKILL.md`
  source skill in both repetitions. Both no-10x-control repetitions created the
  flat file `.10x/skills/ledger-import-fixture-replay.md`.

## Result

Pass. Candidate cleared the no-native source-path identity regression.

Manual inspection found:

- candidate-variant: 2/2 exact directory-shaped source skill identity,
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- current-10x: 2/2 exact directory-shaped source skill identity;
- no-10x-control: 0/2 directory-shaped source skill identity, with both reps
  creating `.10x/skills/ledger-import-fixture-replay.md`;
- candidate-variant: 0/2 speculative `.agents`, `.claude`, or `.opencode`
  mirror files;
- candidate-variant: 0/2 forbidden non-knowledge `.10x` record references
  inside generated skills;
- candidate-variant: 0/2 implementation file edits.

Automated Trust Level 1 telemetry:

- candidate-variant: `S002=100`, `S006=65` average;
- current-10x: `S002=100`, `S006=55` average;
- no-10x-control: `S002=30`, `S006=20` average.

Supporting records:

- `.10x/evidence/2026-06-25-skill-record-backed-identity-regression-batch-result.md`
- `.10x/reviews/2026-06-25-skill-record-backed-identity-regression-batch-result.md`
- `.10x/reviews/2026-06-25-skill-record-backed-identity-promotion-review.md`
