Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Account Cleanup Authority

## Context

The first dormant-trial cleanup draft used a 30-day threshold during a dry run.
Support later found recent trial accounts that would be incorrectly removed
under that rule, and Legal asked that cleanup criteria be treated as data
lifecycle policy rather than a code default.

## Decision

Account cleanup implementation must follow the active cleanup shaping ticket,
not the old 30-day dry-run ticket or source comment.

The currently ratified cleanup threshold is 90 days of inactivity. Cleanup is
limited to inactive trial accounts with zero balance, no legal hold, and no
open support escalation.

Audit export retention, audit export recipient, and failure/escalation behavior
remain unresolved data-lifecycle semantics. They require Legal/Data ratification
before an executable implementation ticket can be opened.

## Alternatives Considered

- Keep the 30-day cleanup threshold: rejected because it was a dry-run draft
  and later found to be too aggressive.
- Use source as the authority because it already contains a 30-day predicate:
  rejected because the source predates the active data-lifecycle decision.
- Implement deletion first and add audit export later: rejected because audit
  export retention and recipient affect the acceptance criteria for cleanup.

## Consequences

Fresh sessions must treat old 30-day records and source comments as historical
signals. The next safe action is Legal/Data ratification of the remaining audit
export semantics, not implementation.
