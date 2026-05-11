# Campaign Map Shell Checks

ID: evidence:20260510-campaign-map-shell-checks
Type: Evidence Observation
Status: recorded
Created: 2026-05-10
Updated: 2026-05-10
Observed: 2026-05-10

## Summary

Observed build output and focused reviews for the Campaign Map shell slice.

## Related Records

- `ticket:20260510-campaign-map-shell` - shell ticket supported by this evidence.
- `spec:opendota-rts-meta-explorer` - Campaign Map behavior and quality bar.

## Procedure And Output

- Ran `npm run build` after shell CSS fixes.
  - Output excerpt:

```text
> ancient-war-room@0.1.0 build
> vite build

vite v8.0.11 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.56 kB │ gzip:  0.35 kB
dist/assets/index-GCqj1Z3R.css   14.00 kB │ gzip:  4.19 kB
dist/assets/index-D9MzXRrb.js   219.99 kB │ gzip: 68.29 kB

✓ built in 93ms
```

- Ran `git diff --check`.
  - Output: no output; command exited successfully.

- Ran focused fresh-context shell review.
  - Initial verdict: pass with reservations. It found two low source-level issues: ineffective mobile stacking for flex header rows and possible clipped focus outlines for edge map nodes.
  - Fixed mobile stacking by using `flex-direction: column` for `.territory-heading` and `.battle-report-hero` at mobile widths.
  - Fixed narrow-screen focus clipping by clamping mobile `.territory-node` centers with enough inset for the global focus outline.
  - Follow-up review verdict: pass for the focus clipping concern.

## What This Shows

- Supports `ticket:20260510-campaign-map-shell#ACC-001`: source renders a named Campaign Map with territory buttons rather than a table/dashboard shell.
- Supports `ticket:20260510-campaign-map-shell#ACC-002`: territory controls are buttons with active state and source-level protected focus visibility.
- Supports `ticket:20260510-campaign-map-shell#ACC-003`: source-level responsive stacking issues found by review were fixed.

## What This Does Not Show

- Does not prove real browser visual quality, rendered contrast, or actual viewport behavior.
- Does not verify hero deep analytics or match battle report behavior.
