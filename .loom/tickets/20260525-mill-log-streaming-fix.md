# Log Streaming Fix + Harness Verification

ID: ticket:20260525-mill-log-streaming-fix
Type: Ticket
Status: closed
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - requires investigating how `opencode run` writes to stdout/stderr when piped; may need PTY workaround.
Priority: high - core visibility feature is broken in production.

## Summary

The log streaming system was built and tested with mock subprocesses but has never been verified with a real harness (`opencode run`). The operator reports "No logs available" when running a real workstation. Investigate why, fix the streaming, and verify with Playwright that real harness output appears in the log viewer.

Additionally, the `LogViewer` has a data shape mismatch: the WebSocket store pushes objects with `{stream, line, timestamp}` fields (from the backend `OutputEvent`), but the LogViewer template renders `{log.data}` which doesn't exist on the payload. The field should be `log.line`.

Closure claim: Real harness output (from `opencode run` or any configured command) streams live into the LogViewer in the frontend, verified end-to-end with Playwright.

## Related Records

- `spec:mill-factory-floor` REQ-003 - full stdout/stderr streaming per workstation
- `loom-mill/src/loom_mill/workstation/engine.py:191-209` - _capture_stream implementation
- `loom-mill/src/loom_mill/workstation/manager.py:128-136` - _pump_output
- `loom-mill/frontend/src/lib/LogViewer.svelte` - frontend display (line 43: `{log.data}` is wrong)
- `loom-mill/frontend/src/lib/ws.svelte.ts:60-68` - WebSocket store log handling

## Scope

Write:
- `loom-mill/frontend/src/lib/LogViewer.svelte` - fix data access (`log.data` → `log.line`), add timestamps in margin, add ANSI color stripping
- `loom-mill/frontend/src/lib/ws.svelte.ts` - verify log event payload shape matches backend
- `loom-mill/frontend/src/lib/types.ts` - fix OutputEvent type to match backend shape: `{stream: string, line: string, timestamp: string}`
- `loom-mill/src/loom_mill/workstation/engine.py` - if needed: add `--no-color` or `script` wrapper for PTY-dependent commands
- `loom-mill/tests/test_log_streaming_real.py` (optional) - integration test with a real command like `echo`

Non-goals:
- Do NOT redesign the LogViewer layout (that's the layout-overhaul ticket)
- Do NOT implement log search/filtering
- Do NOT implement ANSI color rendering (just strip ANSI codes for now)

## Root Cause Analysis

The backend `_capture_stream` in `engine.py:191-209` reads from `asyncio.StreamReader` line-by-line and puts `OutputEvent(stream=stream, line=text, timestamp=timestamp)` on the queue. The manager's `_pump_output` publishes it as `WorkstationOutput`.

In `ws.svelte.ts:60-68`, the store pushes `payload` directly into `workstations[id].output`. The payload from the WebSocket is: `{"workstation_id": "...", "event": "log", "payload": {"stream": "stdout", "line": "hello", "timestamp": "..."}}`.

But in `LogViewer.svelte:43`, the template renders `{log.data}` - this field doesn't exist on the payload. It should be `{log.line}`.

**This is bug #1: template accesses wrong field.**

**Bug #2** (potential): When `opencode run` is executed with `stdout=PIPE`, it may detect it's not a TTY and either:
- Buffer output (no line-by-line streaming until buffer fills)
- Suppress interactive output entirely
- Use a different output format

To verify: run `opencode run --help` or a simple command through the subprocess pipe and check if output actually reaches the StreamReader.

## Detailed Fix

### 1. Fix OutputEvent type (`types.ts`)

Change:
```typescript
export interface OutputEvent {
  stream: string;
  data: string;
}
```

To:
```typescript
export interface OutputEvent {
  stream: 'stdout' | 'stderr';
  line: string;
  timestamp: string;
}
```

### 2. Fix LogViewer template (`LogViewer.svelte`)

Change line 43 from:
```svelte
{log.data}
```
To:
```svelte
{log.line}
```

Also add a timestamp margin:
```svelte
{#each logs as log}
  <div class="flex gap-2 whitespace-pre-wrap break-words {log.stream === 'stderr' ? 'text-status-warning-text' : 'text-text-secondary'}">
    <span class="shrink-0 text-text-tertiary select-none w-16">{formatTime(log.timestamp)}</span>
    <span class="flex-1">{stripAnsi(log.line)}</span>
  </div>
{/each}
```

Where `formatTime` shows `HH:MM:SS` and `stripAnsi` removes ANSI escape codes: `text.replace(/\x1b\[[0-9;]*m/g, '')`.

### 3. Verify subprocess capture works with real commands

Start the Mill backend, create a workstation with harness command `["echo", "hello world"]`, and verify the log appears in the WebSocket stream. If it does, the fix is just the frontend field name.

If `opencode run` specifically doesn't output to piped stdout:
- Try adding `--no-color` or `--plain` flag
- Try wrapping with `script -q /dev/null` (macOS) or `unbuffer` to allocate a PTY
- Document the required harness flags in the config UI

### 4. Add "Harness Test" button (bonus, small)

In the HarnessConfig component, add a "Test" button that:
1. POSTs to a new backend endpoint `POST /harness/test`
2. Backend runs the configured command with `["--version"]` or `["--help"]` (just the first arg that produces output)
3. Returns the first 5 lines of stdout or an error message
4. Frontend shows result inline: "✓ opencode v1.2.3" or "✗ command not found"

## Acceptance

- ACC-001: LogViewer renders log lines from real subprocess output. The `{log.data}` → `{log.line}` bug is fixed.
  - Evidence: Playwright test starting backend, creating a workstation with `["echo", "hello from harness"]`, verifying "hello from harness" appears in the log viewer.
  - Audit: verify types.ts, LogViewer.svelte, and ws.svelte.ts all use consistent field names.

- ACC-002: OutputEvent type matches backend shape: `{stream, line, timestamp}`.
  - Evidence: TypeScript compilation passes. No runtime property-access errors.
  - Audit: diff showing type fix.

- ACC-003: Timestamps appear in the log margin as HH:MM:SS.
  - Evidence: Playwright screenshot showing timestamps next to log lines.
  - Audit: verify format is concise and doesn't take too much width.

- ACC-004: ANSI escape codes are stripped (no garbage characters in log output).
  - Evidence: test with colored output command showing clean text.
  - Audit: verify regex strips common ANSI sequences.

- ACC-005: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: build output.
  - Audit: no type errors.

## Current State

Ready to start. This is a critical bug fix - the log viewer has never worked with real output due to a field name mismatch.

## Journal

- 2026-05-25: Created ticket. Root cause identified: `LogViewer.svelte` renders `log.data` but backend sends `log.line`. Secondary concern: real harness commands may not flush to piped stdout.
