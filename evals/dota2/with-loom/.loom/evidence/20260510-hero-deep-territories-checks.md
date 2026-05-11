# Hero Deep Analytics Territories Checks

ID: evidence:20260510-hero-deep-territories-checks
Type: Evidence Observation
Status: recorded
Created: 2026-05-10
Updated: 2026-05-10
Observed: 2026-05-10

## Summary

Observed build output and focused review for selected-hero deep analytics territories.

## Related Records

- `ticket:20260510-hero-deep-territories` - ticket supported by this evidence.
- `research:20260510-opendota-deep-analytics` - endpoint shape source for the slice.
- `spec:opendota-rts-meta-explorer` - behavior contract for deep analytics and account ID handling.

## Procedure And Output

- Ran `npm run build` after adding selected-hero recent raids loading state.
  - Output excerpt:

```text
> ancient-war-room@0.1.0 build
> vite build

vite v8.0.11 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.56 kB │ gzip:  0.35 kB
dist/assets/index-GCqj1Z3R.css   14.00 kB │ gzip:  4.19 kB
dist/assets/index-Dpqm3iX1.js   220.11 kB │ gzip: 68.34 kB

✓ built in 89ms
```

- Ran `git diff --check`.
  - Output: no output; command exited successfully.

- Ran focused fresh-context review for hero deep territories.
  - Initial verdict: pass with reservations. It found one medium issue: selected-hero recent raids showed empty state while `heroIntel.loading` was true.
  - Fixed by passing `heroIntel.loading` into `RecentHeroMatches`, rendering a loading state, and suppressing empty/cards until loading is false.
  - Follow-up review verdict: pass for the recent-raids loading fix.

## What This Shows

- Supports `ticket:20260510-hero-deep-territories#ACC-001`: selected hero changes trigger lazy hero-specific requests without preloading every hero.
- Supports `ticket:20260510-hero-deep-territories#ACC-002`: source renders matchup, duration, item phase, specialist, and recent hero match territories with loading/empty handling.
- Supports `ticket:20260510-hero-deep-territories#ACC-003`: specialist UI uses anonymized labels and does not display raw `account_id` values.

## What This Does Not Show

- Does not prove live browser/API runtime behavior.
- Does not verify match detail battle reports beyond selected hero match links.
- Does not prove visual quality in a real browser.
