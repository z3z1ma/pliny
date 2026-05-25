# Loom Mill Factory Floor MVP

ID: spec:loom-mill-factory-floor-mvp
Type: Spec
Status: draft
Created: 2026-05-25
Updated: 2026-05-25

## Summary

This spec defines the first Loom Mill product slice: the Factory Floor MVP. The Factory Floor is the execution/control-room mode of Loom Mill. It gives the operator visible, steerable execution over Loom tickets while preserving `.loom/` records as the only durable truth and using coding harnesses for model reasoning and source-changing work.

Downstream planning and tickets should cite this spec when building the first Mill application loop, execution dashboard, harness subprocess control, worktree isolation, and inter-iteration visibility.

## Product Slice

This spec owns the Factory Floor MVP behavior: local execution visibility and control for one workspace, at least one harness transport, one or more workstations, ticket pipeline display, backpressure signals, pause/steer/resume, and at least one inter-iteration summary process.

This spec does not own the Design Office shaping UI, hosted/team collaboration, Textual TUI, cloud deployment, commercial packaging, external project-management integrations, or a general agent framework.

## Spec Set Coverage

This is the first behavior contract for Loom Mill as an application layer. It complements:

- `constitution:main` - defines Loom as protocol plus Mill as factory application.
- `roadmap:loom-mill` - says Factory Floor MVP ships before Design Office MVP.
- `research:20260524-loom-mill-software-factory` - records the factory architecture and open design questions.
- `spec:ticket-owned-worker-handoffs` - defines the ticket-owned worker context Mill must preserve when launching harness work.
- `spec:loom-driver-agent` - defines the inner-loop coordinator behavior that Mill can invoke through a harness.

Adjacent behavior that needs separate specs later:

- Design Office shaping experience.
- Mill record parser and topology extraction if it becomes a reusable module/API.
- Harness adapter contracts if more than one harness is supported.
- Inter-iteration process contracts if they become pluggable or independently versioned.

## Problem

Chat-based Loom execution works but gives the operator poor visibility into long-running autonomous loops. The operator must inspect `.loom/` records, worker reports, git diffs, command output, and audit state manually to understand whether the line is moving, stuck, drifting, or ready for steering.

The Factory Floor MVP should prove that Mill can make execution visible and steerable without becoming a database, semantic scheduler, agent framework, or second source of truth.

## Desired Behavior

Loom Mill runs as a local application for one workspace. It watches `.loom/` and git, parses semi-structured record topology, renders a live Factory Floor dashboard, and manages harness subprocesses inside bounded workstation contexts. The model remains responsible for interpreting prose, selecting or executing shaped work through Loom skills/agents, and updating records. Mill provides mechanical loop continuation, isolation, visibility, pause/resume controls, and non-semantic pattern/backpressure detection.

The MVP should feel like a factory control room, not a record browser. The operator sees the line: queued/shaped tickets, active workstations, evidence/audit posture, recent diffs or commits, iteration summaries, backpressure signals, and andon alerts. When something looks wrong, the operator can pause, inspect or reshape the owning record, and resume from the updated graph.

## Not Doing

- Do not make Mill required for Loom protocol usage.
- Do not move durable truth out of `.loom/` records.
- Do not require a database or schema migration system for protocol records.
- Do not let Mill make semantic decisions about prose meaning, acceptance, priority, audit verdicts, or closure.
- Do not build the Design Office UI in this MVP except for a minimal record-open/edit escape hatch needed for steering.
- Do not support multi-operator collaboration, hosted/cloud operation, or mobile.
- Do not support every harness in the first slice.
- Do not implement a full scheduling agent before one visible ticket execution loop works.
- Do not persist secrets, raw credentials, private keys, or sensitive harness output in records or logs.

## Requirements

- REQ-001: Mill MUST treat `.loom/` records as the only durable truth store for Loom work. Any Mill runtime state must be either ephemeral, explicitly non-authoritative, or recorded through the appropriate Loom surface when future agents need it.

- REQ-002: Mill MUST parse only enough record structure to render topology and state: IDs, types, statuses, dates, headings, related-record references, acceptance IDs, requirement IDs, scenario IDs, and known Loom surface paths. Mill must not interpret prose meaning as product truth.

- REQ-003: The Factory Floor MVP MUST render a pipeline/control-room view of ticket execution state from `.loom/` and git, including queued or open tickets, active tickets, blocked/review/closed state, related evidence/audit records when discoverable, and recent source changes.

- REQ-004: The Factory Floor MVP MUST support starting a harness subprocess against a selected ticket or scoped execution target. The harness command, model, and flags MUST be operator-configurable through a UI surface (e.g., dropdown, settings panel). Mill treats the harness as an opaque subprocess command; the same lifecycle code path applies regardless of which harness is configured.

- REQ-005: Source-changing execution MUST happen in a bounded workstation context. The intended default is one git worktree per active ticket or execution target.

- REQ-006: Mill MUST provide pause/stop control for a running workstation. Pause/stop should terminate the subprocess, preserve the observable run state, and leave durable interpretation to the graph and later model pass.

- REQ-007: Mill MUST support steering by letting the operator inspect and edit the relevant Loom record before resume. Resume starts a fresh harness process from the updated graph rather than relying on hidden in-memory conversation state.

- REQ-008: The MVP MUST produce at least one inter-iteration operator summary after a worker iteration or subprocess exit. The summary may be generated by a model or deterministic summarizer, but it must be labeled as visibility output unless promoted into a Loom record by an appropriate model pass.

- REQ-009: Mill MUST expose backpressure signals that are mechanical or observed, not semantic verdicts. Examples include command pass/fail, repeated identical failures, long iteration duration, no record change after a run, dirty worktree state, missing evidence links, or repeated modification of the same files.

- REQ-010: Mill MUST support an andon state when a mechanical signal or worker exit indicates the line should stop for operator attention. Andon does not decide acceptance; it makes the problem visible and stops or holds execution until the operator or model resolves the next move.

- REQ-011: Mill MUST keep the protocol portable. All Factory Floor behavior must remain additive; chat-based shaping, Driver graph draining, and direct record editing must still work without Mill.

- REQ-012: The MVP MUST use a Python/Starlette backend and Svelte 5/Tailwind frontend that builds to static assets compatible with later Tauri wrapping.

## Scenarios

### SCN-001: Observe Existing Graph

Exercises: REQ-001, REQ-002, REQ-003, REQ-011

GIVEN a workspace with existing `.loom/` records and git history
WHEN the operator opens the Factory Floor
THEN Mill shows tickets grouped by status and related records when discoverable
AND shows recent git changes relevant to the workspace
AND does not require changing the records to view them.

### SCN-002: Start One Ticket Workstation

Exercises: REQ-004, REQ-005, REQ-011

GIVEN an operator selects an open ticket with enough durable context for a worker run
WHEN the operator starts execution
THEN Mill creates or selects a bounded workstation context
AND launches the configured harness subprocess against that ticket or execution target
AND displays the active workstation state without treating subprocess output as durable truth.

### SCN-003: Pause, Steer, Resume

Exercises: REQ-006, REQ-007

GIVEN a workstation is active and the operator sees drift, blockage, or missing constraints
WHEN the operator pauses the run
THEN Mill terminates or stops the subprocess in a controlled way
AND keeps the current record, git, and output state inspectable
WHEN the operator edits the relevant Loom record and resumes
THEN Mill launches a fresh harness subprocess from the updated graph.

### SCN-004: Inter-Iteration Summary

Exercises: REQ-008, REQ-009

GIVEN a worker subprocess exits or an iteration boundary is detected
WHEN Mill gathers the current ticket state, git diff/commit state, and visible command output
THEN Mill produces an operator-facing summary of what appears to have changed
AND labels limits clearly so the summary is not confused with evidence, audit, or ticket closure.

### SCN-005: Andon On Repeated Failure

Exercises: REQ-009, REQ-010

GIVEN a workstation repeats the same failing command, same test failure, or same blocked state across configured iterations
WHEN the pattern threshold is reached
THEN Mill raises an andon alert
AND pauses or holds further automatic continuation for that workstation
AND points the operator to the ticket, output, and changed files that explain the alert.

## Evidence Plan

- REQ-001 / SCN-001: Unit tests or integration checks show Mill renders state from fixture `.loom/` records and does not write durable non-record truth.
- REQ-002 / SCN-001: Parser tests over representative records extract IDs, statuses, types, headings, and references without prose interpretation.
- REQ-003 / SCN-001: UI or API snapshot shows ticket pipeline state, related records, and recent git state for fixture data.
- REQ-004 / SCN-002: Integration test with a configured harness command (any safe local command during development) shows Mill launches and captures subprocess lifecycle for a selected ticket.
- REQ-005 / SCN-002: Integration test shows source-changing execution happens in a separate worktree or bounded workstation directory.
- REQ-006 / SCN-003: Integration test shows pause/stop terminates the subprocess and leaves state inspectable.
- REQ-007 / SCN-003: Manual or integration evidence shows editing a record before resume causes the next subprocess to read the updated file state.
- REQ-008 / SCN-004: Evidence shows an iteration summary is generated and labeled as visibility output, not acceptance proof.
- REQ-009 / SCN-005: Pattern-detection test with repeated failure fixtures raises a backpressure signal.
- REQ-010 / SCN-005: Andon-state test shows the affected workstation stops or holds continuation until operator/model action.

## Resolved Decisions

- RD-001: The harness is a configured subprocess command with flags. Mill provides a harness configuration surface (e.g., dropdown or settings) where the operator selects the transport command, model flags, and any harness-specific options. Mill does not have a "fake harness" abstraction; during development the configured command can be any local command or script. In production it is `opencode run`, `claude -p`, `codex exec`, or whatever the operator prefers. Same subprocess lifecycle code path regardless.

- RD-002: MVP scheduling is manual ticket selection. The operator picks which ticket to start. Automatic pull from ready tickets is a later addition once readiness indicators and WIP behavior are observable.

- RD-003: Mill runtime state lives in a gitignored `.mill/` directory in the workspace root. This holds iteration logs, subprocess PIDs, takt measurements, pattern history, harness config, and runtime session state. Not in `.loom/` because it is not durable truth. Not in a global app cache because it is workspace-specific.

- RD-004: Backend is Python with Starlette for the WebSocket/REST layer (lightweight, async-native, no framework overhead). File watching via watchfiles. Git and subprocess via asyncio subprocess. No ORM or database.

- RD-005: Frontend is Svelte 5 (runes for fine-grained reactivity, built-in motion/transition primitives for dashboard UX, smallest bundle for Tauri startup). Tailwind CSS for full design control. D3 or similar for pipeline/graph visualization. Builds to static assets that Tauri loads directly. SvelteKit only if routing complexity demands it; plain Svelte SPA preferred for MVP.

## Open Questions

- OQ-005: What is the minimum backpressure set for MVP? Recommended answer: subprocess exit status, repeated command/test failure, iteration duration, dirty worktree state, missing evidence links, and no record change after run. Blocks downstream plan? no, if MVP starts with a smaller fixture-tested subset.

## Quality Bar

The Factory Floor MVP should make a long-running Loom execution legible within seconds. A reviewer should be able to answer: what is active, what changed recently, what evidence/audit exists, whether the line is moving or stuck, what the operator can safely pause or steer, and what claims remain unproven.

The UI should feel like a control room, not an IDE clone or markdown notebook. Its primary job is execution situational awareness and intervention.

## Interface Contract

- Inputs: local workspace path, `.loom/` records, git repository state, configured harness command(s), selected ticket or execution target, operator controls.
- Outputs: live UI state, subprocess lifecycle state, iteration summaries, backpressure/andon signals, optional evidence or knowledge records only when produced through an appropriate model pass.
- Side effects: may create/delete worktrees or bounded workstation directories, start/stop subprocesses, read `.loom/` and git state, and write runtime logs outside durable Loom truth. Durable Loom record writes require explicit model/operator action or a later ticket that defines safe record-writing behavior.
- Error semantics: if workspace is not a git repo, `.loom/` is missing, harness command is unavailable, worktree creation fails, or subprocess control is unsafe, Mill shows a blocked/andon-style state rather than inventing semantic progress.
- Validation boundary: MVP evidence can use fixture records and fake harnesses for parser/process behavior; real harness behavior needs separate evidence before broader runtime confidence claims.
- Compatibility or deprecation: no Loom protocol workflow is deprecated by this spec.

## Examples And Non-Examples

Example: The operator selects `ticket:20260525-example`, starts one OpenCode workstation, watches the ticket move to active, sees a generated iteration summary after the subprocess exits, notices an andon alert for repeated test failure, opens the ticket, edits scope or constraints, and resumes from a fresh subprocess.

Non-example: Mill reads the prose in a ticket, decides acceptance is satisfied, closes the ticket itself, and records a verdict without a model/evidence/audit path.

Non-example: Mill requires users to migrate `.loom/` records into a database before the protocol can work.

## Constraints

- `AGENTS.md` currently states this repo ships a Markdown skill corpus, not an app runtime. Adding Mill implementation code is an architecture change that should be deliberate and ticketed; this spec only shapes the behavior.
- Worktree isolation is required before parallel source-changing execution.
- Mill-visible summaries and telemetry are not evidence unless recorded through `loom-evidence` with an observation procedure and limits.
- Operator controls must be safe around long-running subprocesses and avoid destructive cleanup without explicit consent.
- Sensitive output must be redacted or omitted from durable records and logs when possible.

## Related Records

- `constitution:main` - durable Loom/Mill identity, factory principles, and constraints.
- `roadmap:loom-mill` - strategic sequence: Factory Floor MVP before Design Office MVP.
- `research:20260524-loom-mill-software-factory` - synthesis and factory mapping behind this spec.
- `spec:ticket-owned-worker-handoffs` - worker handoff behavior Mill must preserve.
- `spec:loom-driver-agent` - inner-loop coordinator behavior Mill can invoke through harness subprocesses.
- `spec:loom-weaver-agent` - shaping persona relevant to later Design Office work.
