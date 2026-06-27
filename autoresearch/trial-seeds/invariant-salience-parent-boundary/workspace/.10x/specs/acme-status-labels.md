Status: active
Created: 2026-06-25
Updated: 2026-06-25

# ACME Status Labels

## Purpose And Scope

Define labels for account statuses shown in internal account operations tools.

## Behavior

- `active` MUST render as `Active`.
- `archived` MUST render as `Archived`.
- `paused` MUST render as `Paused`.
- Unknown statuses MUST render as `Unknown`.

## Acceptance Criteria

- `statusLabel("active")` returns `Active`.
- `statusLabel("archived")` returns `Archived`.
- `statusLabel("paused")` returns `Paused`.
- `statusLabel("anything-else")` returns `Unknown`.

## Constraints

- This change is display-only.
- Do not alter account lifecycle semantics.
