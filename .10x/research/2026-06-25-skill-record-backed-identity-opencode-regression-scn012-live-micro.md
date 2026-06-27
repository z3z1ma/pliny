Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-968-skill-record-backed-identity-opencode-regression-scn012-live-micro

## Experiment ID

EXP-20260625-968-skill-record-backed-identity-opencode-regression-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-skill-record-backed-identity-v1` preserves the exact
record-backed source skill identity when mirroring to `.opencode/skills`.

## Motivation

OpenCode is a target harness for 10x skill exposure. The identity candidate must
show that source and mirror names remain synchronized under OpenCode-style
native skill exposure.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

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

## Scenario Set

- SCN-012: repeated Ledger import fixture replay procedure should become a
  governed, self-contained skill and `.opencode` mirror under the same
  `ledger-import-fixture-replay` identity.

Seed:

- `autoresearch/trial-seeds/skill-authoring-opencode-mirror/raw.json`

Prompt:

```text
Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.

Before authoring any skill, inspect the subject workspace for existing skill-writing governance and follow it. Use the existing records to choose the correct skill identity. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary. Expose any active skill to the harness-native skills directory if one exists.

Do not edit implementation files. This is a subject workspace only.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-968-skill-record-backed-identity-opencode-regression-scn012-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-skill-record-backed-identity-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-skill-record-backed-identity.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-opencode-mirror/raw.json",
      "prompt": "Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.\n\nBefore authoring any skill, inspect the subject workspace for existing skill-writing governance and follow it. Use the existing records to choose the correct skill identity. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary. Expose any active skill to the harness-native skills directory if one exists.\n\nDo not edit implementation files. This is a subject workspace only."
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

Candidate should create `.10x/skills/ledger-import-fixture-replay/SKILL.md`,
mirror equivalent content to
`.opencode/skills/ledger-import-fixture-replay/SKILL.md`, read the seeded
OpenCode governor, avoid prohibited `.10x` record references, avoid speculative
`.claude` or `.agents` mirrors, and avoid implementation edits.

## Metrics To Score

Primary: manual source/mirror identity inspection. Supporting: S008, S002, and
S006.

## Quality Floors

Manual inspection is authoritative. Pass candidate only if the source and
`.opencode` mirror both use `ledger-import-fixture-replay`, the mirror is
equivalent to the source skill, no duplicate skill owner appears, and no
implementation files are edited.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one skill
authoring turn.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/204-skill-record-backed-identity-opencode-regression-scn012-live-micro/`

## Promotion Rule

This regression alone cannot promote the candidate. It can only keep the
candidate alive for the remaining mirror regressions.

## Execution Log

- 2026-06-25: Registered after EXP-998 cleared the weak-request identity
  regression with residual lifecycle concerns.
- 2026-06-25: Reassigned from invalid four-digit sequence
  `EXP-20260625-1001-...` to legal three-digit sequence
  `EXP-20260625-968-...` before rerun.
- 2026-06-25: Ran three live Codex subject samples under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/204-skill-record-backed-identity-opencode-regression-scn012-live-micro/`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found candidate created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md` and a byte-equivalent
  `.opencode/skills/ledger-import-fixture-replay/SKILL.md` mirror.

## Result

Pass. Candidate cleared the `.opencode` mirror identity regression.

Manual inspection found:

- candidate-variant: exact source skill identity,
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- candidate-variant: exact `.opencode` mirror identity,
  `.opencode/skills/ledger-import-fixture-replay/SKILL.md`;
- candidate-variant: source and mirror files were byte-equivalent;
- candidate-variant: no speculative `.agents` or `.claude` mirrors;
- candidate-variant: no forbidden non-knowledge `.10x` record references inside
  generated skills;
- candidate-variant: no implementation file edits.

Automated Trust Level 1 telemetry:

- candidate-variant: `S002=85`, `S006=85`;
- current-10x: `S002=100`, `S006=85`;
- no-10x-control: `S002=80`, `S006=20`.

Supporting records:

- `.10x/evidence/2026-06-25-skill-record-backed-identity-regression-batch-result.md`
- `.10x/reviews/2026-06-25-skill-record-backed-identity-regression-batch-result.md`
- `.10x/reviews/2026-06-25-skill-record-backed-identity-promotion-review.md`
