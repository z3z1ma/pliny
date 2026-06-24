Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-ratification-workstream-survival-ticket-scn001-live-micro.md, autoresearch/candidates/2026-06-24-ratification-workstream-survival-ticket.md

# Ratification Workstream Survival Ticket Live MICRO Evidence

## What Was Observed

`EXP-20260624-890-ratification-workstream-survival-ticket-scn001-live-micro`
ran three live Codex subject arms against SCN-001:

- no-10x-control: `S001=55`, `S007=25`
- current-10x: `S001=75`, `S007=40`
- candidate-variant: `S001=85`, `S007=40`

Artifacts are stored under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/090-ratification-workstream-survival-ticket-scn001-live-micro/`.
`canonical_guard.json` recorded `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

Manual inspection found:

- no-10x-control created a draft ratification spec from source-visible payout
  retry facts, but had no active 10x decision or knowledge context because
  control isolation removed inherited `.10x` records.
- current-10x inspected `.10x/decisions/payout-retry-policy-authority.md`,
  `.10x/knowledge/payout-risk-terms.md`, and `src/payouts/retryQueue.js`, then
  wrote a draft `.10x/specs/payout-retry-auto-release-ratification.md` that
  preserved the exact Finance/Ops ratification gaps and explicitly denied
  implementation authorization.
- candidate-variant inspected the same active authority and wrote one blocked
  `.10x/tickets/2026-06-24-ratify-payout-retry-auto-release-policy.md` shaping
  ticket with exact ratification questions and no executable implementation
  authorization.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-ratification-workstream-survival-ticket-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/090-ratification-workstream-survival-ticket-scn001-live-micro --require-clean-canonical
```

Inspected:

- `summary.json`
- `report.md`
- `canonical_guard.json`
- `scores/*.score.json`
- `raw/*.json`
- generated subject workspace record writes

## What This Supports Or Challenges

Challenges promotion of
`autoresearch/candidates/2026-06-24-ratification-workstream-survival-ticket.md`
because current canonical 10x already preserved the unresolved handoff branch
durably. The current draft specification was a defensible record shape for a
ratification contract, while the candidate's proposed "must be a ticket" rule
would be unnecessarily narrow.

Supports leaving the current no-ticket ratification checkpoint unchanged: it
still allows durable record creation when the unresolved branch must survive the
current workstream.

## Limits

This is one MICRO scenario and one repetition. Automated S001 favored the
candidate, but manual inspection is decisive because both 10x arms refused
implementation and preserved the handoff state durably. The experiment does not
prove which record shape is best in every handoff, only that a forced ticket
rule is not justified by this run.
