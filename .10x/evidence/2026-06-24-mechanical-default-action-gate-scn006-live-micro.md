Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-mechanical-default-action-gate-scn006-live-micro.md, autoresearch/candidates/2026-06-24-mechanical-default-action-gate.md

# Mechanical Default Action Gate Live MICRO Evidence

## What Was Observed

`EXP-20260624-886-mechanical-default-action-gate-scn006-live-micro` ran three
live Codex subject arms against SCN-006:

- no-10x-control: `S003=100`
- current-10x: `S003=85`
- candidate-variant: `S003=100`

Artifacts are stored under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/086-mechanical-default-action-gate-scn006-live-micro/`.
`canonical_guard.json` recorded `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

Manual inspection found:

- current-10x and candidate-variant both created one executable child ticket,
  made no implementation edits, and asked no naming or placement questions.
- candidate-variant created
  `.10x/tickets/2026-06-24-enterprise-billing-csv-export.md` with active
  spec/decision dependencies, explicit exclusions, evidence expectations, and a
  progress note stating filename/title were mechanical defaults.
- current-10x created
  `.10x/tickets/2026-06-24-enterprise-billing-exceptions-csv-export.md` with
  correct active spec/decision dependencies and a valid execution scope, but did
  not explicitly name mechanical-default reasoning.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-mechanical-default-action-gate-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/086-mechanical-default-action-gate-scn006-live-micro --require-clean-canonical
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

Supports keeping
`autoresearch/candidates/2026-06-24-mechanical-default-action-gate.md` for a
follow-up MICRO. It does not yet support canonical promotion because the prompt
explicitly identified ticket filename/title as mechanical details.

## Limits

This is one MICRO scenario and one repetition. Trust Level 1 scoring rewarded
ticket-shape signals and does not prove the mechanical-default instruction
caused the improvement. The result is confounded by the prompt's explicit
mechanical-default language and by a no-10x control that also scored 100 on
S003.
