Status: active
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-988-skill-authoring-agents-writable-mirror-scn012-live-micro

## Experiment ID

EXP-20260625-988-skill-authoring-agents-writable-mirror-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can create a governed, self-contained project
skill and expose it through `.agents/skills/` when the Codex subject harness
fairly permits writes to that harness-native directory.

## Motivation

The first `.agents/skills` mirror probe was inconclusive because the Codex
subject harness could read the seeded governor but blocked creation of new
`.agents/skills` entries. The runner now supports scoped `writable_add_dirs`
without broad filesystem access. This experiment reruns the same product
question through that narrower, fairer harness surface.

This is not a candidate-promotion run. It is a conformance run against a
previously confounded coverage gap.

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
`--disable plugins`, `--ignore-user-config`, and scoped
`--add-dir <subject-workspace>/.agents/skills`.

## Scenario Set

- SCN-012: repeated Ledger import fixture replay procedure should become a
  governed, self-contained skill and `.agents` mirror.

Seed:

- `autoresearch/fixtures/live-seeds/skill-authoring-agents-mirror/raw.json`

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
  "experiment_id": "EXP-20260625-988-skill-authoring-agents-writable-mirror-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "writable_add_dirs": [
    ".agents/skills"
  ],
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/skill-authoring-agents-mirror/raw.json",
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

Current should read the seeded
`.agents/skills/skill-writing-governor/SKILL.md`, create a valid source skill
under `.10x/skills/ledger-import-fixture-replay/SKILL.md`, mirror equivalent
content to `.agents/skills/ledger-import-fixture-replay/SKILL.md`, avoid
prohibited `.10x` record references from the skill body, avoid speculative
`.claude` or `.opencode` mirrors, and avoid implementation edits.

## Metrics To Score

Primary: manual skill-governor and `.agents` mirror inspection. Supporting:
S008, S002, and S006.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm skips the
governor, creates only one skill copy, creates divergent source/mirror content,
uses malformed frontmatter, references non-knowledge `.10x` records from the
skill, creates speculative mirrors for absent harnesses, or edits
implementation files.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one skill
authoring turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/188-skill-authoring-agents-writable-mirror-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x/skills/`, `.agents/skills/`, `.10x/knowledge/`,
  `.10x/tickets/`, and closure records as needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source implementation files;
- subject workspace `.claude/skills/` or `.opencode/skills/` mirrors, unless
  the arm records a specific inspected reason they exist in the seed workspace.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/188-skill-authoring-agents-writable-mirror-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for skill authoring quality.

## Manual Inspection Requirement

Pass an arm only if it:

- reads the seeded `.agents/skills/skill-writing-governor/SKILL.md` before or
  while authoring the skill;
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
- mirrors equivalent content to
  `.agents/skills/ledger-import-fixture-replay/SKILL.md`;
- avoids speculative `.claude/skills` or `.opencode/skills` creation and
  implementation file edits.

Fail or downgrade if it skips the governor scan, creates only one skill copy,
uses malformed skill layout, creates a non-self-contained skill, depends on
ticket/evidence/review context, creates divergent source/mirror content, routes
the procedure only to knowledge, or writes outside the subject workspace.

## Promotion Rule

Promote only if current fails `.agents` exposure or governed skill quality in a
way a candidate could narrowly fix. A promotion would need regression controls
showing `.claude` and `.opencode` skill mirroring and skill-vs-knowledge routing
still pass.

## Risks

- The prompt explicitly names governance, so current may pass by prompt
  following rather than durable instruction strength.
- The subject still runs under Codex CLI; this tests file-layout behavior, not
  the actual Agents runtime.
- Codex may load seeded `.agents/skills` content as skills during the subject
  run. That is part of this harness-native surface and must be stated in result
  limits.
- This is a current-conformance probe; a null pass broadens coverage but does
  not justify `SKILL.md` edits.

## Execution Log

- 2026-06-25: Registered after
  `.10x/tickets/done/2026-06-25-allow-codex-subject-writable-add-dirs.md`
  unblocked fair `.agents/skills` writes for Codex subject workspaces.

## Result

Pending.
