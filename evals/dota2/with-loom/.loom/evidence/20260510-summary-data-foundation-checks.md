# Campaign Summary Data Foundation Checks

ID: evidence:20260510-summary-data-foundation-checks
Type: Evidence Observation
Status: recorded
Created: 2026-05-10
Updated: 2026-05-10
Observed: 2026-05-10

## Summary

Observed build output and focused fresh-context review for the Campaign Summary Data Foundation slice.

## Related Records

- `ticket:20260510-campaign-summary-data-foundation` - ticket supported by this evidence.
- `research:20260510-opendota-api-shape` - endpoint shape source for the slice.
- `spec:opendota-rts-meta-explorer` - behavior contract for summary data and safe asset handling.

## Procedure And Output

- Ran `npm run build` after narrowing asset prefix validation.
  - Output excerpt:

```text
> ancient-war-room@0.1.0 build
> vite build

vite v8.0.11 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.56 kB │ gzip:  0.35 kB
dist/assets/index-ex-vR8vM.css   13.92 kB │ gzip:  4.16 kB
dist/assets/index-D-VGniOe.js   219.99 kB │ gzip: 68.29 kB

✓ built in 90ms
```

- Ran `git diff --check`.
  - Output: no output; command exited successfully.

- Ran a focused fresh-context review of `src/api.js`, `src/analytics.js`, and summary loading in `src/main.jsx`.
  - Initial review found one blocker: `dotaAsset()` accepted any `/apps/dota2/` path.
  - Fixed by adding allow-listed prefixes in `src/api.js` and narrowing hero/item asset callers in `src/analytics.js`.
  - Follow-up review verdict: pass, with no blocking findings.

## What This Shows

- Supports `ticket:20260510-campaign-summary-data-foundation#ACC-001`: `fetchArray()` rejects non-array payloads, and summary endpoints are loaded through it.
- Supports `ticket:20260510-campaign-summary-data-foundation#ACC-002`: hero image/icon URLs are constrained to expected Dota hero asset prefixes before CDN conversion.
- Supports `ticket:20260510-campaign-summary-data-foundation#ACC-003`: summary loading uses `Promise.allSettled`, preserves successful endpoint data, and surfaces per-endpoint warnings.

## What This Does Not Show

- Does not prove real browser/CORS behavior.
- Does not prove visual Campaign Map quality.
- Does not verify hero deep analytics or match battle report slices.
