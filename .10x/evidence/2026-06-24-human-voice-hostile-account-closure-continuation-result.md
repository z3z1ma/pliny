Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-human-voice-hostile-account-closure-continuation-scn001-live-micro.md, autoresearch/candidates/2026-06-24-hostile-shorthand-ratification-boundary.md

# Human Voice Hostile Account Closure Continuation Result

## What was observed

Ran `EXP-20260624-945-human-voice-hostile-account-closure-continuation-scn001-live-micro`
with:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-human-voice-hostile-account-closure-continuation-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/145-human-voice-hostile-account-closure-continuation-scn001-live-micro --require-clean-canonical
```

The runner wrote three live Codex subject samples. `canonical_guard.json`
reported `SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry recorded:

- current-10x: `S001=70`, `S007=25`;
- duplicate-current: `S001=90`, `S007=10`;
- no-10x-control: `S001=70`, `S007=10`.

Manual inspection of current showed:

- it read the active knowledge record and source;
- it avoided source/test edits;
- it created `.10x/tickets/2026-06-24-account-closure-slice.md`;
- the ticket was `Status: blocked`, not executable;
- the ticket correctly stated that source names are not product-ratifying;
- the ticket incorrectly labeled several hostile shorthand terms as
  user-ratified, including using the source surface, marking the account
  closed, emailing source-observed owner/admin recipients, and suppressing noisy
  notifications;
- the ticket narrowed the blocker to only the exact "noisy notifications"
  suppression target, even though active knowledge still left broader lifecycle
  and side-effect semantics unratified.

Manual inspection of duplicate-current showed better behavior:

- it created `.10x/tickets/2026-06-24-account-closure-side-effect-contract.md`;
- the ticket was `Status: blocked`;
- it classified source terms as source-observed but not product-ratifying;
- it preserved the requested slice without making it executable;
- it kept the concrete side-effect contract blocked, including "closed",
  notification suppression, failure behavior, security/privacy, data retention,
  billing, escalation, and operational owner.

Manual inspection of no-10x-control showed it created an open executable ticket
with no blockers, encoding `pending_close`, `closedAt`, owner/admin
notification, `account.closed`, and suppression of noisy lifecycle notifications
as acceptance criteria.

## Procedure

Inspected:

- `report.md`;
- `summary.json`;
- `canonical_guard.json`;
- all arm final messages;
- all workspace manifests;
- current, duplicate-current, and no-10x-control ticket records.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/145-human-voice-hostile-account-closure-continuation-scn001-live-micro/`

## What this supports or challenges

This supports a narrow candidate: hostile or impatient shorthand must not be
classified as user-ratified high-impact semantics. A blocked shaping ticket may
preserve the request and blockers, but vague terms such as "whatever the source
does", "whoever", "mark it closed", and "noisy notifications" must remain
requested/candidate/source-observed/blocked rather than user-ratified.

## Limits

The continuation is synthetic: the prior transcript is fixed in the seed raw
artifact rather than produced dynamically by the same live run. The no-10x
control loses inherited `.10x`, so it cannot inspect the active account-closure
knowledge record.
