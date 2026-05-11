# Campaign Summary Data Foundation

ID: ticket:20260510-campaign-summary-data-foundation
Type: Ticket
Status: closed
Created: 2026-05-10
Updated: 2026-05-10
Risk: medium - establishes shared OpenDota summary data loading, malformed payload handling, and safe asset URL handling used by later UI slices.
Depends On: ticket:20260510-campaign-stack-foundation

## Summary

Implement the summary-data foundation for the Campaign Map: safe API helpers, hero normalization, summary endpoint loading for `/heroStats`, `/proMatches`, `/publicMatches`, item constants support only if needed by later slices, and robust per-source loading/error/empty behavior.

## Related Records

- `plan:20260510-rts-meta-explorer` - sequences this after stack foundation.
- `spec:opendota-rts-meta-explorer` - requires public OpenDota data and robust failure handling.
- `research:20260510-opendota-api-shape` - records summary endpoint shapes.

## Scope

May change:

- `src/api.js`
- `src/analytics.js` summary helpers
- app-level summary loading state in `src/main.jsx`
- minimal UI needed to expose loading/error state

Must not change:

- final campaign visual layout beyond basic consumers
- hero deep analytics territories
- match detail drilldowns
- backend services or credentials

## Acceptance

- ACC-001: Summary endpoints are fetched through shared helpers that reject non-array payloads where arrays are expected.
  - Evidence: source inspection and build check.
  - Audit: challenge malformed successful payload handling.

- ACC-002: Hero data is normalized and joined to safe hero image/icon URLs using expected Dota asset path prefixes only.
  - Evidence: source inspection.
  - Audit: challenge external asset path assumptions.

- ACC-003: The app can render partial summary data and visible warnings when one summary endpoint fails.
  - Evidence: source inspection; simulated runtime evidence if available.
  - Audit: challenge whether partial failure leaves useful UI.

## Current State

Closed. Summary API helpers, hero normalization, safe asset handling, and summary loading/error state are in place and verified by build output plus focused fresh-context review in `evidence:20260510-summary-data-foundation-checks`.

Acceptance state:

- ACC-001 satisfied: `/heroStats`, `/proMatches`, and `/publicMatches` use `fetchArray()`, which rejects non-array payloads.
- ACC-002 satisfied after fix: hero image/icon CDN conversion now uses narrow Dota hero asset prefixes rather than any `/apps/dota2/` path.
- ACC-003 satisfied by source review: `Promise.allSettled` preserves partial summary data and renders warnings for failed summary endpoints.

This ticket does not claim browser runtime/CORS behavior or Campaign Map visual quality; those belong to later tickets.

## Journal

- 2026-05-10: Created from the split of cancelled `ticket:20260510-campaign-map-deep-analytics`.
- 2026-05-10: Set active after `ticket:20260510-campaign-stack-foundation` closed.
- 2026-05-10: Focused review found hero asset validation too broad; narrowed asset prefix validation in `src/api.js` and `src/analytics.js`.
- 2026-05-10: Reran `npm run build` and `git diff --check`; follow-up focused review passed. Evidence recorded in `evidence:20260510-summary-data-foundation-checks`.
- 2026-05-10: Closed ticket; next plan move is `ticket:20260510-campaign-map-shell`.
