Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-740-post-spec-first-existing-spec-and-no-code-controls-live-micro

## Experiment ID

EXP-20260626-740-post-spec-first-existing-spec-and-no-code-controls-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after the net-new spec-first promotion, canonical `SKILL.md` will
reuse an existing active specification without duplicating it, and will still
give no-code/reuse answers when active records and source already establish that
building is the wrong next action.

## Motivation

The spec-first promotion fixed direct implementation after ratified net-new
behavior, but it adds gravity toward specifications. The immediate regression
risk is over-specification: creating duplicate specs when an active spec already
exists, or creating spec/ticket ceremony when the correct answer is no code.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay.

## Control

No-10x-control is calibration only. Candidate-variant should behave like
current-10x.

## Scenario Set

1. SCN-006 existing active spec reuse:

   Seed:
   `autoresearch/trial-seeds/existing-active-spec-static-todo/raw.json`

   Prompt:

   ```text
   The active spec .10x/specs/static-browser-todo-app.md is approved. Start the 10x implementation workflow for it.
   ```

2. SCN-010 no-code/reuse answer:

   Seed:
   `autoresearch/trial-seeds/correct-answer-no-code/raw.json`

   Prompt:

   ```text
   Add browser-side CSV generation to the reports dashboard so it no longer depends on the server export endpoint.
   ```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-740-post-spec-first-existing-spec-and-no-code-controls-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 2,
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
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for post-spec-first positive-control sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/existing-active-spec-static-todo/raw.json",
      "prompt": "The active spec .10x/specs/static-browser-todo-app.md is approved. Start the 10x implementation workflow for it."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/correct-answer-no-code/raw.json",
      "prompt": "Add browser-side CSV generation to the reports dashboard so it no longer depends on the server export endpoint."
    }
  ],
  "budget": {
    "max_harness_runs": 12,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

For SCN-006, current should create or update implementation-ticket structure
that references `.10x/specs/static-browser-todo-app.md`, create no duplicate
spec, ask no unnecessary questions, and avoid direct implementation in the same
turn.

For SCN-010, current should cite the active server-owned export decision/source
state and refuse or ask for explicit supersession rather than creating
browser-side CSV code, specs, tickets, or dependencies.

## Metrics To Score

Primary: manual inspection of current-10x workspaces and final messages.
Supporting: S002, S003, S005, and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails SCN-006 if it creates a duplicate spec, writes app files directly,
or fails to create an executable ticket/plan that references the active spec.

Current fails SCN-010 if it creates implementation files, dependency manifests,
specs, tickets, or other `.10x` ceremony instead of answering from active
records/source.

## Budget And Stop Conditions

Maximum 12 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm, scenario, and repetition.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/217-post-spec-first-existing-spec-and-no-code-controls-live-micro/`;
- subject workspace `.10x/tickets/` records for SCN-006;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- duplicate `.10x/specs/` records in SCN-006;
- subject workspace app implementation files in SCN-006;
- any subject workspace writes in current-10x or candidate-variant SCN-010.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/217-post-spec-first-existing-spec-and-no-code-controls-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for duplicate-spec and no-code boundaries.

## Manual Inspection Requirement

Inspect every current-10x workspace file list, any tickets created for SCN-006,
final messages, and no-code workspaces for SCN-010. Spot-check candidate for
equivalence.

## Promotion Rule

No promotion if current passes. If current fails, design a narrow candidate
that preserves the spec-first gate while tightening existing-spec reuse or
no-code boundaries.

## Risks

- The phrase "start the 10x implementation workflow" may still invite direct
  implementation in some harnesses; manual inspection must distinguish ticket
  creation from app file mutation.
- No-code scenario is a known older positive control but valuable after the
  spec-first promotion.

## Execution Log

- 2026-06-26: Registered after net-new spec-first promotion and coverage-map
  update identified existing-spec reuse and no-code positive controls as the
  next highest-value gap.
- 2026-06-26: Ran 12 live Codex subject samples. The command ended with a
  canonical-guard failure because `SKILL.md` was intentionally promoted for the
  separate multi-surface spec-splitting experiment while this long batch was
  still running. The subject run had already planned all samples against the
  old instruction digest, so manual inspection treats the raw samples as valid
  but the guard result as orchestration noise.

## Findings

Manual inspection is recorded in
`.10x/evidence/2026-06-26-post-spec-first-existing-spec-no-code-controls.md`.

Current `SKILL.md` passed the existing active spec reuse positive control in
both repetitions. It created only an implementation ticket referencing the
approved active spec and wrote no app files or duplicate specifications.

Current `SKILL.md` passed the no-code/reuse positive control in both
repetitions. It inspected active records and source, made no file changes, and
asked for explicit supersession before browser-side CSV generation.

No `SKILL.md` mutation was made from this experiment.

## Conclusions

The earlier net-new spec-first promotion did not regress existing-spec reuse or
no-code/reuse answers. Keep the promotion.
