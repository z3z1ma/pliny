# Hero Picker Overlap Fix

ID: ticket:20260510-hero-picker-overlap-fix
Type: Ticket
Status: closed
Created: 2026-05-10
Updated: 2026-05-10
Risk: low - narrow CSS fix for side-panel scroll behavior and hero picker visibility.

## Summary

Fix the right-side Hero Scout panel overlapping the hero picker while scrolling. The user-provided screenshot showed the sticky Hero Scout card covering most of the roster, making the actual hero picker barely visible.

## Related Records

- `plan:20260510-rts-meta-explorer` - completed Campaign Map plan receiving this small follow-up fix.
- `spec:opendota-rts-meta-explorer` - requires responsive, usable exploration controls.

## Scope

May change:

- `src/styles.css`
- this ticket and evidence records

Must not change:

- OpenDota data behavior
- Campaign Map interaction model
- backend services or dependencies

## Acceptance

- ACC-001: Hero Scout no longer uses sticky positioning that can overlay the roster while scrolling.
  - Evidence: source inspection of `src/styles.css` and build output.
  - Audit: separate audit would not add useful trust for this narrow CSS fix.

- ACC-002: The hero picker roster has more usable vertical space after the fix.
  - Evidence: source inspection of portrait height and roster max-height changes.
  - Audit: separate audit would not add useful trust; real browser visual verification remains optional follow-up.

- ACC-003: The app still builds after the CSS change.
  - Evidence: `evidence:20260510-hero-picker-overlap-fix`.
  - Audit: separate audit would not add useful trust for build evidence.

## Current State

Closed. `src/styles.css` now makes `.hero-panel` relative rather than sticky, reduces hero portrait minimum height, and increases roster max-height. `npm run build` and `git diff --check` passed.

## Journal

- 2026-05-10: Created and closed after applying the narrow CSS fix requested by the operator.
