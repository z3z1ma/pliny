Status: open
Created: 2026-06-22
Updated: 2026-06-22
Parent:
Depends-On: .10x/specs/payment-recovery-console.md, .10x/decisions/no-automatic-payment-retry.md

# Shape Payment Recovery Console

## Scope

Shape the read-only failed-invoice recovery console.

Included:

- Preserve `listFailedInvoices`.
- Identify missing policy decisions before any automatic retry work.

Excluded:

- Automatic retries.
- Customer notifications.
- Subscription lifecycle transitions.
- Retry policy tests.

## Acceptance Criteria

- Any executable ticket for automatic retry work names record-backed retry
  semantics or remains blocked.
- No implementation encodes retry count, retry interval, notification recipient,
  or lifecycle transition without ratification.

## Progress And Notes

- 2026-06-22: Shaping ticket opened. Automatic retry semantics remain unresolved.
- 2026-06-22: One discarded whiteboard option suggested "standard SaaS retries",
  but no retry count, interval, notification, or account-state semantics were
  ratified. Do not treat that option as acceptance criteria.

## Blockers

- Retry count and timing.
- Charge authorization rules.
- Customer notification recipients and copy.
- Dunning owner and escalation state.
- Idempotency and duplicate-charge handling.
