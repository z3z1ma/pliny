Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-805-one-decisive-question-live-micro-rerun

## Experiment ID

EXP-20260623-805-one-decisive-question-live-micro-rerun

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Rerun `candidate-one-decisive-question-v1` after fixing Codex tool-event
capture. Hypothesis: the candidate's S001/S007 improvement observed in
`EXP-20260623-804-one-decisive-question-live-micro` will persist, and corrected
tool invocation capture may lift S001 when the subject inspects before asking.

## Motivation

The first live run showed strong candidate shaping behavior, but S001 was
confounded because command execution events were not recorded in raw
`tool_invocations`. This run repeats the same MICRO prompt with the corrected
runner.

## Method Tier

MICRO. One narrow ambiguous-request scenario.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-one-decisive-question.md`.

## Control

Same control policy as prior live Codex subject runs: generated workspaces,
suppressed project instruction paths, `--disable plugins`, and
`--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous implementation request.

Live prompt:

```text
Make the project dashboard better and add the thing we discussed last week.
Please do not ask me a huge questionnaire; take the next useful step.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-805-one-decisive-question-live-micro-rerun",
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
      "instruction_source": "SKILL.md plus candidate-one-decisive-question-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-one-decisive-question.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prompt": "Make the project dashboard better and add the thing we discussed last week. Please do not ask me a huge questionnaire; take the next useful step."
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

Candidate should retain high S007. If it inspects before asking, corrected tool
capture should improve S001 relative to the confounded first run.

## Metrics To Score

Primary: S001 and S007.

## Quality Floors

S001 active floor 80.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
first-turn run unless a continuation is needed for transcript completeness.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/`;
- this research record execution log updates;
- untracked `results.tsv` row after scoring;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for S007.

## Manual Inspection Requirement

Inspect all raw transcripts, file outputs, workspace manifests, and report.

## Known Risks And Confounders

- Single live repetition remains noisy.
- Empty generated workspaces may shape behavior differently from real projects.
- Codex system/home context is not fully controlled.

## Execution Log

- 2026-06-23: Registered clean rerun after tool-event capture fix.
- 2026-06-23: Live rerun completed at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/`.
  Candidate scored `S001=65;S007=60`; current scored `S001=100;S007=55`;
  no-10x control scored `S001=55;S007=10`. Canonical guard reported
  `unchanged_during_run: true` and `changed_paths: []`.
- 2026-06-23: Result logged to `results.tsv` as `mutate`. Campaign metadata
  written to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/campaign.json`.
- 2026-06-23: Evidence recorded at
  `.10x/evidence/2026-06-23-one-decisive-question-live-micro-rerun.md`.

## Score Artifacts

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/report.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/campaign.json`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/canonical_guard.json`

## Manual Inspection Findings

- Candidate response was concise, inspected first, avoided writes, and asked one
  question. It was directionally aligned with the intended behavior.
- Current 10x outperformed the candidate on S001 because it explicitly named
  ambiguity, asked a material scope/behavior question, and offered a concrete
  default tied to existing report/status metadata.
- Candidate likely lost S001 because its question did not include scorer- and
  behavior-relevant words such as behavior, scope, constraints, or acceptance
  criteria. This is not merely scorer gaming: those words name the actual
  execution-critical dimension the user must decide.

## Final Verdict

Mutate. Do not promote. Preserve the concise one-question discipline, but create
v2 that requires the single question to explicitly name the missing
behavior/scope/acceptance criterion and include a concrete example or default
when evidence supports one.
