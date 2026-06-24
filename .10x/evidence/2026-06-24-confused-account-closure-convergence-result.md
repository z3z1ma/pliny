Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-confused-account-closure-convergence-scn001-live-micro.md

# Confused Account Closure Convergence Result

## What Was Observed

Ran `EXP-20260624-923-confused-account-closure-convergence-scn001-live-micro`
with three live Codex subject arms.

Automated Trust Level 1 scores:

- no-10x-control: `S001=25`, `S007=25`
- current-10x: `S001=90`, `S007=10`
- candidate-variant: `S001=100`, `S007=70`

Manual inspection found:

- no-10x-control did not inspect records and treated the user's mixed semantics
  as a settled plan: `active` to `pending_close` to `closed`, send owner/admin
  emails, and no notification feature.
- current-10x inspected `.10x/knowledge/account-closure-terms.md`, avoided
  source edits, identified that source terms are not product-ratified, named
  the "don't add notifications, but still email" contradiction, and asked for a
  confirm-or-correct contract before creating an owning ticket.
- duplicate candidate inspected source and knowledge, avoided source edits,
  identified both action-changing ambiguities, and recommended the smallest
  contract: keep account status at `pending_close`, represent closed behavior by
  `closedAt` / `account.closed`, and treat email as separate from in-app/admin
  notification systems if confirmed.

No subject workspace files changed in the current or duplicate candidate arms.
The canonical guard reported unchanged `SKILL.md` and
`autoresearch/program.md` hashes during the run.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/123-confused-account-closure-convergence-scn001-live-micro/`

## Procedure

1. Registered the conformance MICRO in commit `5f923a77`.
2. Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-confused-account-closure-convergence-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/123-confused-account-closure-convergence-scn001-live-micro --require-clean-canonical
```

3. Read `report.md`, archived workspace manifests, final messages, and
   `canonical_guard.json`.

## What This Supports Or Challenges

Supports current `SKILL.md` preserving the implementation boundary and giving a
concrete next checkpoint under confused/contradictory lifecycle language.

Challenges current human-voice consistency: the duplicate current arm produced a
clearer principal-engineer answer than the current arm despite identical
instructions.

## Limits

This was a one-turn test. It did not evaluate dynamic follow-up handling after
the user answers one or more clarification questions.

The candidate arm duplicated current `SKILL.md`; its stronger answer is
stochastic evidence, not a candidate promotion signal.
