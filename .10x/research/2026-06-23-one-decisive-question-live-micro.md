Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-804-one-decisive-question-live-micro

## Experiment ID

EXP-20260623-804-one-decisive-question-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: adding a narrow "one decisive upstream question" clarification rule
will improve S001/S007 behavior on ambiguous requests by reducing question
sprawl while preserving the no-implementation Outer Loop gate.

## Motivation

The operator explicitly identified question quality, enough targeted questions,
and not jumping straight into implementation as the current optimization focus.
The candidate tests whether a small instruction overlay improves that behavior
without adding broader process.

## Method Tier

MICRO. The run targets one behavior: first-turn shaping under ambiguity.

## Variants

- no-10x-control: minimal Codex instruction, isolated from project instruction
  files.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-one-decisive-question.md`.

## Control

The no-10x control receives only minimal direct-task instructions. The Codex
subject runner uses generated workspaces, `--disable plugins`,
`--ignore-user-config`, and suppressed project instruction paths for known
project-level instruction files.

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
  "experiment_id": "EXP-20260623-804-one-decisive-question-live-micro",
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

## Subject Agent And Model

Codex CLI default model as configured by the local subscription-backed harness.

## Harness Target

`codex-cli` live subject runner through `autoresearch/run_once.py`.

## Scenario And Workspace Procedure

The runner creates isolated workspaces for each arm unless continuing from a
prior raw artifact. This first turn has no prior raw artifact.

## Repetition Count

One repetition per arm. This is exploratory MICRO evidence, not a stable effect
size estimate.

## Prediction

Expected:

- no-10x-control likely implements or scaffolds, lowering S001/S007.
- current-10x should ask a material question and avoid implementation.
- candidate-variant should be more concise than current and ask one upstream
  behavior/scope question with a recommendation or explicit lack of context.

Backfire:

- candidate asks too little and misses acceptance criteria;
- candidate over-indexes on the one-question rule and fails to inspect or
  record context;
- candidate writes implementation despite ambiguity.

## Metrics To Score

Primary: S001 and S007.

## Quality Floors

S001 active floor 80. S007 has no active floor but is the target shaping score.

## Budget And Stop Conditions

Maximum 3 harness runs. Timeout 7200 seconds per run to allow slow Codex
reasoning. Stop after one first-turn run unless a subject asks a material
question whose answer should be provided through a registered continuation.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/005-one-decisive-question-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv` row after scoring;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/005-one-decisive-question-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for S007 shaping quality.

## Manual Inspection Requirement

Inspect all three raw transcripts, file outputs, workspace manifests, and the
report before deciding keep/discard/mutate.

## Promotion Criteria

Promotion is not possible from this run alone. A keep/mutate verdict can only
support a follow-up run.

## Known Risks And Confounders

- Empty generated workspaces may reduce inspect-before-ask signal.
- S007 scorer is keyword-based and low-confidence.
- Single live repetition is noisy.
- Codex home/system context is not fully controlled.

## Execution Log

- 2026-06-23: Registered experiment and candidate before execution.
- 2026-06-23: First live run completed at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/005-one-decisive-question-live-micro/`.
  Candidate scored `S001=65;S007=85` versus current `S001=40;S007=20`.
  Manual inspection then found the runner had dropped Codex command execution
  events from `tool_invocations`, confounding the S001 inspect-before-ask
  component. Tool-event fix evidence:
  `.10x/evidence/2026-06-23-codex-tool-event-capture.md`.

## Score Artifacts

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/005-one-decisive-question-live-micro/report.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/005-one-decisive-question-live-micro/campaign.json`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/005-one-decisive-question-live-micro/canonical_guard.json`

## Manual Inspection Findings

- Candidate response was concise, inspected the empty workspace, avoided file
  writes, named the single blocking decision, provided a recommended default,
  and asked one concrete question.
- Current 10x also asked a useful question but wrote a shaping ticket inside
  the generated workspace, triggering the S001 unauthorized-implementation cap
  in the automated scorer.
- Raw Codex JSONL for current and candidate showed command execution events,
  but raw artifacts had empty `tool_invocations`. This made the automated S001
  values unreliable for inspect-before-ask comparison.

## Final Verdict

Review/confounded. The behavioral signal is promising for the candidate, but
the affected S001 score must be rerun after the tool event capture fix before
using the result to keep or mutate the candidate.
