Status: active
Created: 2026-06-24
Updated: 2026-06-24
Parent:
Depends-On: .10x/specs/acme-retry-window.md

# Implement ACME Webhook Retry

## Scope

Implement ACME ledger webhook retry handling according to
`.10x/specs/acme-retry-window.md`.

Included:

- Retry scheduling for `5xx` receiver failures.
- Terminal duplicate handling for `409`.
- Idempotency persistence using `delivery_id`.

Excluded:

- Customer notification behavior.
- Provider API migration.
- Backfill processing.

## Acceptance Criteria

- Implementation follows `.10x/specs/acme-retry-window.md`.
- Tests cover retryable, duplicate, and terminal failure receiver responses.
- No customer notification behavior changes.

## Progress And Notes

- 2026-06-24: Opened from the ratified ACME retry behavior.
- 2026-06-24: Historical note: this ticket was originally scoped around
  `.10x/specs/acme-retry-window.md` before Product ratified "webhook retry
  policy" as the durable term.

## Blockers

- None.
