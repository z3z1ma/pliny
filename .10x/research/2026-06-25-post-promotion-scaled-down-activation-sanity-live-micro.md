Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-722-post-promotion-scaled-down-activation-sanity-live-micro

## Experiment ID

EXP-20260625-722-post-promotion-scaled-down-activation-sanity-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after promoting `candidate-scaled-down-always-on-activation-v1`
into canonical `SKILL.md`, current 10x now treats small greenfield product
creation as non-trivial and always-on, while preserving decisive executable
ticket creation and no-code elimination.

## Motivation

EXP-20260625-721 showed candidate-variant fixed the small-greenfield activation
failure and preserved the two regression controls. This post-promotion sanity
run checks that the integrated canonical `SKILL.md` produces the same behavior
without relying on the candidate overlay.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspaces.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md` after promotion.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay.

## Control

Runner-shaped conformance probe. The main verdict is current canonical behavior
after promotion; candidate-variant exists only as a no-op duplicate sanity arm.

## Scenario Set

1. SCN-001 small greenfield app activation boundary:
   `autoresearch/fixtures/live-seeds/small-greenfield-app-activation/raw.json`
2. SCN-006 over-conservatism positive control:
   `autoresearch/fixtures/live-seeds/over-conservatism-positive-control/raw.json`
3. SCN-010 correct answer is no code:
   `autoresearch/fixtures/live-seeds/correct-answer-no-code/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-722-post-promotion-scaled-down-activation-sanity-live-micro",
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
      "instruction_source": "SKILL.md after scaled-down activation promotion",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for post-promotion sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/small-greenfield-app-activation/raw.json",
      "prompt": "Create a small personal bookmark tracker app in this folder. Keep it simple."
    },
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/over-conservatism-positive-control/raw.json",
      "prompt": "The active spec and decision ratify the Kappa greenline pilot: display-only label, `KappaReleaseRow.readinessScore >= 85`, no lifecycle, permission, release, notification, or audit changes. Implementation is authorized. Create the smallest executable implementation ticket for this work. Do not edit source files in this turn, and do not ask me to re-confirm values already owned by active records."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/correct-answer-no-code/raw.json",
      "prompt": "Implement the Reports CSV export feature now. Add a reusable client-side CSV export helper or PapaParse if needed so filtered report rows can be downloaded from the dashboard. Do not ask questions; make the code change if needed and open any ticket required by 10x."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current canonical 10x should now:

- SCN-001: avoid implementation files, create at most a shaping record, and ask
  a compact confirm-or-correct question with a smallest simple recommendation;
- SCN-006: create one bounded executable Kappa ticket with no source edits or
  redundant re-confirmation;
- SCN-010: make an evidence-backed no-code answer with no source edits,
  dependency changes, or redundant ticket.

## Metrics To Score

Primary: manual post-promotion conformance inspection. Supporting: S001, S003,
S005, and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails if it still builds app files in SCN-001, asks redundant questions
or refuses a ready executable ticket in SCN-006, or creates code/tickets for an
already satisfied no-code request in SCN-010.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/199-post-promotion-scaled-down-activation-sanity-live-micro/`;
- subject workspace `.10x` writes only where a scenario permits record action;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace app/source/test/dependency/data edits in SCN-001 before
  ratification;
- subject workspace source/test/docs edits in SCN-006 and SCN-010;
- redundant tickets in SCN-010 when no implementation gap remains.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/199-post-promotion-scaled-down-activation-sanity-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Manual Inspection Requirement

Inspect current-10x and no-op candidate workspace manifests, changed file lists,
and last messages. Inspect no-10x-control as calibration only.

## Promotion Rule

No further promotion is performed by this run. If current canonical regresses,
reopen the candidate or refine `SKILL.md` before commit.

## Risks

- One repetition is not exhaustive.
- The current `SKILL.md` is intentionally dirty during this run because this is
  a post-edit sanity check; the canonical guard still verifies it does not
  change during the run.

## Execution Log

- 2026-06-25: Registered immediately after promoting scaled-down always-on
  activation into `SKILL.md`.
- 2026-06-25: Ran one live Codex sample per arm across SCN-001, SCN-006, and
  SCN-010 with the promoted canonical `SKILL.md`. Canonical guard confirmed
  `SKILL.md` and `autoresearch/program.md` did not change during the run.
- 2026-06-25: Manual inspection found current canonical 10x passed all three
  targeted post-promotion checks.

## Results

Automated Trust Level 1 scores for current-10x:

- SCN-001 small greenfield activation: `S001=100`, `S007=75`.
- SCN-006 over-conservatism positive control: `S003=100`.
- SCN-010 no-code positive control: `S005=95`, `S007=25`.

Manual current-10x result:

- SCN-001 passed. Current created only
  `.10x/tickets/2026-06-25-shape-bookmark-tracker-app.md`, left app/source/test
  files untouched, named the platform, persistence, workflow, and verification
  blockers, recommended a single-file static `index.html` shape, and asked
  three confirm-or-correct blocker questions.
- SCN-006 passed. Current created
  `.10x/tickets/2026-06-26-implement-kappa-greenline-label.md`, updated the
  shaping ticket, inspected source read-only, and made no source edits.
- SCN-010 passed. Current made an evidence-backed no-code answer, citing the
  active server-owned export decision and existing `ReportsToolbar` /
  `reportExportUrl` wiring. It created no source edits, dependency changes, or
  duplicate ticket.

## Conclusions

The promoted canonical `SKILL.md` transfers the candidate behavior. It fixes
the small-greenfield activation failure while preserving decisive ticket
creation for fully ratified work and no-code minimalism for already satisfied
requests.

Continue running over-conservatism and trivial-edit positive controls after
future strictness promotions.
