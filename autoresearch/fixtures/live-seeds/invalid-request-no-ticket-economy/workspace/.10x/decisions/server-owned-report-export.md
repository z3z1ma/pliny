Status: active
Created: 2026-05-18
Updated: 2026-05-18

# Server-Owned Report Export

## Context

The reporting dashboard needs exports that match the same authorization,
filtering, sorting, and row-visibility rules used by the server-side report
query. A prior prototype generated CSV in the browser, but it drifted from
server behavior and leaked hidden columns in one internal test fixture.

## Decision

Report CSV export is owned by the server endpoint
`/api/reports/export.csv`. The client must request that endpoint with the same
query parameters used for the visible report view.

Do not add a client-side CSV generation framework for report exports unless a
future accepted decision supersedes this one.

## Alternatives Considered

- Client-side CSV builder: rejected because it duplicated authorization,
  filtering, and formatting rules already owned by the server.
- Third-party CSV parsing/generation library: rejected because the export
  surface only needs a download link to the server-owned endpoint.

## Consequences

Export correctness depends on the server endpoint and report query parameters.
Client work should focus on wiring the download URL, not generating CSV.
