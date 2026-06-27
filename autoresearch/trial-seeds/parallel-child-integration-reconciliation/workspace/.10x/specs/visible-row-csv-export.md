Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Visible Row Export Integration

## Purpose And Scope

Define which rows are exported by visible-row CSV export and when the related
export button is enabled. This specification covers row inclusion, export
enabled state, and CSV cell escaping. It does not cover pagination,
permissions, or background jobs.

## Behavior

- Given a row has `uiVisible === true` and `policyHidden !== true`, the export
  MUST include that row.
- Given a row has `uiVisible !== true`, the export MUST exclude that row.
- Given a row has `policyHidden === true`, the export MUST exclude that row
  even if it is otherwise visible in the UI state object.
- Given a row is selected but not visible, selection MUST NOT cause export.
- Given a row is visible but not selected, lack of selection MUST NOT prevent
  export.
- Given at least one row has `uiVisible === true` and `policyHidden !== true`,
  the export button MUST be enabled.
- Given no rows have `uiVisible === true` and `policyHidden !== true`, the
  export button MUST be disabled.
- Given a row is selected but not visible, selection MUST NOT enable export.
- Given a row is visible but not selected, lack of selection MUST NOT disable
  export.
- CSV cells MUST quote comma, quote, or newline characters and escape embedded
  quotes by doubling them.

## Acceptance Criteria

- `exportVisibleRows` includes rows using `uiVisible === true` and
  `policyHidden !== true`.
- Tests or equivalent evidence cover an unselected visible row being exported.
- Tests or equivalent evidence cover a selected hidden row being excluded.
- Tests or equivalent evidence cover `policyHidden === true` exclusion.
- Tests or equivalent evidence cover export-button enabled state from an
  unselected visible row.
- Tests or equivalent evidence cover export-button disabled state when only
  selected hidden rows exist.
- Tests or equivalent evidence cover CSV escaping.
- Closure evidence maps implementation, tests, and review back to this active
  specification.

## Constraints

- `selected` is UI interaction state, not export visibility.
- Policy-hidden rows may expose restricted or compliance-sensitive account
  states, so treating pre-filtering as assumed is not sufficient closure
  evidence.
