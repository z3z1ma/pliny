# Match Battle Reports Checks

ID: evidence:20260510-match-battle-reports-checks
Type: Evidence Observation
Status: recorded
Created: 2026-05-10
Updated: 2026-05-10
Observed: 2026-05-10

## Summary

Observed build output and focused review for Chronicle and selected match Battle Report behavior.

## Related Records

- `ticket:20260510-match-battle-reports` - ticket supported by this evidence.
- `research:20260510-opendota-deep-analytics` - match detail payload source for the slice.
- `spec:opendota-rts-meta-explorer` - behavior contract for recent matches and selected battle reports.

## Procedure And Output

- Ran `npm run build` after battle report fixes.
  - Output excerpt:

```text
> ancient-war-room@0.1.0 build
> vite build

vite v8.0.11 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.56 kB │ gzip:  0.35 kB
dist/assets/index-GCqj1Z3R.css   14.00 kB │ gzip:  4.19 kB
dist/assets/index-B6h5fvTx.js   220.20 kB │ gzip: 68.37 kB

✓ built in 126ms
```

- Ran `git diff --check`.
  - Output: no output; command exited successfully.

- Ran focused fresh-context review for match battle reports.
  - Initial verdict: fail. It found the objective count used a sliced preview length and the full match payload was retained in React state.
  - Fixed by storing `objectiveCount` separately from preview objectives and by storing only `getBattleReport(...)` output in `matchIntel.report`.
  - Follow-up review verdict: pass for the match detail state/report fixes.

## What This Shows

- Supports `ticket:20260510-match-battle-reports#ACC-001`: match feed cards select a match and open Battle Report territory in source.
- Supports `ticket:20260510-match-battle-reports#ACC-002`: match detail fetches are on-demand and transformed into a focused report before being stored in React state.
- Supports `ticket:20260510-match-battle-reports#ACC-003`: focused reports include score, teams, duration, league, teamfight/objective counts, scoreboard, and leaders when payload fields are available.

## What This Does Not Show

- Does not prove live browser/API runtime behavior.
- Does not prove visual quality in a browser.
- Does not verify final production app acceptance across all slices.
