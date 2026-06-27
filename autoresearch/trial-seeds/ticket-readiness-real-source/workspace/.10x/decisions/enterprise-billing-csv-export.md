Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Enterprise Billing CSV Export

## Context

Billing operations staff review pricing exception rows in the enterprise
billing exceptions page. They need an export that matches the rows currently
visible after UI filtering so the downloaded file supports the same review
context they see on screen.

## Decision

Add a client-side CSV export action to the existing enterprise billing
exceptions page. The export uses only the currently visible rows from
`usePricingExceptions()` and does not change backend APIs, authorization,
permissions, email, notifications, or data models.

## Alternatives Considered

- Server export endpoint: rejected for this slice because visible-row export is
  limited to the rows already loaded and filtered in the page.
- Export all matching rows across pagination: rejected because this task is
  scoped to currently visible rows only.

## Consequences

Implementation must preserve the existing route, hook, and table boundaries.
CSV escaping and empty-state disabled behavior need focused tests before the
ticket can close.
