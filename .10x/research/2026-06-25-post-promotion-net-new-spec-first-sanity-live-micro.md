Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-739-post-promotion-net-new-spec-first-sanity-live-micro

## Experiment ID

EXP-20260625-739-post-promotion-net-new-spec-first-sanity-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: canonical `SKILL.md` after promoting the net-new spec-first gate
matches the successful candidate behavior: ratified greenfield app behavior
creates an active spec and ticket structure without implementation, while exact
mechanical edits remain lightweight.

## Motivation

`candidate-net-new-spec-first-gate-v1` passed the primary continuation and exact
edit controls. This post-promotion sanity run checks that the same behavior
transfers into canonical `SKILL.md`.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md` after local promotion.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay.

## Control

No-10x-control is calibration only. Candidate-variant is a no-op duplicate
sanity arm.

## Scenario Set

1. SCN-001 ratified greenfield continuation from the current-10x to-do shaping
   checkpoint.
2. SCN-010 exact one-line source edit.
3. SCN-010 corrected exact formatting edit.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-739-post-promotion-net-new-spec-first-sanity-live-micro",
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
      "instruction_source": "SKILL.md after net-new spec-first promotion",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for post-promotion net-new spec-first sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_paths": {
        "no-10x-control": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-570c079a1a09b893acddf490fe69aea584550fc7c528ba9e4994838917ddcb9d.json",
        "current-10x": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-55b8bac8e47596958c68dc5ceedc082799bbc590c7861460d0fdb718d141dfcc.json",
        "candidate-variant": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-55b8bac8e47596958c68dc5ceedc082799bbc590c7861460d0fdb718d141dfcc.json"
      },
      "prompt": "Confirmed. Use a dependency-free static browser app with index.html, styles.css, and app.js. Behavior: add a todo with trimmed non-empty text; show todos in creation order; mark a todo complete or active; edit todo text; delete one todo; filter all, active, and completed; show an empty-state message when the selected filter has no todos; clear completed only after an explicit confirmation; persist todos and the selected filter in localStorage across refresh. Exclude accounts, backend, sync, dates, priorities, drag/drop, notifications, routing, build tooling, external dependencies, and automated tests. Verification path: manual browser check for add, edit, complete/uncomplete, filter changes, delete, clear-completed cancel and confirm, empty states, and refresh persistence. Proceed with the 10x workflow."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/exact-one-line-code-edit/raw.json",
      "prompt": "In statusLabel.js, change the label returned for \"archived\" from \"Old\" to \"Archived\". Do only that."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/exact-formatting-edit/raw.json",
      "prompt": "In styles.css, change only the .button padding from 4px 8px to 6px 10px. Do only that."
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

Current-10x should create an active spec plus ticket structure and no app files
on SCN-001. It should change only the target file on both SCN-010 controls.

## Metrics To Score

Primary: manual inspection. Supporting: S001, S005, and S007.

## Quality Floors

Current fails if it implements the greenfield app directly, omits the active
spec, or creates `.10x` ceremony for exact edits.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/216-post-promotion-net-new-spec-first-sanity-live-micro/`;
- subject workspace `.10x/specs/` and `.10x/tickets/` records for SCN-001;
- subject workspace exact target-file edits for SCN-010;
- this research record execution log updates;
- evidence/review records after inspection.

Disallowed writes:

- `SKILL.md` or `autoresearch/program.md` during the run;
- subject workspace implementation files for current-10x or candidate-variant
  in SCN-001;
- `.10x` records or unrelated file writes for current-10x or
  candidate-variant in SCN-010.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/216-post-promotion-net-new-spec-first-sanity-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Manual Inspection Requirement

Inspect current-10x primary workspace, spec/ticket contents, exact edit file
outputs, final messages, and canonical guard.

## Promotion Rule

If current passes, keep the promoted canonical text. If current fails, revert or
revise the promotion before committing.

## Risks

This is a local post-promotion run while `SKILL.md` is uncommitted, so
`--require-clean-canonical` is intentionally omitted. The canonical guard still
checks that `SKILL.md` and `autoresearch/program.md` do not change during the
run.

## Execution Log

- 2026-06-25: Registered after applying the candidate text to local
  `SKILL.md`.
- 2026-06-25: Ran 9 live Codex subject samples without
  `--require-clean-canonical` because `SKILL.md` was intentionally dirty during
  local promotion. Canonical guard confirmed `SKILL.md` and
  `autoresearch/program.md` did not change during the run.

## Findings

Artifacts:

- Raw run directory:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/216-post-promotion-net-new-spec-first-sanity-live-micro/`
- Report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/216-post-promotion-net-new-spec-first-sanity-live-micro/report.md`
- Combined evidence:
  `.10x/evidence/2026-06-25-net-new-spec-first-gate-result.md`
- Combined review:
  `.10x/reviews/2026-06-25-net-new-spec-first-gate-result.md`

Current-10x passed the primary after promotion:

- Created `.10x/specs/static-browser-todo-app.md`.
- Updated parent plan `.10x/tickets/2026-06-25-create-todo-app.md`.
- Created child implementation ticket
  `.10x/tickets/2026-06-25-implement-static-todo-app.md`.
- Created no `index.html`, `styles.css`, or `app.js`.

Current-10x passed exact edit controls:

- Exact one-line source edit changed only `statusLabel.js`.
- Corrected exact formatting edit changed only `styles.css`.

Trust Level 1 score summary:

| Arm | Scenario | Score | Value | Floor failures |
| --- | --- | --- | ---: | ---: |
| current-10x | SCN-001 | S001 | 85 | 0 |
| candidate-variant | SCN-001 | S001 | 85 | 0 |
| no-10x-control | SCN-001 | S001 | 30 | 1 |
| current-10x | SCN-010 | S005 average | 85 | 0 |
| candidate-variant | SCN-010 | S005 average | 95 | 0 |

## Conclusions

The promoted canonical text transferred the candidate behavior into `SKILL.md`.
Keep the promotion.
