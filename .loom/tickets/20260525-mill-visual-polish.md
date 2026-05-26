# Visual Polish: Empty States, Relative Times, Toasts, Micro-Interactions

ID: ticket:20260525-mill-visual-polish
Type: Ticket
Status: active
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - cosmetic improvements across components, no structural changes.
Priority: medium - depends on layout overhaul and log fix.
Depends On: ticket:20260525-mill-layout-overhaul

## Summary

Final polish pass across all components: fix empty states to be helpful (not just "nothing here"), add relative time formatting everywhere, add toast notifications for key events, improve micro-interactions (hover states, transitions), and ensure visual consistency with the Linear-inspired theme.

Closure claim: Every visible surface has intentional empty states, relative times, smooth transitions, and notification toasts for key lifecycle events.

## Related Records

- `ticket:20260525-mill-layout-overhaul` - provides the new component structure to polish
- `loom-mill/frontend/src/app.css` - theme variables
- `loom-mill/frontend/src/lib/` - all components to polish

## Scope

Write:
- `loom-mill/frontend/src/lib/Toast.svelte` (new) - notification toast component
- `loom-mill/frontend/src/lib/utils.ts` (new) - shared utilities: formatDuration, formatRelativeTime, stripAnsi
- Every component touched by layout-overhaul - add polish details below

Non-goals:
- Do NOT add external libraries (no date-fns, no toast library)
- Do NOT implement keyboard shortcuts (separate future ticket)
- Do NOT implement command palette (future)

## Detailed Design

### 1. Utility Functions (`utils.ts`)

```typescript
/** Formats seconds into human-readable duration: "3m 22s", "1h 2m", "45s" */
export function formatDuration(seconds: number): string {
  if (seconds < 60) return `${Math.round(seconds)}s`;
  if (seconds < 3600) {
    const m = Math.floor(seconds / 60);
    const s = Math.round(seconds % 60);
    return s > 0 ? `${m}m ${s}s` : `${m}m`;
  }
  const h = Math.floor(seconds / 3600);
  const m = Math.round((seconds % 3600) / 60);
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

/** Formats ISO timestamp to relative: "2m ago", "just now", "1h ago" */
export function formatRelativeTime(iso: string): string {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000;
  if (diff < 10) return 'just now';
  if (diff < 60) return `${Math.round(diff)}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

/** Formats HH:MM:SS from ISO timestamp */
export function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

/** Strips ANSI escape codes from text */
export function stripAnsi(text: string): string {
  return text.replace(/\x1b\[[0-9;]*[a-zA-Z]/g, '');
}
```

### 2. Empty States (per component)

Each empty state should guide the user, not just say "nothing here":

| Component | Empty State Text | Visual |
|-----------|-----------------|--------|
| WorkstationList | "No workstations running. Start one from the pipeline status bar." | Centered, muted, with a subtle dashed border |
| LogViewer (no workstation selected) | "Select a workstation to view its output." | Centered, muted |
| LogViewer (workstation selected, no logs) | "Waiting for output..." with subtle pulse animation | Centered with loading dots |
| DetailPanel (no selection) | "Select a workstation from the left panel to view details." | Centered with subtle icon |
| Iterations tab (no iterations) | "No iterations recorded yet. Iterations are detected from git commits." | Muted explanatory text |
| AndonBoard (no alerts) | "All clear." (NOT "No active alerts") | Centered, muted, small check icon |
| Changelog (no shipments) | "No tickets shipped this session." | Muted |

### 3. Toast Notifications (`Toast.svelte`)

A toast system for key events. Toasts appear at the bottom-center, auto-dismiss after 4 seconds, max 3 visible.

Events that trigger toasts:
- Workstation started: "▶ Started: {ticket-slug}"
- Workstation completed: "✓ Completed: {ticket-slug} ({duration})"
- SPC alert: "⚠ Alert on {ticket-slug}: {reasoning}" (yellow)
- SPC stop (jidoka): "⛔ Stopped: {ticket-slug} - {reasoning}" (red)
- Merge success: "🔀 Shipped: {ticket-slug} → {branch}"
- Merge conflict: "⚠ Conflict: {ticket-slug}" (red)

Toast design:
```svelte
<div class="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 flex flex-col gap-2 items-center">
  {#each visibleToasts as toast (toast.id)}
    <div class="flex items-center gap-2 rounded-lg border px-4 py-2 shadow-lg
      text-[12px] font-medium backdrop-blur-sm
      {toast.type === 'error' ? 'border-status-error-border bg-status-error-bg/90 text-status-error-text' :
       toast.type === 'warning' ? 'border-status-warning-border bg-status-warning-bg/90 text-status-warning-text' :
       'border-border-default bg-bg-surface-elevated/90 text-text-primary'}
      animate-in slide-in-from-bottom-4 fade-in duration-200">
      <span>{toast.message}</span>
    </div>
  {/each}
</div>
```

### 4. Micro-Interactions

- **WorkstationRow hover**: subtle background elevation (150ms ease)
- **WorkstationRow selection**: left border slides in (not instant)
- **Tab switching**: content fades (100ms opacity transition)
- **Drawer open/close**: slide + backdrop fade (200ms ease-out)
- **Toast enter/exit**: slide up + fade in / fade out (200ms)
- **Status dot for running workstations**: subtle pulse animation (2s infinite)
- **Connection indicator**: ping animation when connected (existing, keep)

CSS for pulse:
```css
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.animate-pulse-dot { animation: pulse-dot 2s ease-in-out infinite; }
```

### 5. Relative Times

Every timestamp in the UI should show relative time with full ISO on hover:

- Workstation "last commit": "2m ago" (title="2026-05-25 14:32:01")
- Log timestamps: "14:32:01" (absolute HH:MM:SS is fine for logs)
- Changelog entries: "5m ago" (title="2026-05-25T14:27:00Z")
- Git commits: "3m ago"

For running workstation durations, show a live counting timer: "Running for 3m 22s" that updates every second.

### 6. Consistent Badge Styles

Status badges should be pill-shaped and muted everywhere:
```css
/* Shared badge base */
.badge {
  @apply inline-flex items-center rounded-full px-1.5 py-0.5 text-[9px] font-medium uppercase tracking-wide;
}
```

Color mapping (muted, not saturated):
- running: green-tinted bg, green text
- paused: amber-tinted bg, amber text
- stopped: red-tinted bg, red text
- completed: gray-tinted bg, gray text
- conflict: red-tinted bg, pulsing

## Acceptance

- ACC-001: All empty states show helpful guidance text (not just "nothing here" or "no data").
  - Evidence: Playwright screenshots of each empty state showing guidance text.
  - Audit: verify each matches the table above.

- ACC-002: All durations display as "3m 22s" format, never raw seconds like "202s" or "395.017s".
  - Evidence: Playwright screenshot with various duration values showing formatted output.
  - Audit: grep codebase for raw seconds display.

- ACC-003: Toast notifications appear for workstation lifecycle events (start, complete, jidoka stop).
  - Evidence: Playwright test triggering events and capturing toast appearance.
  - Audit: verify auto-dismiss after 4s.

- ACC-004: Hover states and transitions are smooth (150ms ease minimum, no instant state changes).
  - Evidence: Playwright visual observation of hover/click interactions.
  - Audit: verify CSS transitions are present on interactive elements.

- ACC-005: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: build output.

## Current State

Blocked on layout overhaul.

## Journal

- 2026-05-25: Created ticket. Source: operator feedback on visual quality and UX details.
