# Mill DAG Graph Build

ID: evidence:20260526-mill-graph-dag-build
Type: Evidence Observation
Status: recorded
Created: 2026-05-26
Updated: 2026-05-26
Observed: 2026-05-26

## Summary

Observed the Loom Mill frontend production build after adding hierarchy mode to the
Design Room graph component.

## Observation

Procedure: ran `npm --prefix loom-mill/frontend run build` from the repository root
after editing `loom-mill/frontend/src/lib/design/GraphView.svelte`.

Observed result: Vite transformed 208 modules and completed the production build
successfully. The build emitted pre-existing Svelte deprecation and accessibility
warnings in `ChatPanel.svelte`, `ChatMessage.svelte`, and `ChatInput.svelte`, plus
the existing chunk-size warning. No build error was observed.

## Artifacts

- Command: `npm --prefix loom-mill/frontend run build` - exited successfully.
- Build excerpt: `✓ 208 modules transformed.` and `✓ built in 2.05s`.

## What This Shows

- ticket:20260526-mill-graph-dag#ACC-005 - supports - the frontend production build passes after the DAG graph changes.

## What This Does Not Show

This evidence does not prove manual visual acceptance for hierarchy layout,
click-to-navigate behavior, current-record highlighting, or edge semantics in a
running browser. Those require UI inspection or audit.

## Related Records

- ticket:20260526-mill-graph-dag - consuming ticket for the DAG hierarchy graph.
- loom-mill/frontend/src/lib/design/GraphView.svelte - source file changed for the observation.
