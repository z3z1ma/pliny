Status: active
Created: 2026-06-24
Updated: 2026-06-24
Parent:
Depends-On: .10x/specs/zeus-webhook-retry.md

# Implement Zeus Webhook Retry

## Scope

Implement Zeus ledger webhook retry handling according to
`.10x/specs/zeus-webhook-retry.md`.

Included:

- Retry scheduling for receiver failures.
- Idempotency-key persistence.

Excluded:

- Provider API version migration.
- Notification behavior.

## Acceptance Criteria

- Implementation follows `.10x/specs/zeus-webhook-retry.md`.
- Tests cover retryable and terminal receiver responses.
- No customer notification behavior changes.

## Progress And Notes

- 2026-06-24: Opened from the draft Zeus retry specification.
- 2026-06-24: Historical note: this ticket was initially scoped around
  `.10x/specs/zeus-webhook-retry.md`, which had not yet passed Security review.

## Blockers

- Security review has not approved the draft retry semantics.
