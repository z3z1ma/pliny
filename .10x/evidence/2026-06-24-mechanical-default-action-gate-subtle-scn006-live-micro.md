Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-mechanical-default-action-gate-subtle-scn006-live-micro.md, autoresearch/candidates/2026-06-24-mechanical-default-action-gate.md

# Mechanical Default Action Gate Subtle Live MICRO Evidence

## What Was Observed

`EXP-20260624-887-mechanical-default-action-gate-subtle-scn006-live-micro` ran
three live Codex subject arms against SCN-006:

- no-10x-control: `S003=100`
- current-10x: `S003=85`
- candidate-variant: `S003=65`

Artifacts are stored under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/087-mechanical-default-action-gate-subtle-scn006-live-micro/`.
`canonical_guard.json` recorded `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

Manual inspection found:

- current-10x created one executable child ticket with active record references,
  explicit exclusions, acceptance criteria, verification expectations, source
  context, assumption provenance, and `Blockers: None`.
- candidate-variant created one executable child ticket and named the
  filename/title choice as a mechanical default, but produced a thinner ticket
  than current on source context and provenance.
- no-10x-control created a broad source-only ticket because `.10x` records were
  intentionally removed for the control arm.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-mechanical-default-action-gate-subtle-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/087-mechanical-default-action-gate-subtle-scn006-live-micro --require-clean-canonical
```

Inspected:

- `summary.json`
- `report.md`
- `canonical_guard.json`
- `scores/*.score.json`
- `raw/*.json`
- generated subject workspace tickets
- subject workspace file lists

## What This Supports Or Challenges

Supports discarding
`autoresearch/candidates/2026-06-24-mechanical-default-action-gate.md`. The
candidate regressed below the S003 floor and did not show enough distinct
mechanical-default benefit to justify canonical instruction bulk.

## Limits

This is one MICRO scenario and one repetition. The no-10x control's high score
shows this seed can reward generic ticket shape, so manual inspection is
necessary. The result does not prove mechanical-default guidance is never
useful; it shows this candidate wording is not worth promoting.
