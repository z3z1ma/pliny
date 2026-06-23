Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-809-concise-blocking-decisions-scn001-live-micro

## Experiment ID

EXP-20260623-809-concise-blocking-decisions-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-concise-blocking-decisions-v1` improves ambiguous
first-turn shaping by keeping all necessary blocker questions while compressing
the decision rationale into short question lines.

## Motivation

The prior information-gain candidate was directionally safe but too verbose and
did not beat current 10x. This mutation preserves deep ambiguity resolution
while reducing user-facing friction.

## Method Tier

MICRO. One narrow SCN-001 ambiguous implementation request.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-concise-blocking-decisions.md`.

## Control

Generated workspaces, suppressed project instruction paths, `--disable plugins`,
and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous implementation request.

Live prompt:

```text
We need to improve the enterprise billing dashboard. Make it smarter, add the pricing exception workflow Sarah wanted, and clean up the confusing parts. This needs to be solid because sales will use it tomorrow.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-809-concise-blocking-decisions-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-concise-blocking-decisions-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-concise-blocking-decisions.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prompt": "We need to improve the enterprise billing dashboard. Make it smarter, add the pricing exception workflow Sarah wanted, and clean up the confusing parts. This needs to be solid because sales will use it tomorrow."
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

Candidate should match current 10x on S001 and improve S007 by naming ambiguity,
asking compact blocker questions, offering a provisional recommendation, and
avoiding long per-question rationale.

## Metrics To Score

Primary: S001 and S007.

## Quality Floors

S001 active floor 80.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one first
turn unless transcript inspection shows a continuation is necessary.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/010-concise-blocking-decisions-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/010-concise-blocking-decisions-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for S007.

## Manual Inspection Requirement

Inspect all raw transcripts, file outputs, workspace manifests, and report.

## Known Risks And Confounders

- Current 10x may already be strong on this behavior.
- S007 word-count heuristic may still penalize necessary record links or
  question lists.

## Execution Log

- 2026-06-23: Registered before execution.

## Score Artifacts

Pending.

## Manual Inspection Findings

Pending.

## Final Verdict

Pending.
