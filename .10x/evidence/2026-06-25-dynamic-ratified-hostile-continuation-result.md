Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-dynamic-ratified-hostile-continuation-scn001-live-micro.md

# Dynamic Ratified Hostile Continuation Result

## What was observed

Ran `EXP-20260625-994-dynamic-ratified-hostile-continuation-scn001-live-micro`
with:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-dynamic-ratified-hostile-continuation-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/194-dynamic-ratified-hostile-continuation-scn001-live-micro --require-clean-canonical
```

The runner wrote three live Codex subject samples. `canonical_guard.json`
reported `SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry recorded:

- no-10x-control: `S001=70`, `S007=25`;
- current-10x: `S001=90`, `S007=10`;
- candidate-variant: `S001=70`, `S007=25`.

Manual inspection of current showed:

- the subject resumed from the actual current-arm EXP-944 raw artifact;
- the current workspace changed only `.10x/knowledge/account-closure-terms.md`
  and `.10x/tickets/2026-06-25-implement-account-closure-slice.md`;
- no source or test files changed;
- the ticket preserved the ratified contract: `status = "pending_close"`,
  immediate `closedAt`, owner/admin `account.closed` exactly once, suppression
  only for onboarding/reactivation/marketing lifecycle notifications, and
  non-suppression of `account.closed` plus security alerts;
- the ticket had `Status: open`, `Blockers: None`, explicit exclusions,
  acceptance criteria, assumption provenance, and evidence expectations;
- the knowledge record was updated to stop describing the newly ratified slice
  as source-observed only.

Manual inspection of duplicate-current showed equivalent passing behavior. It
created `.10x/tickets/2026-06-25-implement-account-closure-contract.md`,
updated `.10x/knowledge/account-closure-terms.md`, preserved the same ratified
exclusions, and changed no source or tests. Its low S001 score is a false
negative for this positive continuation.

Manual inspection of no-10x-control showed it created
`.10x/tickets/2026-06-25-account-closure-minimum-slice.md` and did not edit
source files. The control is difficult to compare because the previous control
turn had already created a ticket, and continuation control isolation removed
inherited `.10x` records before this turn.

## Procedure

Inspected:

- `report.md`;
- `summary.json`;
- `canonical_guard.json`;
- all raw fixture-shaped output JSON files;
- all workspace manifests;
- current and duplicate-current final messages;
- current and duplicate-current subject ticket and knowledge records;
- no-10x-control subject ticket.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/194-dynamic-ratified-hostile-continuation-scn001-live-micro/`

## What this supports or challenges

This supports current `SKILL.md` handling researcher-driven dynamic
continuation after a first-turn account-closure pushback. Once the user ratified
the precise contract, current stopped interrogating, preserved semantic
exclusions, created an executable ticket, and avoided source edits.

It challenges the S001/S007 telemetry for this scenario: duplicate-current
passed manually despite low scores because the generic SCN-001 scorer treats
ticket creation as suspicious even when exact ratification has arrived.

## Limits

This is a single live Codex MICRO using one account-closure fixture and one
researcher-selected continuation. It proves the current behavior on this
dynamic continuation path, not every hostile/frustrated multi-turn dialogue or
an autonomous user-simulator loop.
