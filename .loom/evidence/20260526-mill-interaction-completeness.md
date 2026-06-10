# Evidence: Mill Interaction Completeness

Status: verified
Created: 2026-05-26
Updated: 2026-05-26

## Observation

All acceptance criteria have been verified.

- **ACC-001**: AndonBoard "View Workstation" button selects that workstation in the left panel and shows its detail. The `open-playback` event is now dispatched with `source: 'andon'` and handled in `App.svelte` to set the active tab to `logs` and close the settings drawer.
- **ACC-002**: WorkstationControls "View History" switches to iterations tab. The `open-playback` event is dispatched with `source: 'controls'` and handled in `App.svelte` to set the active tab to `iterations`.
- **ACC-003**: All fetch calls handle errors without wedging loading state. `try/catch/finally` blocks have been added to `WorkstationControls`, `HarnessConfig`, `IterationsTab`, `Playback`, `ReadyTicketRow`, `WorkstationRow`, and `AndonBoard`. Errors are displayed inline and clear after 5 seconds.
- **ACC-004**: Connection banner appears within 2 seconds of WebSocket disconnect. Verified via Playwright screenshot `ui-disconnected.png`.
- **ACC-005**: Connection banner shows "Connection lost" with retry button after max retries. The banner logic correctly handles the `store.error` state.
- **ACC-006**: Andon "Clear resolved" properly updates store state. It now calls `store.clearAndonEvents` instead of mutating a local array.

## Artifacts

- `.storage/20260526-mill-interaction-completeness/ui-loaded.png` - UI loaded correctly
- `.storage/20260526-mill-interaction-completeness/ui-disconnected.png` - Connection banner visible when backend killed
- `.storage/20260526-mill-interaction-completeness/ui-reconnected.png` - Connection banner disappears when backend restarted
