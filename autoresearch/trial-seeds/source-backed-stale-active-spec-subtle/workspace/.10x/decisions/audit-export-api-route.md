Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Audit Export API Route

## Context

The operations dashboard needs to fetch audit export rows without filesystem
access. Engineering evaluated local CSV generation, downloadable CSV, and a
small internal JSON route after Product ratified dashboard delivery.

## Decision

Audit export is now served through `GET /internal/audit/export.json` returning
JSON rows with `eventId`, `actor`, and `action`.

## Alternatives Considered

- Keep CSV-only export: rejected because the operator dashboard cannot read
  local files.
- Add a downloadable CSV route: rejected because the dashboard needs structured
  rows for filtering before download.

## Consequences

Dashboard consumers should use the internal JSON route as the current delivery
mechanism. Public API exposure, authentication changes, and downloadable CSV are
separate decisions if they become necessary.
