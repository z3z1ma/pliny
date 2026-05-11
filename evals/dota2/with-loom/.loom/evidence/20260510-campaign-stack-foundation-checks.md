# Campaign Stack Foundation Checks

ID: evidence:20260510-campaign-stack-foundation-checks
Type: Evidence Observation
Status: recorded
Created: 2026-05-10
Updated: 2026-05-10
Observed: 2026-05-10

## Summary

Observed dependency installation, production build, and whitespace checks for the Campaign Map frontend stack foundation.

## Related Records

- `ticket:20260510-campaign-stack-foundation` - stack foundation ticket supported by this evidence.
- `plan:20260510-rts-meta-explorer` - plan consuming this first production slice.

## Procedure And Output

- Ran `npm install` in `/Users/alexanderbutler/code_projects/personal/agent-loom/evals/dota2/with-loom`.
  - Output excerpt:

```text
added 21 packages, and audited 22 packages in 9s
found 0 vulnerabilities
```

- Ran `npm run build` in `/Users/alexanderbutler/code_projects/personal/agent-loom/evals/dota2/with-loom`.
  - Output excerpt:

```text
> ancient-war-room@0.1.0 build
> vite build

vite v8.0.11 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.56 kB │ gzip:  0.35 kB
dist/assets/index-ex-vR8vM.css   13.92 kB │ gzip:  4.16 kB
dist/assets/index-CrvN-TzI.js   219.70 kB │ gzip: 68.21 kB

✓ built in 281ms
```

- Ran `git diff --check`.
  - Output: no output; command exited successfully.

## What This Shows

- Supports `ticket:20260510-campaign-stack-foundation#ACC-001`: dependencies installed successfully and reported zero vulnerabilities.
- Supports `ticket:20260510-campaign-stack-foundation#ACC-002`: Vite production build succeeded.
- Supports the stack-level part of `ticket:20260510-campaign-stack-foundation#ACC-003`: package scripts are executable and documented in `README.md`.

## What This Does Not Show

- Does not prove Campaign Map product quality, OpenDota runtime behavior, browser rendering, or accessibility behavior.
- Does not verify later data, map shell, hero deep analytics, or match battle report tickets.
