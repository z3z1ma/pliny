# Campaign Production Verification

ID: evidence:20260510-campaign-production-verification
Type: Evidence Observation
Status: recorded
Created: 2026-05-10
Updated: 2026-05-10
Observed: 2026-05-10

## Summary

Observed final production verification checks for the Campaign Map app: Vite production build, Markdown/diff whitespace check, Vite preview smoke, final fresh-context audit, and focused top-bar follow-up review.

## Related Records

- `ticket:20260510-campaign-production-verification` - final verification ticket supported by this evidence.
- `plan:20260510-rts-meta-explorer` - plan-level closure story consuming this evidence.
- `audit:20260510-campaign-production-audit` - fresh-context audit result and finding disposition.

## Procedure And Output

- Ran `npm run build` after the final top-bar mobile fix.
  - Output excerpt:

```text
> ancient-war-room@0.1.0 build
> vite build

vite v8.0.11 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.56 kB │ gzip:  0.35 kB
dist/assets/index-HHygtoD1.css   14.03 kB │ gzip:  4.19 kB
dist/assets/index-D-T8RxAw.js   220.20 kB │ gzip: 68.37 kB

✓ built in 118ms
```

- Ran `git diff --check`.
  - Output: no output; command exited successfully.

- Ran Vite preview smoke on port `4174` and requested `/` with `curl -fsSI`.
  - Output excerpt:

```text
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/html
Cache-Control: no-cache
```

- Ran final fresh-context audit across records, source, and evidence.
  - Verdict: pass with reservations.
  - Findings: missing final verification evidence, missing preview smoke evidence, and mobile top-bar source risk.

- Ran focused follow-up review after fixing mobile top-bar CSS.
  - Verdict: FIND-003 resolved; `.top-bar` collapses to `grid-template-columns: 1fr` at mobile widths.

## What This Shows

- Supports `ticket:20260510-campaign-production-verification#ACC-001`: build, diff, and preview-smoke checks were run and recorded.
- Supports `ticket:20260510-campaign-production-verification#ACC-002`: fresh-context audit reviewed the production Campaign Map against the spec and sliced tickets.
- Supports `ticket:20260510-campaign-production-verification#ACC-003`: unperformed browser visual/runtime/accessibility checks are explicitly recorded as limitations.

## What This Does Not Show

- Does not prove real browser visual quality, responsive rendering, rendered contrast, keyboard traversal, screen-reader behavior, or actual OpenDota browser CORS/runtime behavior.
- Does not characterize OpenDota rate limits or long-term endpoint stability.
- Does not prove production readiness for hosted deployment beyond local Vite build/preview serving.
