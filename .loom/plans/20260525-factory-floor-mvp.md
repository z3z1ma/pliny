# Factory Floor MVP

ID: plan:20260525-factory-floor-mvp
Type: Plan
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - new application layer with subprocess management, worktree isolation, and real-time state push; architecture change to a repo that currently ships only a Markdown skill corpus.

## Summary

Build the first Loom Mill product surface: a local Factory Floor application that gives the operator visible, steerable execution over Loom tickets. The Factory Floor watches `.loom/` and git, parses record topology, manages harness subprocesses in isolated worktrees, renders a pipeline/control-room dashboard, and provides pause/steer/resume plus mechanical quality signals.

This needs more than one ticket because the system has distinct layers (parser, watcher, workstation engine, WebSocket API, frontend dashboard, operator controls, inter-iteration processes, quality signals) with clear dependency structure and independent evidence stories.

The plan is complete when an operator can: see their `.loom/` graph state live, configure a harness, select a ticket, start execution in an isolated worktree, watch progress via summaries and pipeline state, see backpressure signals, pause, edit a record, and resume from updated graph state.

## Related Records

- `spec:loom-mill-factory-floor-mvp` - behavior contract this plan implements. All requirements and scenarios are defined there.
- `constitution:main` - Loom/Mill identity, factory principles, constraints.
- `roadmap:loom-mill` - strategic frame: Factory Floor before Design Office.
- `research:20260524-loom-mill-software-factory` - factory architecture synthesis.
- `spec:ticket-owned-worker-handoffs` - worker context model Mill must preserve.
- `spec:loom-driver-agent` - inner-loop coordinator behavior Mill can invoke through harness.

## Strategy

### Code Location

Mill lives at `loom-mill/` in-repo, following the existing monorepo pattern (`loom-core/`, `loom-playbooks/`). Unlike the skill packages, Mill is an application with runtime dependencies. Its `pyproject.toml` owns the Python backend; its `frontend/` subdirectory owns the Svelte app. Extract to a separate repo later if the boundary justifies it.

### Slicing Route: Two Parallel Tracks Converging

The system has two semi-independent tracks that converge at operator controls:

**Track A (visibility):** parser → watcher → WebSocket API → pipeline UI
**Track B (execution):** workstation engine (worktree + subprocess lifecycle)
**Convergence:** controls connect Track A visibility to Track B execution
**Quality layer:** steering, inter-iteration summary, backpressure/andon

After the scaffold (Unit 1), Track A (Units 2-4) and Track B (Unit 5) can proceed in parallel. They converge at Unit 6 (controls). Units 7-9 build on the converged loop.

### Why This Order

1. Scaffold first because everything depends on it.
2. Parser before watcher because the watcher needs to know what changed semantically (new ticket, status change, etc.).
3. Watcher before UI because the UI is just a projection of watcher state.
4. Workstation engine can proceed in parallel with visibility track because it's pure backend (worktree + subprocess) with no UI dependency.
5. Controls after both tracks because they connect visibility to execution.
6. Steering after controls because it's the full pause→edit→resume cycle.
7. Summary and backpressure after workstation because they operate on iteration boundaries.

### Validation Posture

Each ticket should have integration tests or fixture-based evidence. The full end-to-end evidence comes at convergence (Unit 6+). Real harness behavior (OpenCode, Claude, etc.) is separate evidence beyond this plan's scope; this plan uses any configured command including trivial local scripts.

### Loopback Conditions

Replan if:
- The parser approach proves too fragile for real-world records (route to research).
- Worktree isolation breaks with a specific harness (route to research + separate ticket).
- The WebSocket state model doesn't scale to reasonable workspace sizes (route to research).
- The inter-iteration summary model call proves unreliable or too expensive (descope to deterministic summary in MVP).

## Execution Units

### Unit 1: Project Scaffold

Ticket: ticket:20260525-mill-project-scaffold

Create the `loom-mill/` directory with Python backend (pyproject.toml, Starlette app entry, async structure) and Svelte 5 frontend (package.json, vite config, Tailwind, app shell). Dev server runs both with hot reload. No business logic yet. One closure claim: `loom-mill/` builds, dev server starts, and an empty dashboard shell renders.

### Unit 2: Record Parser

Ticket: ticket:20260525-mill-record-parser

Build the `.loom/` record parser that extracts topology: IDs, types, statuses, dates, headings, related-record references, acceptance IDs, requirement IDs, scenario IDs, and surface paths. Input: directory of Markdown files. Output: in-memory state model of the graph topology. One closure claim: given fixture `.loom/` records, the parser extracts correct topology matching expected output.

### Unit 3: File/Git Watcher + State Model

Ticket: ticket:20260525-mill-watcher

Watch `.loom/` and git for changes using watchfiles. On change, re-parse affected records, update in-memory state model, and emit typed events. Include git state: recent commits, current branch, dirty state. One closure claim: file changes in `.loom/` are reflected in state model events within a bounded time.

### Unit 4: Pipeline UI

Ticket: ticket:20260525-mill-pipeline-ui

Svelte frontend receives state via WebSocket, renders ticket pipeline grouped by status (shaped/open → active → review → closed), shows related evidence/audit, shows recent git changes, and updates live. One closure claim: the dashboard renders fixture graph state correctly and updates from WebSocket pushes without full reload.

### Unit 5: Workstation Engine

Ticket: ticket:20260525-mill-workstation-engine

Backend engine that creates a git worktree for a selected ticket, starts a configured harness subprocess in that worktree, captures stdout/stderr and exit status, and tears down on stop. Harness command comes from config. One closure claim: a configured command runs in an isolated worktree and Mill captures its full lifecycle (start, output, exit).

Depends on: Unit 1 only. Can proceed in parallel with Units 2-4.

### Unit 6: Operator Controls + Harness Config

Ticket: ticket:20260525-mill-operator-controls

Connect visibility (pipeline UI) to execution (workstation engine). Add harness configuration surface (command, model, flags). Add start/pause/stop buttons per ticket. Show workstation state (running, paused, stopped, exit code) in the pipeline. One closure claim: operator can configure a harness, select a ticket, start execution, observe workstation state in the dashboard, and pause/stop it.

Depends on: Units 4 + 5.

### Unit 7: Steering Flow

Ticket: ticket:20260525-mill-steering

After pause, the operator can inspect and edit the relevant Loom record (open in editor or minimal inline view), then resume. Resume launches a fresh subprocess from the updated graph, not from stale in-memory state. One closure claim: editing a `.loom/` record between pause and resume changes what the next subprocess iteration sees.

Depends on: Unit 6.

### Unit 8: Inter-Iteration Summary

Ticket: ticket:20260525-mill-iteration-summary

After a subprocess exits or an iteration boundary is detected, Mill runs a lightweight summarization pass (model call via a configured command, or deterministic diff/record-change summary) and surfaces it in the dashboard. Labeled as visibility output, not evidence or acceptance. One closure claim: an iteration boundary produces a labeled summary visible in the Factory Floor dashboard.

Depends on: Units 5 + 4.

### Unit 9: Backpressure + Andon

Ticket: ticket:20260525-mill-backpressure-andon

Detect mechanical patterns: repeated identical failures, long iteration duration, no record change after run, subprocess crash loops. When threshold is reached, raise andon alert in the UI and hold further automatic continuation for that workstation. One closure claim: pattern-matched failure conditions stop the workstation and surface an alert pointing to the relevant ticket, output, and files.

Depends on: Units 5 + 4.

## Milestones

### Milestone: Visible Graph

Child tickets: ticket:20260525-mill-project-scaffold, ticket:20260525-mill-record-parser, ticket:20260525-mill-watcher, ticket:20260525-mill-pipeline-ui

What becomes true: the operator can open Mill and see their `.loom/` graph state rendered as a live pipeline dashboard. No execution yet, but the "control room screens are on."

### Milestone: Core Factory Loop

Child tickets: ticket:20260525-mill-workstation-engine, ticket:20260525-mill-operator-controls, ticket:20260525-mill-steering

What becomes true: the operator can select a ticket, start a harness, watch it run, pause, edit a record, and resume. The factory line runs under operator control.

### Milestone: Quality Signals

Child tickets: ticket:20260525-mill-iteration-summary, ticket:20260525-mill-backpressure-andon

What becomes true: the operator gets automatic summaries between iterations and mechanical alerts when the line is stuck or looping. The factory detects its own defects.

## Current State

Plan created with nine child tickets spanning three milestones. No execution has started. The first parallel work is Units 1 (scaffold), which unblocks both tracks. After scaffold, Units 2-4 (visibility track) and Unit 5 (execution track) can proceed in parallel.

## Journal

- 2026-05-25: Created plan from `spec:loom-mill-factory-floor-mvp` with all blocking open questions resolved. Nine execution units, three milestones, two parallel tracks converging at operator controls.
