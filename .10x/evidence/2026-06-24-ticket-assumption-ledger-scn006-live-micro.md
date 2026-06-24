Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-ticket-assumption-ledger-scn006-live-micro.md, autoresearch/candidates/2026-06-24-ticket-assumption-ledger.md

# Ticket Assumption Ledger SCN-006 Live MICRO

## What Was Observed

Live Codex MICRO
`EXP-20260624-868-ticket-assumption-ledger-scn006-live-micro` ran three arms
against the mixed-provenance billing export seed:

- no-10x-control
- current-10x
- candidate-variant

The output root is
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/068-ticket-assumption-ledger-scn006-live-micro/`.

The canonical guard recorded no mutation to `SKILL.md` or
`autoresearch/program.md` during the subject run.

Automated scorer output:

- current-10x: `S003=100`
- candidate-variant: `S003=100`
- no-10x-control: `S003=80`

Manual inspection found:

- current-10x created a strong executable ticket at
  `.10x/tickets/2026-06-24-implement-billing-exceptions-csv-export.md`. The
  ticket included governing references, scope, exclusions, acceptance criteria,
  evidence expectations through tests, the user-ratified `owner_email` column,
  and `Blockers: None`. Provenance was accurate but distributed through prose.
- candidate-variant created the same bounded executable ticket and additionally
  included a compact `Assumption Provenance` section. It separated
  record-backed behavior, source-observed facts, current user-ratified behavior,
  and blocked assumptions.
- no-10x-control created a ticket without available records because control
  isolation removed inherited `.10x`; it correctly noted that active spec and
  decision paths needed attachment before execution.

Candidate and current both avoided implementation source edits.

## Procedure

1. Ran the live MICRO through `autoresearch/run_once.py` with
   `--require-clean-canonical`.
2. Opened the generated report and canonical guard.
3. Inspected final messages for all arms.
4. Read the current and candidate ticket records.
5. Read workspace manifests to confirm only ticket records changed for current
   and candidate.

## What This Supports Or Challenges

Supports promoting
`autoresearch/candidates/2026-06-24-ticket-assumption-ledger.md` into
`SKILL.md`.

The evidence supports a narrow rule for mixed-provenance or high-impact
executable tickets, not a universal ledger requirement for every trivial ticket.

## Limits

One live Codex sample per arm. The experiment tests ticket authoring quality,
not whether a child executor performs better from the provenance ledger.
