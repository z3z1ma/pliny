# Settings Drawer + Harness Smoke Test

ID: ticket:20260525-mill-settings-drawer
Type: Ticket
Status: active
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - moving existing components into a slide-out drawer; adding one small backend endpoint.
Priority: medium - depends on layout overhaul.
Depends On: ticket:20260525-mill-layout-overhaul

## Summary

Move HarnessConfig, GitPanel, quality Metrics, and Changelog out of the always-visible sidebar into a settings/info drawer that slides out from the right when the gear icon in the header is clicked. Add a "Test Harness" button that runs a quick smoke test of the configured command.

The current sidebar is a dumping ground where "No tickets shipped yet" overlaps Harness Configuration and everything fights for 320px of vertical space. This ticket fixes that by making these panels on-demand.

Closure claim: Configuration and info panels live in a slide-out drawer (not always visible), with a working "Test Harness" button that verifies the configured command runs successfully.

## Related Records

- `ticket:20260525-mill-layout-overhaul` - removes the sidebar; this ticket provides the replacement
- `loom-mill/frontend/src/lib/HarnessConfig.svelte` - existing component to move
- `loom-mill/frontend/src/lib/GitPanel.svelte` - existing component to move
- `loom-mill/frontend/src/lib/Metrics.svelte` - existing component to move
- `loom-mill/frontend/src/lib/Changelog.svelte` - existing component to move
- `loom-mill/frontend/src/lib/AndonBoard.svelte` - existing component to move

## Scope

Write:
- `loom-mill/frontend/src/lib/SettingsDrawer.svelte` (new) - slide-out right panel with tabs
- `loom-mill/frontend/src/lib/HarnessConfig.svelte` - add "Test Harness" button + result display
- `loom-mill/frontend/src/App.svelte` - gear icon in header opens/closes drawer
- `loom-mill/src/loom_mill/api/workstation.py` - add `POST /harness/test` endpoint

Backend endpoint design:
```python
@app.route("/harness/test", methods=["POST"])
async def test_harness(request):
    # Run configured command with --version or --help
    # Capture first 10 lines of stdout within 5 second timeout
    # Return {"success": true, "output": "opencode v1.2.3\n..."} 
    # or {"success": false, "error": "command not found"}
```

Non-goals:
- Do NOT redesign HarnessConfig internal layout (just move it)
- Do NOT implement per-workstation config override UI
- Do NOT implement config import/export

## Detailed Design

### SettingsDrawer.svelte

A slide-out panel from the right edge of the screen. Overlay with backdrop. Tabbed internally.

```svelte
<div class="fixed inset-0 z-50 {open ? '' : 'pointer-events-none'}">
  <!-- Backdrop -->
  <div class="absolute inset-0 bg-black/30 transition-opacity {open ? 'opacity-100' : 'opacity-0'}"
    onclick={close}></div>
  
  <!-- Drawer -->
  <div class="absolute right-0 top-0 h-full w-[400px] bg-bg-surface border-l border-border-default
    transform transition-transform {open ? 'translate-x-0' : 'translate-x-full'}">
    
    <!-- Header -->
    <div class="flex items-center justify-between px-4 py-3 border-b border-border-default">
      <h2 class="text-[13px] font-semibold text-text-primary">Settings & Info</h2>
      <button onclick={close} class="text-text-tertiary hover:text-text-primary">✕</button>
    </div>
    
    <!-- Tabs -->
    <div class="flex border-b border-border-default">
      <button class="px-4 py-2 text-[11px] ...">Harness</button>
      <button class="px-4 py-2 text-[11px] ...">Metrics</button>
      <button class="px-4 py-2 text-[11px] ...">Alerts</button>
      <button class="px-4 py-2 text-[11px] ...">Git</button>
    </div>
    
    <!-- Content -->
    <div class="flex-1 overflow-y-auto p-4">
      {#if tab === 'harness'}
        <HarnessConfig />
      {:else if tab === 'metrics'}
        <Metrics ... />
        <Changelog ... />
      {:else if tab === 'alerts'}
        <AndonBoard ... />
      {:else if tab === 'git'}
        <GitPanel ... />
      {/if}
    </div>
  </div>
</div>
```

### "Test Harness" Button in HarnessConfig

Below the command/args/env fields, add:

```svelte
<div class="mt-3 pt-3 border-t border-border-subtle">
  <button 
    onclick={testHarness}
    disabled={testing}
    class="flex items-center gap-2 px-3 py-1.5 rounded text-[11px] font-medium
      bg-bg-surface-active border border-border-default text-text-secondary
      hover:bg-bg-surface-elevated hover:text-text-primary transition-colors">
    {#if testing}
      <span class="animate-spin">↻</span> Testing...
    {:else}
      ▶ Test Harness
    {/if}
  </button>
  
  {#if testResult}
    <div class="mt-2 rounded border p-2 font-mono text-[10px] leading-relaxed
      {testResult.success ? 'border-status-success-border bg-status-success-bg text-status-success-text' : 
                           'border-status-error-border bg-status-error-bg text-status-error-text'}">
      {testResult.success ? '✓ ' : '✗ '}{testResult.output || testResult.error}
    </div>
  {/if}
</div>
```

The test calls `POST /harness/test` which runs the configured harness command with `["--version"]` appended to args, captures stdout for up to 5 seconds, and returns the result.

### Header Integration

In App.svelte header, the gear icon:

```svelte
<button 
  onclick={() => settingsOpen = !settingsOpen}
  class="p-1 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary transition-colors"
  title="Settings & Info">
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
</button>
```

When andon alerts are active, show a red badge on the gear icon:

```svelte
{#if andonCount > 0}
  <span class="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-status-error-text"></span>
{/if}
```

## Acceptance

- ACC-001: Gear icon in header opens a slide-out drawer from the right with tabs: Harness, Metrics, Alerts, Git.
  - Evidence: Playwright screenshot showing drawer open with tabs visible.
  - Audit: verify slide animation works, backdrop closes drawer.

- ACC-002: All former sidebar content (HarnessConfig, Metrics, Changelog, AndonBoard, GitPanel) renders correctly inside the drawer tabs.
  - Evidence: Playwright screenshots of each tab showing content without overflow/clipping issues.
  - Audit: verify no content is lost vs. previous sidebar.

- ACC-003: "Test Harness" button runs the configured command and shows success/failure result.
  - Evidence: Playwright test clicking "Test Harness" with `echo` as command, verifying "✓" result appears.
  - Audit: verify 5-second timeout works, error handling works for bad commands.

- ACC-004: The old sidebar is completely removed from the layout.
  - Evidence: Playwright full-page screenshot showing no right sidebar.
  - Audit: verify App.svelte no longer renders `<aside>`.

- ACC-005: `npm --prefix loom-mill/frontend run build` and `python -m pytest loom-mill/tests/ -q` both pass.
  - Evidence: build + test output.

## Current State

Blocked on layout overhaul.

## Journal

- 2026-05-25: Created ticket. Source: operator feedback about sidebar being a dumping ground with visual overflow bugs.
