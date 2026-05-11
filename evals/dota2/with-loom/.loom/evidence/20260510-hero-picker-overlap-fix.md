# Hero Picker Overlap Fix Checks

ID: evidence:20260510-hero-picker-overlap-fix
Type: Evidence Observation
Status: recorded
Created: 2026-05-10
Updated: 2026-05-10
Observed: 2026-05-10

## Summary

Observed source change and build checks for the Hero Scout overlap fix.

## Related Records

- `ticket:20260510-hero-picker-overlap-fix` - ticket supported by this evidence.

## Procedure And Output

- Changed `src/styles.css` so `.hero-panel` is no longer sticky, the portrait is more compact, and `.roster-panel` can use more viewport height.
- Ran `npm run build`.
  - Output excerpt:

```text
> ancient-war-room@0.1.0 build
> vite build

vite v8.0.11 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.56 kB │ gzip:  0.35 kB
dist/assets/index-ZlyNf4fk.css   14.05 kB │ gzip:  4.20 kB
dist/assets/index-BrJ19QSL.js   220.20 kB │ gzip: 68.37 kB

✓ built in 118ms
```

- Ran `git diff --check`.
  - Output: no output; command exited successfully.

## What This Shows

- Supports `ticket:20260510-hero-picker-overlap-fix#ACC-001`: `.hero-panel` no longer uses sticky positioning in source.
- Supports `ticket:20260510-hero-picker-overlap-fix#ACC-002`: source gives the roster more usable vertical space.
- Supports `ticket:20260510-hero-picker-overlap-fix#ACC-003`: the app still builds after the CSS change.

## What This Does Not Show

- Does not include a fresh browser screenshot after the fix.
