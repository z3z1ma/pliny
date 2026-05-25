# Agent Loom Constitution

ID: constitution:main
Type: Constitution Core
Status: active
Created: 2026-05-24
Updated: 2026-05-24

## Summary

Agent Loom is a software factory system. It has two parts: a portable protocol and a factory application. The protocol defines how AI agents read, write, and maintain a prose-first recovery graph. The factory application provides first-class experiences for shaping work and observing execution. Both serve one goal: the operator shapes precise manufacturing orders, and the factory builds software autonomously with quality built in at every step.

## Project Judgment

### What This Project Is

Agent Loom is a software factory. It has two layers:

**Loom (the protocol):** A plain-English markdown protocol that defines what kinds of truth exist, where they live, how they link, and what invariants models must maintain. The protocol is portable across any AI harness or interface that supports context injection. Records are prose-first, semi-structured, designed for reasoning models reading with find and grep. There is no database, no structured schema, no integrity guarantee beyond what a reasoning model maintains.

**Loom Mill (the factory application):** A first-class application built on top of the protocol. One application, two modes. The Design Office (shaping) and the Factory Floor (execution). Mill observes and steers but never owns truth. It shells out to any coding harness for model inference. It manages worktree isolation, inter-iteration AI processes, and operator visibility. Mill is a client of the protocol, not a replacement for it.

### What This Project Is Not

- Not a database or structured record store
- Not a replacement for the coding harness (Mill shells out to whatever harness the operator uses)
- Not an agent framework or LLM wrapper
- Not dependent on any single model provider
- Not a tool that removes the operator from the loop
- Not infrastructure that makes decisions the model should make

### The Factory Metaphor Is Architecture

The system maps to a manufacturing factory. This is not analogy. It is structural design:

- Design Office = shaping mode (operator + Weaver co-author blueprints)
- Factory Floor = execution mode (bounded iterations, quality at every step)
- Workstation = one worktree running one ticket
- Machine Operator = Ralph worker (one task, follows instructions)
- Shift Supervisor = Mill orchestrator (manages iterations, detects patterns)
- Production Planner = scheduling agent (picks next work from queue)
- Inline Inspection = evidence gathering during implementation
- End-of-Line Inspection = audit (fresh context adversarial review)
- Statistical Process Control = pattern detection across iterations
- Andon Cord = pause/alert on defect detection
- Poka-yoke = scope boundaries, write constraints, required evidence
- Tooling/Jigs = skills + knowledge records
- Kanban Signal = "ready to fab" indicators
- Kaizen = knowledge promotion from retrospectives
- Raw Materials = the `.loom/` graph
- Finished Goods = working software merged to main

### How Intelligence Works

The intelligence is always in the model reading prose. Mill never interprets record meaning or makes execution decisions. The model reads the graph, decides what to do, acts within bounds, and updates records. Mill provides the loop, isolation, visibility, and steering. The division is:

- Model handles: implementation, judgment, priority reasoning, evidence interpretation, audit, escalation
- Mill handles: loop continuation, worktree isolation, inter-iteration processes, telemetry, pause/resume, pattern detection (mechanical, not semantic)

## Principles And Constraints

### Protocol Principles

- Records are prose-first. Semi-structured labels (IDs, statuses, types) support topology extraction. Prose carries meaning.
- Skills should be operational kernels that install behavior, not manuals that explain philosophy. The "sign next to the slide" standard: short enough that the model thinks about the sign.
- The protocol is the stable core. Skills, Mill, harnesses, and operators are all clients.
- Portability is non-negotiable. The protocol must work in any system that supports context injection: ChatGPT, Claude.ai, OpenCode, Cursor, Codex, Gemini, a raw API loop, web interfaces with skill support.
- Nothing is deprecated. Chat-based shaping still works. Telling Driver to drain the graph still works. Mill is additive.

### Factory Principles

- Single-piece flow. One ticket through the line at a time per workstation. No batching.
- The line never stops unless something is wrong. Execution continues by default.
- Pull, not push. Work enters fabrication when capacity exists and the piece is ready.
- Quality built in, not bolted on. Evidence during implementation, not only after.
- Fresh context per iteration. Each worker gets a clean context window. The graph is continuity.
- Worker output is claims until reconciled. Trust nothing without checking.
- The factory improves itself. Inter-iteration retrospectives promote knowledge back into the graph.
- The operator steers, the factory builds. The operator's job is design and steering. The factory's job is execution and quality.

### Constraints

- Mill must never own truth. All durable state lives in `.loom/` records.
- Mill must never make semantic decisions about records. Only models reason about prose.
- The protocol must not require Mill to function. A model with skills and a file system is sufficient.
- Inter-iteration processes must not modify records in ways that break graph consistency for the next worker iteration.
- Worktree isolation is required for parallel execution. No two workers share a filesystem.
- Skills must not explain Loom's packaging, adapter mechanics, or self-justification. They teach runtime behavior.

## Current Constitutional Direction

The project has two immediate work streams:

1. **Protocol compression**: Reduce model-visible skill doctrine to operational kernels. Cut repeated explanations, philosophy, and justification. Preserve invariants, activation discipline, surface model, and record contracts.

2. **Loom Mill design and prototyping**: Build the factory application. Start with execution visibility (Tab 2 / Factory Floor) as it solves the biggest pain point. Shaping experience (Tab 1 / Design Office) follows as the more complex but more differentiating surface.

Both are independent and can proceed in parallel. Protocol compression improves the portable foundation regardless of Mill. Mill can be built incrementally against the current protocol.

## Open Questions

- What is the minimum viable Factory Floor (Tab 2) that delivers real value?
- How should the scheduling agent's priorities be shaped by the operator?
- Should inter-iteration processes be pluggable?
- How much Mill state (iteration counts, takt measurements, pattern history) should persist in `.loom/` vs. be ephemeral?
- What is the right technology stack for Mill's backend?
- Should Mill produce its own records (evidence from automated checks) or only orchestrate model-produced records?

## Related

- `research:20260524-loom-mill-software-factory` - full investigation and synthesis that produced this constitutional direction
- `decision:0002` - validates ticket-owned worker handoffs as the execution contract Mill implements
- `spec:ticket-owned-worker-handoffs` - behavior contract for bounded worker runs
- `spec:loom-driver-agent` - Driver behavior that maps to Mill's orchestration loop
- `spec:loom-weaver-agent` - Weaver behavior that maps to Mill's shaping mode
