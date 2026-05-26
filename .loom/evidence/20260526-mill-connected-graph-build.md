# Mill Connected Graph Build

ID: evidence:20260526-mill-connected-graph-build
Type: Evidence Observation
Status: recorded
Created: 2026-05-26
Updated: 2026-05-26
Observed: 2026-05-26

## Summary

Frontend production build was run after adding the connected-record graph view for
`ticket:20260526-mill-graph-connected`.

## Observation

Procedure: ran `npm --prefix loom-mill/frontend run build` from the repository
root after installing `d3-force` and adding the graph component.

Observed result: Vite completed successfully and produced `dist/index.html`, CSS,
and JS assets. The run emitted pre-existing Svelte deprecation/accessibility
warnings in chat components and a chunk-size warning, but did not fail.

## Artifacts

- Command excerpt: `✓ 208 modules transformed.` and `✓ built in 1.97s`.
- Command excerpt: output included warnings in `src/lib/design/ChatPanel.svelte`,
  `src/lib/design/ChatInput.svelte`, and `src/lib/design/ChatMessage.svelte`.

## What This Shows

- `ticket:20260526-mill-graph-connected#ACC-004` - supports - the frontend build
  completed successfully after the graph implementation.

## What This Does Not Show

This evidence does not show browser-rendered visual quality, click navigation in a
live UI, or readability with 5-20 nodes. Those need manual UI verification or a
separate review pass. Recheck if frontend source, dependency versions, or build
configuration changes.

## Related Records

- `ticket:20260526-mill-graph-connected` - ticket whose build acceptance this
  observation supports.
