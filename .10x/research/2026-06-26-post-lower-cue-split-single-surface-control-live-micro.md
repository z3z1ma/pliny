Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-745-post-lower-cue-split-single-surface-control-live-micro

## Experiment ID

EXP-20260626-745-post-lower-cue-split-single-surface-control-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after promoting lower-cue multi-surface splitting, canonical
`SKILL.md` should still keep a genuinely cohesive small static to-do app in one
focused specification and one bounded child ticket, rather than splitting
mechanically.

## Motivation

The lower-cue multi-surface promotion deliberately strengthens anti-god-spec
behavior. Its main regression risk is over-splitting cohesive single-surface
work. This positive control tests the explicit single-cohesive-surface
exception immediately after promotion.

## Method Tier

MICRO using live Codex subject continuations from
`EXP-20260625-735-generic-named-app-activation-live-micro`.

## Variants

- no-10x-control: minimal Codex instruction continued from the prior no-10x
  to-do raw artifact for calibration only.
- current-10x: canonical `SKILL.md`, continued from the prior current-10x
  to-do shaping checkpoint.
- candidate-variant: canonical `SKILL.md` plus no-op duplicate sanity overlay,
  continued from the prior candidate to-do shaping checkpoint.

## Scenario Set

Single cohesive continuation:

```text
Confirmed. Use a dependency-free static browser app with index.html, styles.css, and app.js. Behavior: add a todo with trimmed non-empty text; show todos in creation order; mark a todo complete or active; delete one todo; filter all, active, and completed; show an empty-state message when the selected filter has no todos; persist todos and the selected filter in localStorage across refresh. Exclude accounts, backend, sync, edit, projects, import/export, activity log, dates, priorities, drag/drop, notifications, routing, build tooling, external dependencies, and automated tests. Verification path: manual browser check for add, complete/uncomplete, filter changes, delete, empty states, and refresh persistence. Proceed with the 10x workflow.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-745-post-lower-cue-split-single-surface-control-live-micro",
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
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for single-surface anti-over-splitting sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_paths": {
        "no-10x-control": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-570c079a1a09b893acddf490fe69aea584550fc7c528ba9e4994838917ddcb9d.json",
        "current-10x": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-55b8bac8e47596958c68dc5ceedc082799bbc590c7861460d0fdb718d141dfcc.json",
        "candidate-variant": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/raw/sha256-004f2bedd5fac1e15e6cc1c327077f41636b2adfdbde342846dbaabbcd3c266e.json"
      },
      "prompt": "Confirmed. Use a dependency-free static browser app with index.html, styles.css, and app.js. Behavior: add a todo with trimmed non-empty text; show todos in creation order; mark a todo complete or active; delete one todo; filter all, active, and completed; show an empty-state message when the selected filter has no todos; persist todos and the selected filter in localStorage across refresh. Exclude accounts, backend, sync, edit, projects, import/export, activity log, dates, priorities, drag/drop, notifications, routing, build tooling, external dependencies, and automated tests. Verification path: manual browser check for add, complete/uncomplete, filter changes, delete, empty states, and refresh persistence. Proceed with the 10x workflow."
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

Current should create or update one active specification for the cohesive static
to-do behavior, update or create the parent plan, create one bounded child
ticket, and stop without implementation files.

## Metrics To Score

Primary: manual inspection of spec count, ticket count/scope, file writes, and
final messages.

## Quality Floors

Manual inspection is authoritative.

Current fails if it creates multiple specs for this cohesive surface, creates
implementation files, asks for already-ratified choices, or creates a broad
multi-surface plan unrelated to the simple behavior.

Current passes if it creates one focused active spec, one bounded child ticket
under the parent, no app files, and no unresolved blockers.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/223-post-lower-cue-split-single-surface-control-live-micro/`;
- subject workspace `.10x/specs/` and `.10x/tickets/` records for current-10x
  and candidate-variant;
- this research record execution log updates;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files for current-10x or candidate-variant.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/223-post-lower-cue-split-single-surface-control-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Manual Inspection Requirement

Inspect current-10x and candidate-variant workspace file lists, spec records,
ticket records, final messages, and raw metadata.

## Promotion Rule

No promotion if current passes. If current fails by over-splitting, tighten the
new lower-cue split rule before commit or create a corrective candidate.

## Risks

- One repetition may miss stochastic over-splitting. If this passes, repeat a
  broader anti-over-splitting batch later across several cohesive features.

## Execution Log

- 2026-06-26: Registered immediately after promoting
  `candidate-lower-cue-multi-surface-spec-splitting-v1`.
- 2026-06-26: Ran live with `--require-clean-canonical`; artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/223-post-lower-cue-split-single-surface-control-live-micro/`.
- 2026-06-26: Manual inspection found a narrow failure. Current `SKILL.md`
  avoided implementation and created one cohesive active specification, but
  over-decomposed one cohesive app into shell, interaction, and verification
  child tickets. The no-op candidate arm stochastically produced the preferred
  one-spec, one-parent, one-executable-child shape. Registered
  `EXP-20260626-746-ticket-boundary-corrective-single-surface-live-micro` to
  test a targeted child-ticket-boundary mutation.

## Findings

Current passed the anti-god-spec part of the control but failed the
anti-over-ticketing part. The promoted lower-cue specification language was not
causing mechanical specification splitting, but adjacent ticket language still
allowed mechanical child-ticket splitting by activity phase.

## Conclusions

The correct mutation is not to weaken focused specification splitting. The
needed fix is a narrower ticket-boundary rule: child tickets should split by
independent deliverable outcomes, distinct governing surfaces, real handoff
dependencies, or distinct verification authority, not by setup/interaction/
verification phases inside one cohesive implementation.
