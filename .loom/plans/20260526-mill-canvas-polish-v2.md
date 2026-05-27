# Shaping Canvas Production Polish

ID: plan:20260526-mill-canvas-polish-v2
Type: Plan
Status: open
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - state machine UX changes touch the core interaction loop; canvas theming is visual-only

## Summary

The canvas implementation is functionally complete but has critical UX failures
visible in production use:

1. The canvas background uses Svelvet's default dark theme which is off-brand and
   ugly. Needs proper theming for both dark and light modes.

2. After the AI produces observation nodes (no question), the operator is stuck.
   There's no way to continue, no indication of session state, and no input
   affordance. The session appears frozen with a "Processing..." node that gives
   no real information. This is the primary UX failure.

3. The harness subprocess states are not mapped to the UX. The operator cannot tell
   if the system is: idle waiting for them, actively processing, errored, timed out,
   or finished but has nothing to ask.

## Related Records

- `spec:mill-shaping-canvas` — governing spec
- `plan:20260526-mill-shaping-canvas` — completed canvas plan
- `principle:no-backward-compat-own-stack` — no legacy code maintenance

## Strategy

### Route: UX-First, Then Visual Polish

The state machine UX is the critical fix. An operator who cannot tell what's
happening or how to continue will never use the canvas. Fix that first.

Canvas theming is visual polish — important for feel but not blocking interaction.

### What belongs in this plan

- Session state machine: define ALL states, map each to visible UX
- Persistent input affordance: operator can ALWAYS type and send
- Processing transparency: what's running, how long, cancel/retry
- Error recovery: visible errors with retry actions
- Canvas background theming for dark/light modes

### What is deliberately left out

- New node types or interaction patterns
- Layout algorithm changes
- Position persistence (known deferred item)
- Auto-pan (Svelvet limitation)

## Execution Units

### Unit 1: Session State Machine and Input Affordance

Ticket: ticket:20260526-mill-canvas-state-machine

The core problem: after the AI produces nodes, there's no way for the operator to
continue unless the AI explicitly asked a question. The operator should ALWAYS be
able to send a message, regardless of session state.

**Session states** (visible to operator):
- `idle` — session exists, AI is not processing, operator can type
- `thinking` — harness is running, show what's happening
- `error` — something failed, show what and how to retry
- `complete` — AI has nothing more to say, waiting for operator

**Required UX elements**:
1. A persistent input bar at the bottom of the canvas (like the current chat input
   pattern) — always visible when session is active
2. A session status indicator (top of canvas or in the input bar):
   - "Waiting for you" (idle)
   - "Processing... 5s" (thinking, with elapsed time)
   - "Error: harness timeout. [Retry]" (error, with action)
3. ProcessingNode shows: what harness is running, elapsed time, [Cancel] button
4. When advance finishes without producing a question node, session transitions
   to `idle` and the input bar is focused — the operator can type freely
5. When advance produces a question node, the question node has response affordance
   AND the input bar is available (both work)

**Backend changes**:
- Advance endpoint returns processing state info (started_at timestamp)
- WebSocket event for advance-started and advance-completed
- Error events with structured error info (timeout, parse failure, harness crash)

**Frontend changes**:
- New `CanvasInputBar.svelte` component (persistent at bottom)
- Session state derived from: is advance in flight? did it error? is it idle?
- ProcessingNode shows elapsed time via a reactive timer
- Status indicator component

### Unit 2: Canvas Theme and Background

Ticket: ticket:20260526-mill-canvas-theme

The Svelvet canvas background is off-brand. Need proper theming.

**Dark mode**: Use our `bg-bg-primary` token as the canvas background (the dark
charcoal from our design system, not Svelvet's default grey). The dot grid (if
Svelvet renders one) should use subtle `border-subtle` color dots.

**Light mode**: Use `bg-bg-primary` for light mode too (the tokens switch
automatically). Canvas should look clean and professional in both modes.

**Implementation**:
- Override Svelvet's canvas background via CSS (target `.svelvet-wrapper` or
  Svelvet's `Background` component)
- Ensure node components look correct against both backgrounds
- Edge color should use our `text-text-tertiary` token for subtlety

### Unit 3: Parser Robustness Hardening

Ticket: ticket:20260526-mill-canvas-parser-hardening

Verify and harden the regex-based parser. The parser already uses regex (confirmed),
but needs edge case coverage:

- Verify: no string splitting anywhere in the parse path
- Add test: model outputs partial XML (tag opened but never closed)
- Add test: model outputs nested `<node>` tags (should not nest)
- Add test: model outputs HTML-like content inside record bodies
- Add test: model outputs multiple `<explore>` tags (only first used)
- Verify: the `</node>` inside content fix (from earlier audit) still holds
- Ensure: regex patterns are compiled once (not per-call)

### Unit 4: Close Prior Tickets and Administrative Cleanup

Ticket: ticket:20260526-mill-canvas-admin-cleanup

- All 8 canvas implementation tickets are now closed (done above)
- Remove dead untracked files from repo root (screenshots, logs, patches)
- Verify `.gitignore` covers `.mill/` and common artifacts
- Run `git diff --check` for any trailing whitespace

## Milestones

### Milestone: Operator Can Always Continue

Child tickets: ticket:20260526-mill-canvas-state-machine

When complete: the operator is never stuck. There is always a visible way to send
input, and the system always communicates what it's doing.

### Milestone: Canvas Looks Professional

Child tickets: ticket:20260526-mill-canvas-theme

When complete: dark and light modes both look on-brand with proper backgrounds and
consistent visual language.

## Current State

Plan created. All prior canvas tickets closed. Immediate execution needed.

## Journal

- 2026-05-26: Created plan. Primary UX failure: operator gets stuck after AI
  produces observations. Need persistent input bar and state transparency.
