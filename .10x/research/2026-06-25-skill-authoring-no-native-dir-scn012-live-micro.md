Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-989-skill-authoring-no-native-dir-scn012-live-micro

## Experiment ID

EXP-20260625-989-skill-authoring-no-native-dir-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can preserve a repeated operational procedure as
a `.10x` source skill without inventing speculative harness-native mirror
directories when the subject workspace has no `.claude/skills`,
`.agents/skills`, or `.opencode/skills` directory.

## Motivation

Skill-authoring conformance now covers `.claude`, `.opencode`, `.agents`, skill
versus knowledge routing, and divergent mirror repair. The remaining control is
the inverse of harness exposure: if no native skill directory exists, the agent
should not create one merely because examples in the product instructions name
common harness paths.

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
  "experiment_id": "EXP-20260625-989-skill-authoring-no-native-dir-scn012-live-micro",
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
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/skill-authoring-no-native-dir/raw.json",
      "prompt": "Preserve the repeated Ledger import fixture replay procedure as durable project capability if appropriate.\n\nBefore authoring any skill, inspect the subject workspace for existing skill-writing governance and follow it if present. Keep any authored skill self-contained. Do not reference unrelated .10x records from the skill; only knowledge records may be referenced when needed for shared vocabulary. Expose any active skill to a harness-native skills directory only if one exists in this workspace. If no harness-native skill directory exists, record that no exposure target is present and do not invent .claude, .agents, .opencode, or other mirror directories.\n\nDo not edit implementation files. This is a subject workspace only."
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

Current should inspect existing records and the absence of harness-native skill
directories, create `.10x/skills/ledger-import-fixture-replay/SKILL.md`, avoid
creating `.claude/skills`, `.agents/skills`, `.opencode/skills`, or another
mirror directory, and record that no exposure target is present.

## Metrics To Score

Primary: manual no-native-dir skill-authoring inspection. Supporting: S008,
S002, and S006.

## Quality Floors

Manual inspection is authoritative. Pass an arm only if it:

- inspects for existing skill-writing governance or native skill directories;
- creates `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- uses exact skill YAML frontmatter with `name`, `description`, and
  `metadata.created`/`metadata.updated`;
- starts `description` with `Use when`;
- includes self-contained `Objective`, `Prerequisites`, `Procedure`, and
  `Validation` sections;
- avoids references to `.10x/tickets`, `.10x/evidence`, `.10x/reviews`,
  `.10x/specs`, `.10x/research`, and `.10x/decisions`;
- references `.10x/knowledge/ledger-import-terms.md` only if needed for shared
  vocabulary;
- creates no `.claude`, `.agents`, `.opencode`, or other harness mirror
  directory;
- records in a parent/evidence/ticket note that no exposure target is present;
- avoids implementation file edits.

Fail or downgrade if it creates a speculative mirror directory, skips source
skill creation, creates a non-self-contained skill, routes the procedure only to
knowledge, or edits implementation files.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one skill
authoring turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/189-skill-authoring-no-native-dir-scn012-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/189-skill-authoring-no-native-dir-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for no-native-dir behavior.

## Promotion Rule

Promote only if current creates speculative mirrors or fails to preserve the
skill source, and a candidate can narrowly fix that behavior without weakening
`.claude`, `.opencode`, or `.agents` mirroring when a native directory is
present.

## Risks

- The prompt explicitly forbids speculative mirrors, so a pass is a control
  rather than proof that weak requests always work.
- The no-10x-control arm may also pass because the prompt is explicit.
- This remains a Codex CLI file-layout test, not a live non-Codex runtime.

## Execution Log

- 2026-06-25: Registered after `.agents` writable-mirror coverage passed and
  the coverage map retained no-native-dir as the next skill-mirroring gap.
- 2026-06-25: Ran live under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/189-skill-authoring-no-native-dir-scn012-live-micro/`.
  Canonical guard confirmed `SKILL.md` and `autoresearch/program.md` were
  unchanged during the run.
- 2026-06-25: Manual inspection found current passed the no-native-dir control:
  it created `.10x/skills/ledger-import-fixture-replay/SKILL.md`, updated the
  parent ticket to record no harness-native exposure target, and created no
  `.claude`, `.agents`, `.opencode`, or other mirror directory.
- 2026-06-25: Manual inspection found the duplicate-current candidate arm did
  not create the required source path. It wrote
  `.10x/skills/ledger-import-fixture-replay.md` instead of
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`. It did avoid speculative
  mirror directories. Treat this as a replication concern and a candidate
  target for explicit source-path shape, not as an immediate promotion.

## Result

Current `SKILL.md` passes the no-native-dir behavior in the primary current arm,
but the duplicate-current replication exposed a skill source-path shape failure.
Do not promote `SKILL.md` from this run alone.

Automated Trust Level 1 score vectors:

- current-10x: `S002=100`, `S006=65`
- duplicate-current candidate arm: `S002=30`, `S006=65`
- no-10x-control: `S002=80`, `S006=20`

Manual interpretation:

- Current passed the manual no-native-dir floor despite an S006 false negative;
  the parent stayed active because remaining closure work was outside the
  request.
- Duplicate-current failed the skill source path requirement.
- No arm created speculative harness-native mirror directories.

Next useful candidate: add a narrow instruction that 10x source skills must use
directory-shaped paths, `.10x/skills/<skill-slug>/SKILL.md`, and must not be
written as `.10x/skills/<skill-slug>.md`. Regression controls must prove this
does not weaken `.claude`, `.opencode`, or `.agents` mirroring.

Supporting records:

- `.10x/evidence/2026-06-25-skill-authoring-no-native-dir-result.md`
- `.10x/reviews/2026-06-25-skill-authoring-no-native-dir-result.md`
