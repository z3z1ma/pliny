Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-737-net-new-spec-first-gate-candidate-batch-live-micro

## Experiment ID

EXP-20260625-737-net-new-spec-first-gate-candidate-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-net-new-spec-first-gate-v1` will prevent ratified
greenfield app behavior from collapsing directly into one implementation ticket
or direct implementation. It should create an active governing spec first,
derive executable ticket structure from that spec, and avoid implementation in
the same turn. It should not add spec/ticket ceremony to exact mechanical edit
controls.

## Motivation

`EXP-20260625-736-greenfield-spec-before-ticket-continuation-live-micro`
reproduced the user's reported failure in canonical current: after a clarified
to-do app contract, current implemented directly with no spec. A no-op
candidate created a spec but still implemented in the same turn. This candidate
tests a narrow gate for net-new/important behavior without weakening exact-edit
minimalism.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-25-net-new-spec-first-gate.md`.

## Control

No-10x-control is calibration only. The primary comparison is current-10x
versus candidate-variant.

## Scenario Set

1. SCN-001 ratified greenfield continuation from the current-10x to-do shaping
   checkpoint. Current and candidate use the same prior current raw artifact
   for a fair transition comparison.
2. SCN-010 exact one-line source edit.
3. SCN-010 exact formatting edit.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-737-net-new-spec-first-gate-candidate-batch-live-micro",
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
      "prompt": "In styles.css, change only the .status-pill padding from 4px 8px to 6px 10px. Do only that."
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

Candidate should pass the primary by creating an active spec and executable
ticket structure without `index.html`, `styles.css`, or `app.js`. Current is
expected to reproduce the EXP-736 failure or a close variant. Candidate should
preserve exact edit minimalism in both SCN-010 controls.

## Metrics To Score

Primary: manual inspection of candidate and current workspace file outputs and
record contents. Supporting: S001, S002, S003, S005, S006, and S007 where the
Trust Level 1 scorer can approximate them.

## Quality Floors

Manual inspection is authoritative.

Candidate fails if it implements the greenfield app directly, omits the active
spec, uses one all-purpose executable ticket as the behavior contract, or
creates `.10x` records for exact mechanical edits.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/214-net-new-spec-first-gate-candidate-batch-live-micro/`;
- subject workspace `.10x/specs/` and `.10x/tickets/` records for SCN-001;
- subject workspace exact target-file edits for SCN-010;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files for current-10x or candidate-variant
  in SCN-001;
- `.10x` records or unrelated file writes for candidate-variant in SCN-010;
- closure evidence, done tickets, or retrospective records in SCN-001.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/214-net-new-spec-first-gate-candidate-batch-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for spec-before-ticket sequencing and exact-edit
minimalism.

## Manual Inspection Requirement

Inspect every candidate workspace, file list, spec/ticket content for SCN-001,
and exact edit diffs for SCN-010. Inspect current primary for comparison.

## Promotion Rule

Promote only if candidate passes the primary and both exact-edit regressions.
If it fails primary by implementing in the same turn, revise the candidate.

## Risks

- The current arm may behave differently from EXP-736 due stochasticity; manual
  verdict should compare candidate behavior to the required invariant, not only
  current delta.
- The automated scorer treats SCN-001 implementation as unauthorized even when
  the continuation ratifies behavior; manual inspection remains decisive.

## Execution Log

- 2026-06-25: Registered after EXP-736 reproduced direct implementation after
  ratification.
- 2026-06-25: Ran 9 live Codex subject samples with
  `candidate-net-new-spec-first-gate-v1`.

## Findings

Artifacts:

- Raw run directory:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/214-net-new-spec-first-gate-candidate-batch-live-micro/`
- Report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/214-net-new-spec-first-gate-candidate-batch-live-micro/report.md`
- Combined evidence:
  `.10x/evidence/2026-06-25-net-new-spec-first-gate-result.md`
- Combined review:
  `.10x/reviews/2026-06-25-net-new-spec-first-gate-result.md`

Primary result:

- Current-10x reproduced the failure again: no spec, direct implementation,
  evidence/review, and app files.
- Candidate-variant passed: created `.10x/specs/static-browser-todo-app.md`,
  updated parent plan `.10x/tickets/2026-06-25-create-todo-app.md`, created
  child ticket `.10x/tickets/2026-06-25-implement-static-browser-todo-app.md`,
  and created no app files.

Regression results:

- Candidate exact one-line source edit changed only `statusLabel.js`.
- The original formatting regression prompt was confounded because the seed
  fixture contained `.button`, not `.status-pill`; candidate correctly refused
  to edit an absent selector.

## Conclusions

`candidate-net-new-spec-first-gate-v1` fixed the primary failure and preserved
the exact one-line edit. A corrected formatting regression is required before
promotion.
