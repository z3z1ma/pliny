Status: active
Created: 2026-06-24
Updated: 2026-06-25
Parent: none
Depends-On: .10x/specs/visible-row-export.md

# Visible Row Export Parent

## Scope

Deliver the visible-row CSV export behavior described in
`.10x/specs/visible-row-export.md`.

Child tickets:

- `.10x/tickets/2026-06-24-align-visible-row-export.md`

Explicitly excluded:

- dashboard rendering;
- delivery transport;
- administrator notification copy.

## Acceptance Criteria

- Child ticket satisfies `.10x/specs/visible-row-export.md`.
- Evidence proves active-spec behavior, including policy-hidden exclusion and
  selected-but-not-visible exclusion.
- Review concerns are resolved or residual risk is explicitly accepted.
- Parent closure preserves references after moving child tickets to terminal
  state.

## Progress And Notes

- 2026-06-24: Child reported first implementation complete.
- 2026-06-24: Active-spec fail review identified selected-row behavior.
- 2026-06-25: Child reported repair complete.
- 2026-06-25: Fresh evidence and active-spec pass review are recorded.

## Blockers

- None currently recorded. Historical fail review findings are recorded as
  resolved by `.10x/reviews/2026-06-25-visible-row-active-spec-pass-review.md`.
