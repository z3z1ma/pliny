Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Audit Export API Route

## Context

The CSV-only audit export spec from 2026-06-18 blocks the operations dashboard
from fetching exports without filesystem access. Engineering implemented and
reviewed a small HTTP route after Product ratified API delivery for the operator
dashboard.

## Decision

Audit export is now served through `GET /internal/audit/export.json` returning
JSON rows with `eventId`, `actor`, and `action`. The older CSV-only spec must be
superseded or replaced before future implementation tickets use it.

## Alternatives Considered

- Keep CSV-only export: rejected because the operator dashboard cannot read
  local files.
- Add a downloadable CSV route: rejected because the dashboard needs structured
  rows for filtering before download.

## Consequences

The source route and tests are intended behavior. The active spec
`.10x/specs/audit-export.md` is stale until the record graph is repaired.
