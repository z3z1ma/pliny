Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-807-information-gain-scn001-live-micro

## Experiment ID

EXP-20260623-807-information-gain-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-information-gain-interrogation-v1` improves ambiguous
first-turn shaping by asking all necessary blocker questions in dependency
order, with each question tied to the execution decision it resolves.

## Motivation

Fresh review concluded that 10x should not optimize for fewer questions. It
should optimize for eliminating execution-critical ambiguity before code,
tickets, or specs pretend the work is clear.

## Method Tier

MICRO. One narrow SCN-001 ambiguous implementation request.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-information-gain-interrogation.md`.

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
  "experiment_id": "EXP-20260623-807-information-gain-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-information-gain-interrogation-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-information-gain-interrogation.md"
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

Candidate should avoid implementation, inspect first, and ask a small set of
blocker questions tied to behavior, scope, acceptance criteria, and launch
constraints. Current 10x may perform well; the candidate must improve question
materiality or clarity to justify mutation.

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
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for S007.

## Manual Inspection Requirement

Inspect all raw transcripts, file outputs, workspace manifests, and report.

## Known Risks And Confounders

- Current 10x may already be strong on this behavior.
- S007 word-count heuristic may penalize longer but justified interviews.

## Execution Log

- 2026-06-23: Registered before execution.
- 2026-06-23: Ran live Codex MICRO with three arms. Initial automated scoring
  exposed a scorer bug: `.10x` record writes were treated as unauthorized
  implementation writes for S001.
- 2026-06-23: Fixed the S001 record-write floor bug under
  `.10x/tickets/done/2026-06-23-fix-s001-record-write-floor.md`, reran tests,
  rescored the raw artifacts, regenerated the report with campaign metadata,
  and appended `results.tsv` with status `mutate`.

## Score Artifacts

- Raw artifacts:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro/raw/`
- Score artifacts:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro/scores/`
- Report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro/report.md`
- Evidence:
  `.10x/evidence/2026-06-23-information-gain-scn001-live-micro.md`

## Manual Inspection Findings

- Corrected score vector:
  - current-10x: `S001=100;S007=45`
  - no-10x-control: `S001=75 floor;S007=10`
  - candidate-variant: `S001=80;S007=45`
- Current 10x asked five useful blocker questions and recommended a narrow
  sales-readiness release.
- Candidate asked five blocker questions with decision-rationale annotations,
  but it did not outperform current 10x and was more verbose.
- No-10x control refused implementation in this sample, but did not create
  durable records and remained below the S001 active floor.
- The candidate's useful direction is not "ask fewer questions"; it is "ask
  necessary questions while naming why each answer changes execution." The next
  mutation should compress that behavior and explicitly name ambiguity.

## Final Verdict

`mutate`, not promoted. The candidate preserved discipline but underperformed
current 10x on S001 and tied on S007.
