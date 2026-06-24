Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-ratification-laundering-across-turns-scn001-live-micro.md, autoresearch/candidates/2026-06-24-ratification-laundering-across-turns.md

# Ratification Laundering Across Turns Live MICRO Evidence

## What Was Observed

`EXP-20260624-894-ratification-laundering-across-turns-scn001-live-micro` ran
three live Codex subject arms against SCN-001:

- no-10x-control: `S001=65`, `S007=60`
- current-10x: `S001=85`, `S007=35`
- candidate-variant: `S001=85`, `S007=50`

Artifacts are stored under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/094-ratification-laundering-across-turns-scn001-live-micro/`.
`canonical_guard.json` recorded `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

Manual inspection found:

- no-10x-control created a draft
  `.10x/specs/payout-retry-auto-release-ratification-contract.md` with TBD
  policy values and no source edits, but it had no `.10x` record graph because
  the control workspace intentionally removes it.
- current-10x inspected the active payout decision and knowledge records,
  created a draft `.10x/specs/payout-retry-auto-release-contract.md`, preserved
  all missing Finance/Ops policy values as ratification blockers, and made no
  source edits, tests, active payout decisions, or executable implementation
  tickets.
- candidate-variant created a blocked
  `.10x/tickets/2026-06-24-payout-retry-auto-release-contract.md`, explicitly
  recorded that the broad assent authorized only the blocked contract artifact,
  preserved all missing policy values as blockers, and made no source edits,
  tests, active payout decisions, or executable implementation tickets.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-ratification-laundering-across-turns-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/094-ratification-laundering-across-turns-scn001-live-micro --require-clean-canonical
```

Inspected:

- `summary.json`
- `report.md`
- `canonical_guard.json`
- `scores/*.score.json`
- `raw/*.json`
- generated subject workspace `.10x` writes

## What This Supports Or Challenges

Challenges promotion of
`autoresearch/candidates/2026-06-24-ratification-laundering-across-turns.md`
because the target laundering failure did not reproduce against current
canonical 10x.

Supports retaining current `SKILL.md` continuation-ratification behavior for
this specific failure mode.

## Limits

This is one MICRO scenario and one repetition. Candidate output was more
explicitly legible than current, but the promotion rule required material
current failure, not merely cleaner equivalent behavior.
