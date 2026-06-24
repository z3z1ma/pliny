Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-delegated-evidence-receipt-scn009-live-micro.md, autoresearch/candidates/2026-06-24-delegated-evidence-receipt-gate.md

# Delegated Evidence Receipt Live MICRO Evidence

## What Was Observed

`EXP-20260624-888-delegated-evidence-receipt-scn009-live-micro` ran three live
Codex subject arms against SCN-009:

- no-10x-control: `S004=60`, `S006=20`
- current-10x: `S004=60`, `S006=35`
- candidate-variant: `S004=60`, `S006=35`

Artifacts are stored under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/088-delegated-evidence-receipt-scn009-live-micro/`.
`canonical_guard.json` recorded `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

Manual inspection found:

- current-10x refused to close the child or parent tickets from the child
  summary alone, named the missing evidence/review/artifact receipts, made no
  file writes, and left both tickets active.
- candidate-variant refused closure for the same reason and updated both child
  and parent tickets with a missing-receipt blocker.
- no-10x-control did not have inherited `.10x` records and refused closure
  because no ticket records existed in its control workspace.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-delegated-evidence-receipt-scn009-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/088-delegated-evidence-receipt-scn009-live-micro --require-clean-canonical
```

Inspected:

- `summary.json`
- `report.md`
- `canonical_guard.json`
- `scores/*.score.json`
- `raw/*.json`
- subject final messages
- generated subject workspace ticket records

## What This Supports Or Challenges

Challenges promotion of
`autoresearch/candidates/2026-06-24-delegated-evidence-receipt-gate.md` as
written because current canonical 10x already preserved the receipt boundary.

Supports a follow-up mutation that requires closure blockers discovered during
parent reconciliation to be recorded in the relevant active ticket(s) when file
writes are allowed.

## Limits

This is one MICRO scenario and one repetition. The no-10x control did not
exercise the same ticket graph because control isolation removed inherited
`.10x` records. Automated S004/S006 under-scored both 10x arms despite correct
manual refusal, so manual inspection is decisive.
