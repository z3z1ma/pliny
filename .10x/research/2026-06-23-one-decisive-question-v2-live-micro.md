Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-806-one-decisive-question-v2-live-micro

## Experiment ID

EXP-20260623-806-one-decisive-question-v2-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-one-decisive-question-v2` will preserve the concise
one-question style while improving S001 by explicitly asking for the missing
behavior, scope, constraint, or acceptance criterion.

## Motivation

The v1 clean rerun improved S007 slightly but lost S001 because the question was
too vague for an execution-critical ambiguity. V2 keeps the one-question
discipline but requires the question to name the missing execution dimension.

## Method Tier

MICRO. One narrow ambiguous-request scenario.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-one-decisive-question-v2.md`.

## Control

Generated workspaces, suppressed project instruction paths, `--disable plugins`,
and `--ignore-user-config`.

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
  "experiment_id": "EXP-20260623-806-one-decisive-question-v2-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-one-decisive-question-v2",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-one-decisive-question-v2.md"
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

Candidate should improve over v1 on S001 by using behavior/scope/acceptance
criterion wording, while retaining S007 brevity and recommendation quality.

## Metrics To Score

Primary: S001 and S007.

## Quality Floors

S001 active floor 80.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one first
turn unless a continuation is needed for transcript completeness.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/007-one-decisive-question-v2-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv` row after scoring;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/007-one-decisive-question-v2-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for S007.

## Manual Inspection Requirement

Inspect all raw transcripts, file outputs, workspace manifests, and report.

## Known Risks And Confounders

- Single live repetition is noisy.
- Formulaic wording can satisfy the heuristic without genuinely improving
  behavior, so manual inspection matters.

## Execution Log

- 2026-06-23: Registered v2 experiment before execution.
- 2026-06-23: Cancelled during first live run after operator correctly
  challenged the one-question optimization direction. The run was interrupted
  before producing scoreable raw artifacts. Partial prompt artifacts may exist
  under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/007-one-decisive-question-v2-live-micro/`
  and must not be used as evidence.

## Score Artifacts

None. Run cancelled before scoreable output.

## Manual Inspection Findings

The hypothesis optimized the wrong surface. `SKILL.md` already says
interrogation is mandatory and relentless, but never indiscriminate. A candidate
that drives toward one question risks suppressing legitimate ambiguity
reduction in complex software work.

## Final Verdict

Cancelled. Do not pursue one-question discipline as an optimization target.
Future candidates should optimize question materiality, dependency ordering,
and completeness of ambiguity resolution rather than question count.
