Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-919-skill-vs-knowledge-routing-conceptual-fact-scn012-live-micro

## Experiment ID

EXP-20260624-919-skill-vs-knowledge-routing-conceptual-fact-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` routes durable conceptual vocabulary to
knowledge, not to a skill or harness-native mirror, when no repeatable
operational procedure exists.

## Motivation

The governed skill-authoring MICRO showed current can create and mirror a skill
when a true procedure exists. This control tests the opposite side of the
boundary: a durable naming convention should become knowledge, not a skill.

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

- SCN-012: retrospective extraction after child completion surfaces one
  conceptual naming convention that should be preserved as knowledge.

Seed:

- `autoresearch/fixtures/live-seeds/skill-authoring-governor-mirror/raw.json`

Prompt:

```text
The only durable learning to preserve from this Ledger import workstream is conceptual vocabulary: the settled domain name is `sourceRef`, not `externalId`. Do not create a skill unless there is a repeatable operational procedure to expose. Preserve this context in the correct 10x record shape and avoid harness-native skill mirroring unless a real skill exists. Do not edit implementation files.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-919-skill-vs-knowledge-routing-conceptual-fact-scn012-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/skill-authoring-governor-mirror/raw.json",
      "prompt": "The only durable learning to preserve from this Ledger import workstream is conceptual vocabulary: the settled domain name is `sourceRef`, not `externalId`. Do not create a skill unless there is a repeatable operational procedure to expose. Preserve this context in the correct 10x record shape and avoid harness-native skill mirroring unless a real skill exists. Do not edit implementation files."
    }
  ],
  "budget": {
    "max_harness_runs": 2,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should create or update `.10x/knowledge/ledger-import-terms.md`, avoid
creating `.10x/skills/` or `.claude/skills/` records, and avoid implementation
edits.

## Metrics To Score

Primary: manual record routing inspection. Supporting: S002, S005, and S008.

## Quality Floors

Fail or downgrade if an arm creates a skill for conceptual vocabulary, mirrors
to harness-native skill directories without a real skill, fails to preserve the
`sourceRef` convention, or edits implementation files.

## Budget And Stop Conditions

Maximum 2 live Codex calls. Timeout 7200 seconds per run. Stop after one
retrospective routing turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/119-skill-vs-knowledge-routing-conceptual-fact-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x/knowledge/` records and parent ticket notes.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files;
- subject workspace `.10x/skills/` or harness-native skill directories unless
  the arm identifies a true repeatable operational procedure.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/119-skill-vs-knowledge-routing-conceptual-fact-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for skill-vs-knowledge routing.

## Manual Inspection Requirement

Pass an arm only if it preserves `sourceRef` as knowledge, avoids creating or
mirroring a skill, and does not edit implementation files.

## Promotion Rule

No behavioral candidate is under test; `candidate-variant` duplicates
`current-10x` only to satisfy the current runner's fixed arm contract. If
current creates a skill for conceptual vocabulary, create a narrow candidate for
knowledge/skill routing.

## Risks

The prompt explicitly says the learning is conceptual, so this is a positive
control for routing rather than an adversarial ambiguous skill request.

## Execution Log

- 2026-06-24: Registered from the conformance map and scout recommendations.
- 2026-06-24: Added duplicate `candidate-variant` arm after the runner rejected
  two-arm live definitions.
