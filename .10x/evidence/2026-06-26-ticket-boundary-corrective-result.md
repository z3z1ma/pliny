Status: recorded
Created: 2026-06-26
Updated: 2026-06-26
Relates-To: .10x/research/2026-06-26-post-lower-cue-split-single-surface-control-live-micro.md, .10x/research/2026-06-26-ticket-boundary-corrective-single-surface-live-micro.md, .10x/reviews/2026-06-26-promote-ticket-boundary-corrective.md

# Ticket Boundary Corrective Result

## What Was Observed

`EXP-20260626-745-post-lower-cue-split-single-surface-control-live-micro`
ran with clean canonical instructions and produced three live samples under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/223-post-lower-cue-split-single-surface-control-live-micro/`

Manual inspection found:

- `no-10x-control` implemented app files directly: `index.html`, `styles.css`,
  and `app.js`.
- `current-10x` created one active specification and no app files, but split
  one cohesive static to-do app into three child tickets:
  `.10x/tickets/2026-06-25-build-static-todo-shell.md`,
  `.10x/tickets/2026-06-25-implement-todo-interactions.md`, and
  `.10x/tickets/2026-06-25-verify-static-todo-app.md`.
- `candidate-variant` created one active specification, one parent plan, one
  executable child ticket, one evidence record, and no app files.
- The canonical guard for the run reported `unchanged_during_run: true` and
  `require_clean_canonical: true`.

`EXP-20260626-746-ticket-boundary-corrective-single-surface-live-micro` then
ran the same continuation after patching `SKILL.md` to make child-ticket
boundaries use the same independence test as specification boundaries.
Artifacts are under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/224-ticket-boundary-corrective-single-surface-live-micro/`

Manual inspection found:

- `no-10x-control` again implemented app files directly.
- `current-10x` created one active specification:
  `.10x/specs/static-browser-todo-app.md`.
- `current-10x` updated the parent plan:
  `.10x/tickets/2026-06-25-create-todo-app.md`.
- `current-10x` created exactly one executable child ticket:
  `.10x/tickets/2026-06-26-build-static-browser-todo-app.md`.
- The child ticket owns implementation and manual verification evidence for
  the cohesive static app. It did not split shell/setup, interaction, and
  verification into separate tickets.
- The current arm created no implementation files.
- The canonical guard reported `unchanged_during_run: true`; pre-run clean was
  intentionally not required because `SKILL.md` contained the corrective
  mutation under test.

## Procedure

1. Ran `python3 autoresearch/run_once.py` for `EXP-20260626-745` with
   `--require-clean-canonical`.
2. Inspected `report.md`, `canonical_guard.json`, raw JSON final messages,
   workspace file lists, and current-arm records.
3. Patched `SKILL.md` to make child-ticket splitting depend on independent
   deliverable boundaries rather than activity phases.
4. Registered and ran `EXP-20260626-746`.
5. Inspected the same artifact classes for the corrective run.

## What This Supports Or Challenges

This supports promoting the child-ticket-boundary mutation in `SKILL.md`.
It challenges the previous wording that allowed an agent to satisfy spec-first
structure while manufacturing setup, interaction, and verification tickets for
one cohesive implementation.

## Limits

This is one Codex live continuation per arm. It does not prove behavior in
Claude Code, OpenCode, oh-my-pi, or future model versions. The no-op candidate
arm in the first run was stochastic evidence, not causal proof. The corrective
promotion rests on the before/after current-arm comparison plus manual
inspection.
