Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-fish-before-opening-scn005-live-micro.md, autoresearch/candidates/2026-06-23-fish-before-opening-pressure.md

# Fish Before Opening SCN-005 Live MICRO

## What Was Observed

Ran `EXP-20260623-854-fish-before-opening-scn005-live-micro` with one live
Codex sample for each arm.

Automated Trust Level 1 score vectors:

- current-10x: `S002=30`, `S005=80`
- candidate-variant: `S002=80`, `S005=80`
- no-10x-control: `S002=80`, `S005=80`

The canonical guard reported no changes to `SKILL.md` or
`autoresearch/program.md` during the run.

Manual inspection found:

- current-10x created no duplicate ticket and made no source edits, but it also
  made no durable record update for the current explicit follow-up request.
- candidate-variant updated the existing active ticket
  `.10x/tickets/2026-06-23-add-csv-export-quote-newline-coverage.md` with the
  new request context, created no duplicate ticket, and made no source edits.
- no-10x-control created a new ticket because its inherited `.10x` record graph
  had been removed as part of control isolation.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/054-fish-before-opening-scn005-live-micro/`

## Procedure

1. Registered `candidate-fish-before-opening-pressure-v1` and a SCN-005 live
   seed with one existing active CSV quote/newline coverage ticket.
2. Ran `python3 autoresearch/validate.py`.
3. Ran `python3 -m unittest discover autoresearch/tests`; 52 tests passed.
4. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-fish-before-opening-scn005-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/054-fish-before-opening-scn005-live-micro --require-clean-canonical`.
5. Read the score report, canonical guard, archived workspace manifests, final
   messages, and ticket bodies for current, candidate, and control.

## What This Supports Or Challenges

Supports promoting `candidate-fish-before-opening-pressure-v1` into `SKILL.md`
as a narrow fish-before-opening pressure rule. The candidate improved durable
record ownership while preserving the no-duplicate-ticket invariant.

Challenges the Trust Level 1 scorer for controls in this scenario: because the
control workspace intentionally removes inherited `.10x`, it cannot use the
seeded active owner and its positive S002 score is not comparable.

## Limits

This is one MICRO seed and one sample per arm. It does not prove the promoted
rule handles every ambiguous duplicate-ticket case, terminal-ticket reopening
case, or materially distinct follow-up.
