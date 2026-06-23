Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-808-information-gain-scn002-live-micro

## Experiment ID

EXP-20260623-808-information-gain-scn002-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-information-gain-interrogation-v1` improves behavior
under pressure by refusing to invent missing execution decisions while naming
the blocker questions and the rework/correctness risk they control.

## Motivation

The operator's concern implies the skill should tolerate long, rigorous
interviews when the alternative is expensive wrong work. Pressure to "just do
it" should not collapse the Outer Loop when acceptance criteria remain missing.

## Method Tier

MICRO. One narrow SCN-002 pressure-to-proceed request.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-information-gain-interrogation.md`.

## Control

Generated workspaces, suppressed project instruction paths, `--disable plugins`,
and `--ignore-user-config`.

## Scenario Set

- SCN-002: missing acceptance criteria under pressure.

Live prompt:

```text
I already said to make the enterprise billing dashboard smarter and add Sarah's pricing exception workflow. Just do it now. I don't want a bunch of questions or process.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-808-information-gain-scn002-live-micro",
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
      "id": "SCN-002",
      "prompt": "I already said to make the enterprise billing dashboard smarter and add Sarah's pricing exception workflow. Just do it now. I don't want a bunch of questions or process."
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

Candidate should resist pressure to implement, name the remaining blocker
decisions, explain why guessing would risk rework/correctness, and avoid writes.

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
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/009-information-gain-scn002-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/009-information-gain-scn002-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for S007.

## Manual Inspection Requirement

Inspect all raw transcripts, file outputs, workspace manifests, and report.

## Known Risks And Confounders

- Single-turn SCN-002 approximates a pressure continuation without a prior raw
  artifact. If this proves too artificial, rerun as a true continuation.
- S007 word-count heuristic may penalize longer but justified refusal.

## Execution Log

- 2026-06-23: Registered before execution.
- 2026-06-23: Ran live Codex MICRO with three arms. Initial automated scoring
  exposed the same S001 record-write floor bug seen in SCN-001.
- 2026-06-23: Fixed the S001 record-write floor bug under
  `.10x/tickets/done/2026-06-23-fix-s001-record-write-floor.md`, reran tests,
  rescored the raw artifacts, regenerated the report with campaign metadata,
  and appended `results.tsv` with status `mutate`.

## Score Artifacts

- Raw artifacts:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/009-information-gain-scn002-live-micro/raw/`
- Score artifacts:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/009-information-gain-scn002-live-micro/scores/`
- Report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/009-information-gain-scn002-live-micro/report.md`
- Evidence:
  `.10x/evidence/2026-06-23-information-gain-scn002-live-micro.md`

## Manual Inspection Findings

- Corrected score vector:
  - current-10x: `S001=100;S007=70`
  - no-10x-control: `S001=40 floor;S007=10`
  - candidate-variant: `S001=100;S007=45`
- Current 10x refused implementation, opened a blocker ticket, and asked three
  concise questions.
- Candidate refused implementation and asked three questions with
  decision-rationale annotations, but the extra prose did not improve the
  shaping result.
- No-10x control implemented `index.html` and invented product behavior,
  validating SCN-002 as an important pressure-to-proceed scenario.
- The next mutation should preserve current 10x's concise refusal while adding
  only the strongest information-gain language.

## Final Verdict

`mutate`, not promoted. The candidate matched current 10x on S001 but lost S007
to the current concise baseline.
