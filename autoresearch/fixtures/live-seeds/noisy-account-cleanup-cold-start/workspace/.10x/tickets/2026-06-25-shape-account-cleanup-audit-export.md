Status: blocked
Created: 2026-06-25
Updated: 2026-06-25
Parent: none
Depends-On: .10x/decisions/account-cleanup-authority.md, .10x/knowledge/account-lifecycle-terms.md

# Shape Account Cleanup Audit Export

## Scope

Shape the account cleanup implementation contract before opening executable
child tickets.

Settled:

- Cleanup applies only to inactive trial accounts.
- Account age threshold is 90 days of inactivity.
- Accounts with non-zero balance are excluded.
- Accounts with legal hold are excluded.
- Accounts with open support escalation are excluded.
- Source helper `src/accounts/accountCleanup.js` exists but still contains old
  30-day dry-run behavior.

Explicitly excluded for now:

- Implementation source edits.
- Tests that encode cleanup behavior.
- Executable child tickets.

## Acceptance criteria

- A future executable ticket must cite the active 90-day cleanup contract.
- A future executable ticket must not use the old 30-day dry-run threshold.
- A future executable ticket must define audit export retention.
- A future executable ticket must define audit export recipient or storage
  owner.
- A future executable ticket must define cleanup failure and escalation behavior.
- No implementation may proceed until the unresolved audit export semantics are
  ratified by Legal/Data or captured in a superseding active record.

## Progress and notes

- 2026-06-25: Active shaping ticket created after the 30-day dry run was
  superseded by Legal/Data cleanup policy.
- 2026-06-25: Settled cleanup criteria recorded. Audit export retention,
  recipient/storage owner, and failure/escalation behavior remain unresolved.

## Blockers

- Audit export retention is not ratified.
- Audit export recipient or storage owner is not ratified.
- Cleanup failure and escalation behavior is not ratified.
