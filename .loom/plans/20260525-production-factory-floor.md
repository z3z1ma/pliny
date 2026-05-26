# Production Factory Floor

ID: plan:20260525-production-factory-floor
Type: Plan
Status: completed
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - significant backend concurrency work (N workstations, worktree management, subprocess multiplexing) plus LLM integration for SPC. Mitigated by: MVP architecture is sound, each unit is independently testable, and the work is additive to existing code.

## Summary

Take the Factory Floor from MVP (single workstation, basic pipeline, simple controls) to production: N concurrent workstations, full observability (logs, diffs, playback), autonomous scheduling, LLM-backed process control with jidoka, configurable merge workflow, and a control room frontend that makes parallel execution legible and steerable.

This is the second leg of Loom Mill development. When complete, an operator can shape 10 tickets, configure the factory, and walk away. The factory pulls work, builds it in parallel, detects and stops on defects, and ships finished goods to the configured branch. The operator sees everything from the control room.

## Related Records

- `spec:mill-factory-floor` - behavior contract for the control room and workstation engine
- `spec:mill-scheduling-agent` - behavior contract for autonomous work selection
- `spec:mill-process-control` - behavior contract for SPC and jidoka
- `spec:mill-shipping-dock` - behavior contract for merge workflow
- `plan:20260525-factory-floor-mvp` - completed predecessor plan (MVP)
- `constitution:main` - factory principles (pull, WIP, jidoka, single-piece flow)
- `research:20260524-loom-mill-software-factory` - factory architecture research

## Strategy

**Route: foundation → observability → intelligence → integration**

The MVP proved single-workstation execution works. This plan deepens it in layers:

1. **Foundation**: Multi-workstation engine. The current engine manages one worktree/subprocess. Generalize to N concurrent, with multiplexed WebSocket events and WIP enforcement. Everything else builds on this.

2. **Observability**: Log streaming and iteration history. These are the data layer that SPC, diffs, playback, and metrics all consume. Build them before the consumers.

3. **Intelligence**: SPC/jidoka and scheduling agent. These are autonomous processes that read observability data and make decisions. They can be built and tested independently.

4. **Shipping**: Merge workflow. Needs the workstation lifecycle to know "done" and the scheduling agent to know "capacity freed."

5. **Frontend integration**: Update the UI to render all the new backend state. Split into three focused passes: workstation panels + logs, diffs + playback, and pipeline/andon/metrics/changelog.

**Why this order**: Each layer is independently testable and useful. Multi-workstation without SPC is still better than single workstation. Log streaming without playback is still useful live. Scheduling without shipping still reduces manual work.

**Recovery**: If SPC model integration proves problematic, the deterministic fallback rules still provide value. If merge conflicts with parallel worktrees are too complex, fall back to sequential merge ordering. Each unit can stop cleanly without blocking the others.

**Validation posture**: Each unit has backend tests (pytest). Frontend units verified with `npm run build` + Playwright screenshots. SPC tested with fixture iteration histories. Scheduling tested with fixture ticket graphs. Shipping tested with mock git repos.

## Execution Units

### Unit 1: Multi-Workstation Engine

Ticket: ticket:20260525-mill-multi-workstation

Generalize the workstation engine from 1 to N concurrent. Each workstation gets a stable ID, owns one worktree + subprocess + event stream. WebSocket protocol gains workstation_id multiplexing. WIP limit enforcement blocks new starts when at capacity.

Cites: `spec:mill-factory-floor` REQ-001, REQ-002, REQ-009, REQ-015, REQ-017, REQ-018

Dependencies: none (builds on existing MVP code)
Evidence: pytest - N concurrent workstations with mock harness, WIP blocking, multiplexed WebSocket messages.
Stop: if asyncio subprocess management at scale reveals fundamental issues with the current architecture.

### Unit 2: Log Streaming

Ticket: ticket:20260525-mill-log-streaming

Pipe full stdout/stderr from each harness subprocess to WebSocket in real-time, tagged by workstation ID. Stream without buffering entire output in memory. Older entries can be truncated from the live stream (full logs persist in `.mill/`).

Cites: `spec:mill-factory-floor` REQ-003, REQ-015

Dependencies: Unit 1 (needs multi-workstation)
Evidence: pytest - subprocess output arrives at WebSocket client within 1s, correctly tagged, no cross-workstation contamination.
Stop: if streaming volume is unmanageable (signal for buffering/sampling strategy).

### Unit 3: Iteration History + Persistence

Ticket: ticket:20260525-mill-iteration-history

Detect iteration boundaries (git commit on worktree branch, subprocess exit). Record per-iteration: start/end time, duration, git diff stat, files changed, exit code, commit SHA. Persist in `.mill/workstations/{id}/iterations/{n}.json`. Provide API for random-access retrieval.

Cites: `spec:mill-factory-floor` REQ-004, REQ-005, REQ-008, REQ-017

Dependencies: Unit 1 (needs multi-workstation)
Evidence: pytest - commit detection creates iteration records, metadata is correct, diff is captured, takt duration is tracked.
Stop: if git diff capture at iteration speed introduces race conditions with the harness subprocess.

### Unit 4: SPC + Jidoka

Ticket: ticket:20260525-mill-spc-jidoka

Implement the inter-iteration SPC pass. After each iteration: collect structured summary from iteration history, send to configured SPC model, receive continue/alert/stop signal. On `stop`: halt workstation (jidoka). Deterministic fallback rules for when model is unavailable. Configurable thresholds and model.

Cites: `spec:mill-process-control` REQ-001 through REQ-011

Dependencies: Unit 3 (needs iteration history data)
Evidence: pytest - fixture iteration histories trigger correct signals. Repetition detection works. Timeout triggers fallback. Jidoka halts workstation on stop signal.
Stop: if LLM response quality for structured pattern detection is too unreliable (fall back to rules-only).

### Unit 5: Scheduling Agent

Ticket: ticket:20260525-mill-scheduling-agent

Implement pull-based scheduling. On workstation completion + WIP capacity: scan ready tickets, resolve dependencies, apply priority ordering, consult LLM advisory for heijunka, pull top candidate. Configurable ready statuses, disable toggle, operator overrides (pin/exclude).

Cites: `spec:mill-scheduling-agent` REQ-001 through REQ-009

Dependencies: Unit 1 (needs multi-workstation lifecycle events)
Evidence: pytest - fixture ticket graphs produce correct ordering. Dependencies block correctly. Heijunka advisory input/output format works with mock LLM. Disabled mode prevents auto-pull.
Stop: if dependency resolution from Related Records references is too ambiguous to be reliable.

### Unit 6: Shipping Dock

Ticket: ticket:20260525-mill-shipping-dock

Implement merge workflow. Two modes: auto-merge and operator-approved. Configurable target branch (per-factory default + per-ticket override). Merge with `--no-ff`. Conflict detection triggers jidoka. Worktree cleanup after merge. Notify scheduler of freed capacity.

Cites: `spec:mill-shipping-dock` REQ-001 through REQ-011

Dependencies: Unit 1 (needs workstation lifecycle)
Evidence: pytest - mock git repo shows merge creates correct commit on target branch. Conflicts trigger conflict state. Sequential merges include prior changes. Skip/abort work correctly.
Stop: if parallel worktree merging reveals git-level issues that need architectural change.

### Unit 7: Frontend - Workstation Panels + Log Streaming

Ticket: ticket:20260525-mill-frontend-workstations

Update the frontend to render N workstation panels simultaneously. Each panel shows: ticket ID, iteration number, status, takt indicator, last commit time, controls (pause/stop/view). Add log panel per workstation showing streamed output. Handle WebSocket multiplexing on the client side.

Cites: `spec:mill-factory-floor` REQ-011, REQ-016

Dependencies: Units 1 + 2 (needs backend multi-workstation + log streaming)
Evidence: `npm run build` passes. Playwright screenshot showing multiple workstation panels with distinct log streams.
Stop: if rendering N log streams simultaneously causes performance issues (signal for virtualization approach).

### Unit 8: Frontend - Diff Viewer + Playback

Ticket: ticket:20260525-mill-frontend-diffs-playback

Add diff viewer component: per-iteration diff (syntax highlighted) and aggregate diff. Add playback: step through completed iterations of any workstation, showing diff + duration + SPC signals at each step. Timeline/scrubber UI.

Cites: `spec:mill-factory-floor` REQ-006, REQ-007

Dependencies: Unit 3 (needs iteration history API)
Evidence: `npm run build` passes. Playwright screenshot showing diff viewer with syntax highlighting. Playback stepping through iterations.
Stop: if large diffs make rendering impractical (signal for diff summarization).

### Unit 9: Frontend - Pipeline + Andon + Metrics + Changelog

Ticket: ticket:20260525-mill-frontend-pipeline-complete

Update pipeline to show all lifecycle stages (shaped → executing → evidence → audit → shipping → closed). Add andon board aggregating SPC stops/alerts with links to workstations. Add quality metrics panel (iterations/ticket, avg duration, rework count, completion rate). Add changelog view (tickets shipped this session with summary diffs).

Cites: `spec:mill-factory-floor` REQ-010, REQ-012, REQ-013, REQ-014

Dependencies: Units 4 + 5 + 6 (needs SPC signals, scheduling state, shipping events)
Evidence: `npm run build` passes. Playwright screenshots showing: full pipeline with all stages, andon board with alerts, metrics panel, changelog.
Stop: if the number of signals overwhelms the UI (signal for filtering/aggregation strategy).

## Milestones

### Milestone: Multi-Workstation Foundation

Child tickets: ticket:20260525-mill-multi-workstation, ticket:20260525-mill-log-streaming, ticket:20260525-mill-iteration-history

What becomes true: N workstations can run concurrently with full observability (logs + iteration tracking). The factory can execute in parallel even without intelligence or shipping. Manual start/stop still required.

### Milestone: Autonomous Factory

Child tickets: ticket:20260525-mill-spc-jidoka, ticket:20260525-mill-scheduling-agent, ticket:20260525-mill-shipping-dock

What becomes true: The factory runs itself. Work is pulled automatically, quality is monitored between iterations, defects stop the line, and finished goods merge to the target branch. The operator can walk away.

### Milestone: Production Control Room

Child tickets: ticket:20260525-mill-frontend-workstations, ticket:20260525-mill-frontend-diffs-playback, ticket:20260525-mill-frontend-pipeline-complete

What becomes true: The operator sees everything. N workstations live, diffs per iteration, playback for review, andon board for alerts, metrics for quality trends, changelog for output. The control room is production-ready.

## Current State

All 9 execution units completed and shipped. 46 backend tests passing. Frontend builds successfully (94.82 kB JS, 25.58 kB CSS). All 3 milestones satisfied.

## Journal

Append material updates at the bottom. Record plan creation, child ticket creation,
strategy changes, milestone movement, blockers, review, completion, and
cancellation.

- 2026-05-25: Created plan with 9 execution units across 3 milestones. Strategy: foundation → observability → intelligence → integration. Specs: `spec:mill-factory-floor`, `spec:mill-scheduling-agent`, `spec:mill-process-control`, `spec:mill-shipping-dock` all active.
- 2026-05-25: Unit 1 (multi-workstation) completed. 23 tests passing.
- 2026-05-25: Units 2, 3, 5, 6 completed in parallel. Log streaming, iteration history, scheduling agent, shipping dock all shipped. 42 tests passing.
- 2026-05-25: Units 7, 8 (frontend workstations + diffs/playback) completed in parallel.
- 2026-05-25: Unit 4 (SPC + jidoka) completed. 46 tests passing.
- 2026-05-25: Unit 9 (frontend pipeline + andon + metrics + changelog) completed. All milestones satisfied. Plan completed.
