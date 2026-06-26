Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-746-ticket-boundary-corrective-single-surface-live-micro

## Experiment ID

EXP-20260626-746-ticket-boundary-corrective-single-surface-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: the corrected child-ticket boundary language should keep a
genuinely cohesive small static to-do app in one active specification, one
parent plan, and one executable child ticket, rather than splitting shell,
interaction, and verification into separate child tickets.

## Motivation

`EXP-20260626-745-post-lower-cue-split-single-surface-control-live-micro`
showed that canonical `SKILL.md` avoided a god spec and did not implement app
files, but still over-decomposed one cohesive app into three executable child
tickets. The corrective mutation keeps anti-god-spec pressure while requiring
ticket splits to use the same independence test as specification splits.

## Method Tier

MICRO using live Codex subject continuations from
`EXP-20260625-735-generic-named-app-activation-live-micro`.

## Variants

- no-10x-control: minimal Codex instruction continued from the prior no-10x
  to-do raw artifact for calibration only.
- current-10x: patched canonical `SKILL.md`.
- candidate-variant: patched canonical `SKILL.md` plus no-op duplicate sanity
  overlay.

## Scenario Set

Single cohesive continuation:

```text
Confirmed. Use a dependency-free static browser app with index.html, styles.css, and app.js. Behavior: add a todo with trimmed non-empty text; show todos in creation order; mark a todo complete or active; delete one todo; filter all, active, and completed; show an empty-state message when the selected filter has no todos; persist todos and the selected filter in localStorage across refresh. Exclude accounts, backend, sync, edit, projects, import/export, activity log, dates, priorities, drag/drop, notifications, routing, build tooling, external dependencies, and automated tests. Verification path: manual browser check for add, complete/uncomplete, filter changes, delete, empty states, and refresh persistence. Proceed with the 10x workflow.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-746-ticket-boundary-corrective-single-surface-live-micro",
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
      "instruction_source": "patched SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "patched SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for single-surface corrective sanity comparison."
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

The corrected current arm should create one active specification, one parent
plan, one executable child ticket, no implementation files, and no separate
shell or verification child ticket.

## Metrics To Score

Manual inspection of workspace file list, spec count, ticket count/scope,
final message, and raw metadata.

## Quality Floors

Manual inspection is authoritative.

Pass:

- one focused active specification;
- one parent plan;
- one executable child ticket under the parent;
- no app implementation files;
- no setup-only or verification-only child ticket for this cohesive surface;
- no unresolved blockers.

Fail:

- multiple specs for this cohesive surface;
- separate shell/setup, interaction, or verification child tickets;
- implementation files;
- unresolved blockers or questions for already-ratified choices.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/224-ticket-boundary-corrective-single-surface-live-micro/`;
- subject workspace `.10x/specs/`, `.10x/tickets/`, and `.10x/evidence/`
  records;
- this research record execution log updates;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md` during the run;
- `autoresearch/program.md`;
- subject workspace implementation files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/224-ticket-boundary-corrective-single-surface-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Manual Inspection Requirement

Inspect workspace file list, spec records, ticket records, final message, and
raw metadata.

## Promotion Rule

Promote and commit the corrective mutation only if manual inspection confirms
the child-ticket boundary improves without implementation leakage.

## Risks

- One repetition may miss stochastic over-splitting. If this passes, repeat a
  broader anti-over-splitting batch later.

## Execution Log

- 2026-06-26: Registered after `EXP-20260626-745` exposed current-arm
  ticket over-fragmentation.
- 2026-06-26: Ran live with canonical guard enabled; artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/224-ticket-boundary-corrective-single-surface-live-micro/`.
- 2026-06-26: Manual inspection found current `SKILL.md` passed the corrective
  target. It created one active specification, updated the existing parent
  plan to own exactly one executable child ticket, and created one executable
  child ticket that owns implementation plus manual verification evidence. No
  current-arm implementation files were created.

## Findings

The corrective mutation changed the current-arm behavior from three child
tickets in `EXP-20260626-745` to one executable child ticket in this run. The
single child ticket included the app files, behavior, exclusions, acceptance
criteria, and manual evidence expectation. The parent ticket coordinated that
single child instead of manufacturing shell and verification children.

The no-10x control implemented app files directly. The candidate-variant arm
also avoided implementation and over-ticketing, but used a shaping ticket plus
one executable ticket rather than an explicit parent plan; promotion is based
on the current-arm corrective pass.

## Conclusions

Promote the child-ticket-boundary mutation. It preserves focused
anti-god-spec pressure while preventing activity-phase child-ticket churn for
one cohesive implementation.
