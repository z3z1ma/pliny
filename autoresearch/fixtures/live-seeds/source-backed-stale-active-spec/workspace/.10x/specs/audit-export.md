Status: active
Created: 2026-06-18
Updated: 2026-06-18

# Audit Export

## Purpose And Scope

Define the operator audit export surface.

## Behavior

- Audit export MUST be generated only as a local CSV file.
- Audit export MUST NOT expose an HTTP API route.
- The CSV header MUST be exactly `event_id,actor,action`.

## Acceptance Criteria

- No HTTP API route exists for audit export.
- CSV output uses `event_id,actor,action`.

## Constraints

- This specification predates the API-route decision in
  `.10x/decisions/audit-export-api-route.md`.
