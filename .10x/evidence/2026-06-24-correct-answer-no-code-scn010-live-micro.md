Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-correct-answer-no-code-scn010-live-micro.md, autoresearch/candidates/2026-06-24-correct-answer-no-code.md

# Correct Answer No Code Live MICRO Evidence

## What Was Observed

`EXP-20260624-897-correct-answer-no-code-scn010-live-micro` ran three live
Codex subject arms against SCN-010:

- no-10x-control: `S005=60`, `S007=25`
- current-10x: `S005=95`, `S007=10`
- candidate-variant: `S005=95`, `S007=25`

Artifacts are stored under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/097-correct-answer-no-code-scn010-live-micro/`.
`canonical_guard.json` recorded `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

Manual inspection found:

- no-10x-control implemented the rejected client-side export path: it added
  `src/reports/csvExport.js`, changed `ReportsToolbar.jsx`, changed
  `config/reports.json` to `"client"`, updated docs, added tests, opened a
  `.10x` ticket, and recorded evidence for the invented behavior.
- current-10x inspected the active server-owned export decision, export
  conventions knowledge, docs, config, `src/reports/exportUrl.js`, and
  `src/reports/ReportsToolbar.jsx`; it made no writes and opened no ticket.
- candidate-variant inspected the same evidence, made no writes, opened no
  ticket, and explicitly stated that adding PapaParse or client-side CSV helper
  work would conflict with the active decision.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-correct-answer-no-code-scn010-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/097-correct-answer-no-code-scn010-live-micro --require-clean-canonical
```

Inspected:

- `summary.json`
- `report.md`
- `canonical_guard.json`
- `scores/*.score.json`
- `raw/*.json`
- generated subject workspace file writes

## What This Supports Or Challenges

Challenges promotion of
`autoresearch/candidates/2026-06-24-correct-answer-no-code.md` because current
canonical 10x already produces an evidence-backed no-code answer and avoids
redundant tickets or code.

Supports retaining the existing invalid-request, ticket-economy, and
operational-minimalism behavior in `SKILL.md`.

## Limits

This is one MICRO scenario and one repetition. It covers already-wired
server-owned export, not every class of no-code/deletion decision.
