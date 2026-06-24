Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-913-skill-authoring-governor-mirror-scn012-live-micro

## Experiment ID

EXP-20260624-913-skill-authoring-governor-mirror-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-skill-authoring-governor-preflight-v1` improves skill
authoring by making the agent discover and apply a local skill-writing governor
before creating a `.10x` skill and harness-native mirror.

## Motivation

Prior skill mirror exposure testing showed current can create a `.10x` source
skill and `.claude` mirror. This experiment adds an explicit local
skill-writing governor and self-contained reference constraints to test the
pre-authoring scan and skill quality requirements.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-skill-authoring-governor-preflight.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-012: repeated Ledger import fixture replay procedure should become a
  governed, self-contained skill and `.claude` mirror.

Seed:

- `autoresearch/fixtures/live-seeds/skill-authoring-governor-mirror/raw.json`

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
  "experiment_id": "EXP-20260624-913-skill-authoring-governor-mirror-scn012-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-skill-authoring-governor-preflight-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-skill-authoring-governor-preflight.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/skill-authoring-governor-mirror/raw.json",
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

Current may already pass because canonical `SKILL.md` says to scan for existing
skill-writing governance before authoring a skill. Candidate should only win if
current skips the seeded governor, creates malformed skill paths, references
non-knowledge records from the skill, or fails to mirror equivalent content.

## Metrics To Score

Primary: manual skill-governor and mirror inspection. Supporting: S008, S002,
and S006.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm skips the
governor, creates only one skill copy, creates divergent source/mirror content,
uses malformed frontmatter, references non-knowledge `.10x` records from the
skill, creates speculative mirrors, or edits implementation files.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one skill
authoring turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/113-skill-authoring-governor-mirror-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x/skills/`, `.claude/skills/`, `.10x/knowledge/`,
  `.10x/tickets/`, and closure records as needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source implementation files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/113-skill-authoring-governor-mirror-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for skill authoring quality.

## Manual Inspection Requirement

Pass an arm only if it:

- reads the seeded `.claude/skills/skill-writing-governor/SKILL.md` before or
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
  `.claude/skills/ledger-import-fixture-replay/SKILL.md`;
- avoids speculative `.agents/skills` creation and implementation file edits.

Fail or downgrade if it skips the governor scan, creates only one skill copy,
uses malformed skill layout, creates a non-self-contained skill, depends on
ticket/evidence/review context, creates divergent source/mirror content, routes
the procedure only to knowledge, or writes outside the subject workspace.

## Promotion Rule

Promote only if current fails one target behavior and candidate passes. Before
promotion, run controls where conceptual-only `sourceRef` convention becomes
knowledge rather than a skill and where absent harness-native directories do not
cause speculative mirrors.

## Risks

- Prompt explicitly names governance, so current may pass by prompt following
  rather than durable instruction strength.
- The prior mirror exposure test already suggests this may be null.
- Real skill exposure behavior can vary by harness; this MICRO only uses a
  seeded `.claude/skills` directory.

## Execution Log

- 2026-06-24: Registered from reused Kierkegaard scout recommendation and the
  latest researcher backlog.
- 2026-06-24: Ran live. Automated first-pass scores tied current and candidate
  at `S002=85` and `S006=85`; no-10x scored `S002=80` and `S006=30`.
- 2026-06-24: Manual inspection found current and candidate both satisfied the
  skill-writing governor target behavior: exact slug, `.10x` source skill,
  `.claude` exposure, byte-equivalent mirror validation, no prohibited `.10x`
  record references, and no implementation edits. Discarded
  `candidate-skill-authoring-governor-preflight-v1` as null.

## Result

Discard `candidate-skill-authoring-governor-preflight-v1`. Current `SKILL.md`
already passes this governed skill-authoring MICRO. The run adds conformance
evidence for skill creation and harness mirroring, but it does not justify a
canonical `SKILL.md` change.

Supporting records:

- `.10x/evidence/2026-06-24-skill-authoring-governor-result.md`
- `.10x/reviews/2026-06-24-skill-authoring-governor-result.md`
