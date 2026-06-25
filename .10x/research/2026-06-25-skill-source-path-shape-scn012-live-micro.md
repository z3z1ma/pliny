Status: active
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-990-skill-source-path-shape-scn012-live-micro

## Experiment ID

EXP-20260625-990-skill-source-path-shape-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-skill-source-path-shape-v1` improves skill source path
reliability by making `.10x/skills/<skill-slug>/SKILL.md` explicit, without
creating speculative harness mirror directories when no native directory exists.

## Motivation

`EXP-20260625-989-skill-authoring-no-native-dir-scn012-live-micro` produced a
mixed result: current passed the primary current arm, but the duplicate-current
arm wrote `.10x/skills/ledger-import-fixture-replay.md`. The proposed candidate
is intentionally narrow and targets only that source-path shape.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and two
repetitions per arm to reduce stochastic overinterpretation.

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

No `writable_add_dirs` are configured. The subject workspace intentionally has
no harness-native skill directory.

## Scenario Set

- SCN-012: repeated Ledger import fixture replay procedure should become a
  source skill, but no harness mirror should be invented.

Seed:

- `autoresearch/fixtures/live-seeds/skill-authoring-no-native-dir/raw.json`

Prompt:

```text
Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.

Before authoring any skill, inspect the subject workspace for existing skill-writing governance and follow it if present. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary. Expose any active skill to a harness-native skills directory only if one exists in this workspace. If no harness-native skill directory exists, record that no exposure target is present and do not invent .claude, .agents, .opencode, or other mirror directories.

Do not edit implementation files. This is a subject workspace only.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-990-skill-source-path-shape-scn012-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-skill-source-path-shape-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-skill-source-path-shape.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/skill-authoring-no-native-dir/raw.json",
      "prompt": "Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.\n\nBefore authoring any skill, inspect the subject workspace for existing skill-writing governance and follow it if present. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary. Expose any active skill to a harness-native skills directory only if one exists in this workspace. If no harness-native skill directory exists, record that no exposure target is present and do not invent .claude, .agents, .opencode, or other mirror directories.\n\nDo not edit implementation files. This is a subject workspace only."
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
both repetitions and create no harness mirror directories. Current may pass or
may repeat the flat-file source-path failure. Candidate is promotable only if
it shows a reliable path-shape improvement and later mirror regressions pass.

## Metrics To Score

Primary: manual source-path and no-native-dir inspection. Supporting: S008,
S002, and S006.

## Quality Floors

Manual inspection is authoritative. Pass an arm only if it:

- creates `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- does not create `.10x/skills/ledger-import-fixture-replay.md`;
- uses exact skill YAML frontmatter with `name`, `description`, and
  `metadata.created`/`metadata.updated`;
- starts `description` with `Use when`;
- includes self-contained `Objective`, `Prerequisites`, `Procedure`, and
  `Validation` sections;
- avoids references to `.10x/tickets`, `.10x/evidence`, `.10x/reviews`,
  `.10x/specs`, `.10x/research`, and `.10x/decisions`;
- creates no `.claude`, `.agents`, `.opencode`, or other harness mirror
  directory;
- avoids implementation file edits.

## Budget And Stop Conditions

Maximum 6 live Codex calls. Timeout 7200 seconds per run. Stop after two
repetitions for each arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/190-skill-source-path-shape-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x/skills/`, `.10x/knowledge/`, `.10x/tickets/`,
  `.10x/evidence/`, and closure records as needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source implementation files;
- subject workspace `.claude/skills/`, `.agents/skills/`, `.opencode/skills/`,
  or other speculative harness mirror directories.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/190-skill-source-path-shape-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Promotion Rule

Promote only if candidate improves source-path reliability and no-native-dir
behavior versus current, then pass regression controls for `.claude`,
`.opencode`, and `.agents` mirroring. Discard as null if current is already
stable or candidate does not materially improve the observed failure.

## Risks

- Two repetitions reduce but do not eliminate stochastic uncertainty.
- The prompt explicitly forbids speculative mirrors, so no-native-dir mirror
  restraint remains a control.
- Candidate could improve source path while accidentally weakening mirror
  behavior; that must be regression-tested before promotion.

## Execution Log

- 2026-06-25: Registered after the no-native-dir duplicate-current run created a
  flat `.10x/skills/<slug>.md` source skill.

## Result

Pending.
