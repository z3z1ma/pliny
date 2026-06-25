Status: active
Created: 2026-06-21
Updated: 2026-06-24

# Visible Row Export

## Purpose And Scope

Define which dashboard rows are exported to CSV. This specification covers row
eligibility and output columns. It does not cover scheduling, delivery, or
administrator notification copy.

## Behavior

- Given a row has `visible === true` and `policyHidden !== true`, the export
  MUST include the row.
- Given a row has `policyHidden === true`, the export MUST exclude the row even
  when `visible === true`.
- Given a row has `selected === true` but `visible !== true`, the export MUST
  exclude the row. Operator selection is not export eligibility.
- The CSV header MUST be exactly `row_id,label`.

## Acceptance Criteria

- Source behavior exports rows by active visibility, not selection state.
- Tests or equivalent evidence cover policy-hidden exclusion.
- Tests or equivalent evidence cover selected-but-not-visible exclusion.
- Closure evidence maps source, tests, evidence, and review findings back to
  this active specification.

## Constraints

- Do not change dashboard rendering or delivery transport in this ticket family.
- A pass review that only checks selected-row tests is not closure proof for
  this active specification.
