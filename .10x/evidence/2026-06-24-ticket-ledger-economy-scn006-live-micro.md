Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-ticket-ledger-economy-scn006-live-micro.md, autoresearch/candidates/2026-06-24-ticket-ledger-economy-guard.md

# Ticket Ledger Economy SCN-006 Live MICRO

## What Was Observed

Live Codex MICRO
`EXP-20260624-869-ticket-ledger-economy-scn006-live-micro` ran three arms
against the simple display-name normalization ticket seed:

- no-10x-control
- current-10x
- candidate-variant

The output root is
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/069-ticket-ledger-economy-scn006-live-micro/`.

The canonical guard recorded no mutation to `SKILL.md` or
`autoresearch/program.md` during the subject run.

Automated scorer output:

- current-10x: `S003=100`
- candidate-variant: `S003=100`
- no-10x-control: `S003=100`

Manual inspection found:

- current-10x created
  `.10x/tickets/2026-06-24-implement-profile-display-name-normalization.md`
  with a complete executable ticket, no implementation, and `Blockers: None`.
  It also added an unnecessary `Assumption Provenance` section for a trivial
  single-spec ticket.
- candidate-variant created the same bounded executable ticket without a
  provenance ledger. It included scope, exclusions, acceptance criteria,
  evidence expectations, references, progress notes, and blockers.
- no-10x-control also created a ticket. This run therefore did not separate
  general ticket readiness, only ledger economy after the prior promotion.

## Procedure

1. Ran the live MICRO through `autoresearch/run_once.py` with
   `--require-clean-canonical`.
2. Opened the generated report and canonical guard.
3. Inspected final messages for all arms.
4. Read current and candidate ticket records.

## What This Supports Or Challenges

Supports promoting
`autoresearch/candidates/2026-06-24-ticket-ledger-economy-guard.md` into
`SKILL.md`.

Challenges the sufficiency of the first limiting clause in the ticket assumption
ledger promotion: current still overused the ledger on a trivial single-source
ticket.

## Limits

One live Codex sample per arm. The seed was deliberately simple; this result
does not weaken the ledger requirement for high-impact or mixed-provenance
tickets.
