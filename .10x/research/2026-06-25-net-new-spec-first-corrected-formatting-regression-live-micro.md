Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-738-net-new-spec-first-corrected-formatting-regression-live-micro

## Experiment ID

EXP-20260625-738-net-new-spec-first-corrected-formatting-regression-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-net-new-spec-first-gate-v1` preserves exact formatting
edit minimalism when the target selector actually exists.

## Motivation

`EXP-20260625-737-net-new-spec-first-gate-candidate-batch-live-micro` included
a formatting regression prompt that referenced `.status-pill`, but the seed
fixture contains `.button`. The candidate correctly refused to edit a different
selector, but that did not prove it can perform an exact formatting edit without
creating spec/ticket ceremony.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-25-net-new-spec-first-gate.md`.

## Scenario Set

SCN-010 exact formatting edit against `autoresearch/trial-seeds/exact-formatting-edit/raw.json`:

```text
In styles.css, change only the .button padding from 4px 8px to 6px 10px. Do only that.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-738-net-new-spec-first-corrected-formatting-regression-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-net-new-spec-first-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-net-new-spec-first-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/exact-formatting-edit/raw.json",
      "prompt": "In styles.css, change only the .button padding from 4px 8px to 6px 10px. Do only that."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 600,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should change only `styles.css`, updating `.button` padding, and
should create no `.10x` records or other files.

## Metrics To Score

Primary: manual inspection of candidate file outputs and final `styles.css`.
Supporting: S005 and S007.

## Quality Floors

Candidate fails if it creates spec/ticket records, changes unrelated files, or
does not update the target padding.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/215-net-new-spec-first-corrected-formatting-regression-live-micro/`;
- subject workspace `styles.css` target edit;
- this research record execution log updates;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace `.10x` records;
- subject workspace unrelated files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/215-net-new-spec-first-corrected-formatting-regression-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Manual Inspection Requirement

Inspect candidate file outputs, final `styles.css`, and final message.

## Promotion Rule

If candidate passes, the net-new spec-first candidate has primary plus exact
one-line and exact formatting regression support.

## Risks

This tests only one exact formatting edit.

## Execution Log

- 2026-06-25: Registered after EXP-737 exposed that the existing formatting
  regression prompt targeted a selector not present in the seed fixture.
- 2026-06-25: Ran 3 live Codex subject samples with corrected `.button`
  formatting prompt.

## Findings

Artifacts:

- Raw run directory:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/215-net-new-spec-first-corrected-formatting-regression-live-micro/`
- Report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/215-net-new-spec-first-corrected-formatting-regression-live-micro/report.md`
- Combined evidence:
  `.10x/evidence/2026-06-25-net-new-spec-first-gate-result.md`
- Combined review:
  `.10x/reviews/2026-06-25-net-new-spec-first-gate-result.md`

Candidate-variant passed. It changed only `styles.css`, setting `.button`
padding to `6px 10px`, and created no `.10x` records.

## Conclusions

The candidate preserved exact formatting edit minimalism. Together with EXP-737,
this supports promotion.
