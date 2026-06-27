Status: open
Created: 2026-06-25
Updated: 2026-06-25
Parent: none
Depends-On: .10x/specs/payments-retry-window.md

# Implement Payments Webhook Retry

## Scope

Implement the behavior described by `.10x/specs/payments-retry-window.md`.

Explicitly excluded:

- changing retry duration;
- changing the backoff cap;
- changing webhook authentication.

## Acceptance Criteria

- Implementation satisfies `.10x/specs/payments-retry-window.md`.
- Tests cover transient failure retry, retry-window expiry, and success cleanup.

## Progress And Notes

- 2026-06-25: Opened against `.10x/specs/payments-retry-window.md`.
- 2026-06-25: Terminology review found "retry window" is misleading because the
  record governs a whole webhook retry policy, not only duration.
- Historical note: before rename, `rg "payments-retry-window"` returned:

```text
.10x/tickets/2026-06-25-implement-payments-webhook-retry.md:5:Depends-On: .10x/specs/payments-retry-window.md
.10x/specs/payments-retry-window.md:5:# Payments Retry Window
```

## Blockers

- None. The requested rename is terminology-only.
