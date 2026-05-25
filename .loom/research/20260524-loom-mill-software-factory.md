# Loom Mill: Software Factory Architecture

ID: research:20260524-loom-mill-software-factory
Type: Research
Status: active
Created: 2026-05-24
Updated: 2026-05-24

## Summary

Investigation into how Loom should evolve from a portable skill-based protocol into a full software factory system, informed by the Ralph Wiggum technique articles and operator experience. Concludes that Loom's existing conceptual model already captures the essential Ralph principles, that the protocol should be compressed rather than expanded, and that a first-class application ("Loom Mill") should be built on top of the protocol to provide shaping and execution experiences the operator cannot get from chat alone.

## Question

Can Loom's goal be achieved purely as a skill pack, or does it need a more comprehensive application layer? If an application layer, what should it look like, what should it NOT do, and how does it relate to the portable protocol?

## Scope

Covered:

- Synthesis of the Ralph Wiggum technique, operator skill, loop mechanics, and software factory concepts from Geoffrey Huntley's articles
- Mapping of Ralph principles to existing Loom surfaces
- Evaluation of skill-pack-only vs. custom tooling vs. hybrid approaches
- Architecture of a first-class application ("Loom Mill") with two modes
- Complete factory metaphor mapping to Loom Mill components
- Inter-iteration AI processes and their role
- Worktree isolation and parallel execution
- Relationship between protocol compression and application design
- Technology choices (web, Tauri, TUI)

Excluded:

- Detailed UI wireframes or component specifications
- Specific tech stack selection (React vs. Svelte, etc.)
- Implementation timeline or effort estimates
- Business model or go-to-market
- Detailed protocol compression proposals (separate work)

## Method And Sources

- Operator-provided articles: Ralph Wiggum technique, LLMs as mirrors of operator skill, AI as economic warfare, cognitive security, embedded software factory preview, everything is a ralph loop
- Inspection of existing Loom records: `decision:0002`, `spec:ticket-owned-worker-handoffs`, `spec:loom-driver-agent`, `spec:loom-weaver-agent`, `plan:20260515-ticket-owned-worker-handoffs`, `research:20260510-loom-loop-failure-analysis`
- Inspection of shipped skill surfaces: `loom-ralph`, `loom-tickets`, `loom-audit`, `loom-evidence`, `loom-driver.md`, `loom-weaver.md`
- Collaborative operator-agent shaping session on 2026-05-24

## Findings

### Finding 1: Loom Already Captures The Ralph Principles

The core Ralph ideas map directly to existing Loom surfaces:

| Ralph Principle | Loom Surface |
|---|---|
| One thing per loop | Ticket (one bounded closure claim) |
| Bounded worker discipline | Ralph (ticket-owned worker runs) |
| Backpressure (tests, checks, validation) | Evidence (observations associated to acceptance criteria) |
| Fresh context adversarial review | Audit (Ralph-backed review in fresh context) |
| Monolithic scheduler, not agent swarm | Driver (inner-loop coordinator) |
| Shape before execute | Weaver (outer-loop shaping) |
| Specs as deterministic context stack | Specs + Plans + Knowledge (loaded each iteration) |
| Worker output is claims, not truth | `spec:ticket-owned-worker-handoffs` REQ-005 |
| Operator skill matters | Shaping discipline, Weaver adversarial posture |
| Loop failures tune the system | Knowledge promotion, retrospective |
| Transient prompts are transport, not truth | `decision:0002`, REQ-004 |

No new conceptual machinery is needed. The protocol is sound.

### Finding 2: The Protocol Is Too Verbose

The existing skill surfaces over-explain philosophy and repeat surface-ownership explanations across every skill. The model-visible doctrine should be compressed toward operational kernels: short, sharp, invariant-focused instructions that install behavior rather than justify it. The Ralph "sign next to the slide" standard is the right bar: short enough that the model thinks about the sign, not overwhelmed by it.

What should be cut:
- Repeated surface-ownership explanations
- Long prose justifying Loom's existence
- Multiple restatements of shape-before-execute, evidence-before-closure, audit-before-trust
- Agent prompts that duplicate skill doctrine
- "Done means" sections that restate obvious invariants

What must be preserved:
- The surface model (what truth lives where)
- Ticket-owned worker handoff model
- Skill activation discipline
- Evidence/audit separation
- Driver/Weaver split
- Transient prompts are transport, not truth
- Worker reports are claims, not proof

### Finding 3: Skills Cannot Guarantee The Loop

A skill pack can teach a model the discipline. It cannot reliably enforce:
- Loop continuation across context windows
- Guaranteed fresh context per iteration
- Mechanical isolation (worktrees)
- Real-time telemetry
- Pattern detection across iterations
- Automated pause on defect detection
- Parallel worker coordination with actual filesystem isolation

The model can simulate scheduling within a single session (and does so successfully for 12+ hour runs with frontier models), but the operator has no visibility outside of manually digging through records and git.

### Finding 4: The Runner Is Not Infrastructure—It Is Just Loop Continuation

The `.loom/` records are prose-first, semi-structured, designed for reasoning models. There is no structured schema a dumb script can parse for decision-making. Graph integrity depends on a model reading with find/grep and making judgment calls.

Therefore the "runner" is not a scheduler, dispatcher, or state machine. It is simply: keep feeding a model the graph with fresh context. The intelligence is entirely in the model plus the protocol. The mechanical loop is trivial: `while :; do cat PROMPT.md | coding-harness; done`.

What a "custom harness" actually provides:
- Loop continuation (trivial mechanically)
- Visibility for the operator (the real UX problem)
- Steering (pause, reshape, resume)
- Isolation (worktrees)
- Inter-iteration processes (supplementary AI reasoning between iterations)

### Finding 5: Loom Mill Architecture

Loom Mill is one application with two modes (tabs):

**Tab 1: Shaping (The Design Office)**
- Operator + AI co-author records
- Split view: graph sidebar, document center, chat panel
- Voice input for thinking aloud
- Provenance/linking visualization
- Readiness indicators ("ready to fab" signals)
- Does NOT deprecate chat-based shaping; augments it

**Tab 2: Execution (The Factory Floor)**
- Pipeline view of tickets flowing through stages
- Live summaries per iteration (generated by inter-iteration AI)
- Backpressure signals (tests, types, lint, grep checks)
- Pattern detection and alerts (jidoka/andon)
- Pause/steer/resume controls
- Changelog and aggregate views
- Does NOT deprecate telling Driver to "drain the graph" in chat; augments it

**Under the hood:**
- Python backend watches `.loom/` and git for changes
- Manages harness subprocesses (start/stop)
- Manages worktree isolation
- Runs inter-iteration AI processes
- Pushes real-time updates via WebSocket
- Frontend: web (with Tauri desktop option)
- Alternative: Textual-based Python TUI

### Finding 6: Inter-Iteration Processes Are Key

Because Mill manages the subprocess, it can run lightweight AI processes between worker iterations:

| Process | Input | Output | Purpose |
|---|---|---|---|
| Summarize | ticket + diff + evidence | concise summary | operator visibility in dashboard |
| Retrospect | ticket + evidence + patterns | knowledge records | graph improvement for future iterations |
| Aggregate | recent summaries | changelog view | big-picture operator awareness |
| Check evidence | ticket ACC-* + evidence | readiness signal | know when a ticket is done |
| Detect patterns | last N iteration data | warnings/alerts | catch drift before operator notices |
| Select next work | graph state + operator priorities | next ticket | pull-based scheduling |

These are cheap API calls (reading + producing markdown), not full coding harness runs. They operate on merged state after the worker's changes are committed. They improve the graph so future fresh-context iterations benefit from accumulated learning.

### Finding 7: Worktree Isolation Enables Safe Parallelism

Since Mill manages the subprocess, it can create Git worktrees per ticket:
- Each worker gets an isolated filesystem
- Parallel workers cannot step on each other
- Bad iterations are rolled back by deleting the worktree
- Merge is an explicit step Mill controls
- Validation can run before merge
- Roll back is trivial: `git branch -D`

### Finding 8: Complete Factory Mapping

The system maps precisely to a manufacturing factory:

**Roles:**
- Operator = Factory Owner (sets direction, quality bar, priorities, watches, steers)
- Weaver = Design Engineer (turns ideas into buildable blueprints, challenges weak designs)
- Scheduling Agent = Production Planner (picks next work unit based on priorities and capacity)
- Mill Orchestrator = Shift Supervisor (manages worktrees, launches workers, runs inter-iteration processes, detects patterns)
- Ralph Worker = Machine Operator (one task, one workstation, follows instructions, reports result)
- Auditor = End-of-Line Inspector (fresh eyes, reports defects, does not fix them)
- Inter-Iteration Processes = Quality Engineers + Maintenance Crew (summarize, improve tooling, clean up)

**Process elements:**
- Single-piece flow: one ticket through the line at a time per workstation
- The line never stops unless something is wrong
- Pull system: work pulled into fabrication when capacity exists and piece is ready
- Takt time: iteration duration as a signal (too long = task too big)
- WIP limits: configurable limit on concurrent active tickets
- Autonomation (Jidoka): machine stops itself when defect detected
- Andon cord: worker or pattern detection signals a problem, line stops, operator addresses it
- Poka-yoke: scope boundaries, write constraints, required evidence (mistake-proofing)
- Kanban signals: "ready to fab" indicators
- Kaizen: each iteration makes the graph slightly smarter via knowledge promotion
- Changeover time: minimize worktree setup, context loading, inter-iteration overhead
- Heijunka: level scheduling, mix difficulty, maintain steady flow

**Physical mapping:**
- Design Office = Tab 1 (shaping)
- Factory Floor = Tab 2 (execution)
- Workstation = one worktree running one ticket
- Tooling/Jigs = skills + knowledge records
- Raw Materials = the `.loom/` graph
- Control Room = operator dashboard
- Shipping Dock = ticket closure + merge to main
- Finished Goods = working software on main branch

### Finding 9: Three-Layer Architecture

The system has three clean layers:

**Layer 0: Protocol (Loom)**
- Prose-first markdown records
- Semi-structured labels for topology (IDs, statuses, types, links)
- Portable across any harness or interface
- Defined by compressed skills
- The single source of truth
- No database, no structured schema, no integrity guarantees beyond model maintenance

**Layer 1: Skills**
- Teach any model the protocol
- Portable: work in ChatGPT, Claude.ai, OpenCode, Cursor, Codex, Gemini, any system supporting context injection
- Define invariants and record contracts
- Compressed operational kernels, not manuals

**Layer 2: First-Class Experience (Loom Mill)**
- One application, two tabs
- Web-first (Tauri for desktop, Textual TUI as lightweight option)
- Observes and steers but never owns truth
- Shells out to harness exec commands
- Does not deprecate chat-based workflows
- Records-as-API: Mill is just another client of `.loom/`

### Finding 10: The Protocol Is The Stable Core

Everything else is a client. The skills are a client (they teach models to read/write the protocol). Mill is a client (it watches, orchestrates, and renders the protocol). The harness is a client (it runs model inference that reads/writes the protocol). Even the operator is a client (they read and write records directly when they choose to).

This means:
- Protocol compression is independent of Mill development
- Mill can be built incrementally without changing the protocol
- Multiple interfaces can coexist (chat, Mill web, Mill TUI, raw file editing)
- The protocol survives if Mill is abandoned or rewritten
- Other people could build their own clients on the same protocol

## Conclusions

1. **Loom's conceptual model is correct.** The Ralph articles validate rather than challenge it. No new surfaces or concepts are needed.

2. **The protocol should be compressed.** Skills should be operational kernels that install behavior, not manuals that explain philosophy. The factory metaphor provides the right frame for thinking about what each piece does.

3. **Loom Mill should be built as a separate application on top of the protocol.** It provides the first-class experiences that chat alone cannot: split-pane shaping, factory floor visibility, pause/steer, pattern detection, inter-iteration intelligence, worktree isolation.

4. **Mill's intelligence comes from the model reading prose, not from structured data processing.** The backend watches files and manages subprocesses. It never makes decisions about what work means or what to do next. Those calls belong to the model reading the graph.

5. **Inter-iteration processes are how the factory improves itself.** Summaries for the operator, retrospectives for knowledge promotion, pattern detection for defect prevention. These run between iterations as lightweight AI calls.

6. **The factory metaphor is not analogy. It is architecture.** Every element of a manufacturing factory has a precise mapping to a Loom Mill component. The system should be designed, named, and built with this mapping as the structural guide.

7. **Portability is preserved.** Loom protocol + skills work everywhere. Mill is additive. Nothing is deprecated.

## Recommendations

- **Immediate:** Compress Loom protocol skills toward operational kernels. This is independent of Mill and improves the portable foundation.
- **Immediate:** Update constitution to reflect the Loom/Mill split identity and factory direction.
- **Near-term:** Prototype Mill Tab 2 (execution visibility) as it solves the biggest current pain point and is architecturally simpler.
- **Near-term:** Design the inter-iteration process contracts (what each process receives and produces).
- **Later:** Build Mill Tab 1 (shaping experience) as the more complex but more differentiating surface.
- **Later:** Explore the Textual TUI as a lightweight parallel track.

## Open Questions

- What is the minimum viable Tab 2 that delivers real value? (file watcher + status rendering + start/stop + basic summaries?)
- How should the scheduling agent's priorities be shaped by the operator? (constitution/roadmap? explicit queue ordering? both?)
- Should inter-iteration processes be pluggable (operator can add their own checks) or fixed?
- What is the right takt time signal? Should Mill suggest ticket splitting when iterations run long?
- How much of the factory floor state should persist in `.loom/` vs. be ephemeral Mill state? (iteration counts, takt measurements, pattern history)
- Should Mill produce its own records (e.g., evidence records from automated checks) or only the model does that?
- What is the right technology for the real-time file watching + WebSocket bridge?

## Related Records

- `decision:0002` - validates that tickets own worker context; Mill orchestrates workers against tickets
- `spec:ticket-owned-worker-handoffs` - the execution contract Mill implements
- `spec:loom-driver-agent` - Driver behavior maps to Mill's orchestration loop
- `spec:loom-weaver-agent` - Weaver behavior maps to Mill's shaping mode
- `research:20260510-loom-loop-failure-analysis` - historical context for why bounded execution discipline exists
- `plan:20260510-core-loop-hardening` - historical context for protocol hardening that Mill now operationalizes
