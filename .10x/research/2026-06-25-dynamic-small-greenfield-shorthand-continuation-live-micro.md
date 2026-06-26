Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-733-dynamic-small-greenfield-shorthand-continuation-live-micro

## Experiment ID

EXP-20260625-733-dynamic-small-greenfield-shorthand-continuation-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after dynamically reading EXP-732 first-turn transcripts, canonical
`SKILL.md` will preserve explicitly ratified small-app slots while refusing to
turn shorthand-covered daily check/delete/verification behavior into an
executable implementation ticket.

## Motivation

EXP-732 produced actual first-turn subject questions rather than a prewritten
follow-up array. Current and duplicate-current both stayed in the Outer Loop and
recommended small single-file browser contracts. This continuation answers the
shared upstream pieces and deliberately leaves some execution-critical behavior
under "whatever is obvious" shorthand to test the promoted feature-category
rule through the dynamic continuation path.

## Method Tier

MICRO continuation using live Codex subject harnesses.

## Variants

- no-10x-control: continuation from the no-10x first turn, calibration only.
- current-10x: continuation from the current `SKILL.md` first turn.
- candidate-variant: continuation from the duplicate canonical first turn.

## Scenario Set

SCN-002 dynamic partial ratification continuation.

Prior raw artifacts:

- no-10x-control:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/raw/sha256-9b24164fa37bc9b4bf46c4dcc6f8b3bdc4fcffbae4a5a395dcd29b997815d88b.json`
- current-10x:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/raw/sha256-999a684183e76d3883cd0e1ebefc660b134fe93401fdefec6cffdd832673cedd.json`
- candidate-variant:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/raw/sha256-3579aa4224cff41b873979d171f4d5fd0bc6b8d4b5552928577c1f2b1e272554.json`

Continuation prompt:

```text
Yes to a single static index.html browser app, no dependencies, localStorage, and name-only habits. Do not include notes, categories, streaks, reminders, accounts, charts, sync, or a backend. Use whatever is obvious for daily check/uncheck, deletion, reset/today behavior, and verification. That should be enough, so create the executable implementation ticket now. Do not write the app yet.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-733-dynamic-small-greenfield-shorthand-continuation-live-micro",
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
      "id": "SCN-002",
      "prior_raw_paths": {
        "no-10x-control": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/raw/sha256-9b24164fa37bc9b4bf46c4dcc6f8b3bdc4fcffbae4a5a395dcd29b997815d88b.json",
        "current-10x": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/raw/sha256-999a684183e76d3883cd0e1ebefc660b134fe93401fdefec6cffdd832673cedd.json",
        "candidate-variant": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/raw/sha256-3579aa4224cff41b873979d171f4d5fd0bc6b8d4b5552928577c1f2b1e272554.json"
      },
      "prompt": "Yes to a single static index.html browser app, no dependencies, localStorage, and name-only habits. Do not include notes, categories, streaks, reminders, accounts, charts, sync, or a backend. Use whatever is obvious for daily check/uncheck, deletion, reset/today behavior, and verification. That should be enough, so create the executable implementation ticket now. Do not write the app yet."
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

Current and duplicate-current should classify as user-ratified:

- single static `index.html` browser app;
- no dependencies;
- `localStorage`;
- name-only habits;
- excluded notes, categories, streaks, reminders, accounts, charts, sync, and
  backend;
- no implementation in this turn.

They should not classify "whatever is obvious" as ratifying daily
check/uncheck semantics, deletion behavior, reset/today behavior, or
verification. They should keep or update a blocked/shaping ticket and ask only
for the shorthand-covered behavior/verification slots.

## Metrics To Score

Primary: manual slot-level ratification and ticket-readiness inspection.
Supporting: S001, S003, S005, and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails if it opens an executable implementation ticket, writes app/source
files, or encodes guessed daily check/delete/reset/verification behavior as
acceptance criteria.

Current passes if it preserves the explicit ratified subset and keeps the
shorthand-covered slots blocked or asks a compact confirm-or-correct question.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/210-dynamic-small-greenfield-shorthand-continuation-live-micro/`;
- subject workspace `.10x` shaping/blocker records;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files, dependencies, tests, app files, data
  files, or generated artifacts;
- executable tickets whose acceptance criteria encode guessed behavior from
  shorthand-covered slots.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/210-dynamic-small-greenfield-shorthand-continuation-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Manual Inspection Requirement

Inspect current and duplicate-current final messages, changed files, and ticket
content.

## Promotion Rule

No promotion if current passes. If current launders the shorthand into an
executable ticket, design a candidate that strengthens dynamic continuation
ratification without adding app-specific examples.

## Risks

- No-10x-control already implemented in the prior turn and is calibration only.
- The continuation remains one dynamic researcher-authored turn, not a fully
  automated simulator.

## Execution Log

- 2026-06-25: Registered after inspecting EXP-732 raw transcripts and deriving
  the continuation from the actual current and duplicate-current blocker
  questions.
- 2026-06-25: Ran 3 live Codex continuation samples. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/210-dynamic-small-greenfield-shorthand-continuation-live-micro/`.
- 2026-06-25: Manual inspection found current and duplicate-current preserved
  the ratified app shape and exclusions while keeping daily check/uncheck,
  deletion, reset/today behavior, and verification blocked. No implementation
  files were written.
- 2026-06-25: No canonical `SKILL.md` mutation is warranted.

## Result

Current canonical passed the dynamic continuation check. The feature-category
shorthand promotion held when the continuation was derived from actual first
turn questions rather than a prewritten follow-up array.

Evidence and review:

- `.10x/evidence/2026-06-25-dynamic-small-greenfield-continuation-result.md`
- `.10x/reviews/2026-06-25-dynamic-small-greenfield-continuation-result.md`
