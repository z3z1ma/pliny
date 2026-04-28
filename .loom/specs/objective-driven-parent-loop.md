---
id: spec:objective-driven-parent-loop
kind: spec
status: draft
created_at: 2026-04-28T00:00:00Z
updated_at: 2026-04-28T00:00:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:gastown-simplified-parent-driver
external_refs: {}
---

# Summary

This spec defines the intended behavior for an objective-driven parent loop: a
chat-initiated Loom workflow that can turn a high-level user objective into
measurable owner records, create and execute bounded ticket tranches through
Ralph/subagents, reconcile truth, and continue until the objective is satisfied
or a human decision is needed.

# Problem

Loom currently has strong owner layers and Ralph packet discipline, but a user
still tends to drive each phase manually: ask for planning, ask for ticket
creation, ask for Ralph execution, ask for follow-up tickets, and so on. That
keeps the workflow honest, but it does not deliver the hands-off step change that
Gastown-style orchestration suggests.

The missing behavior is an explicit parent workflow that can continue across the
outer loop and inner loop without an external script or daemon. The workflow must
remain compatible with Loom's truth boundaries: records own project truth,
tickets own live execution, packets own bounded child contracts, and transports
or subagents do not become canonical ledgers.

# Desired Behavior

When a user provides a high-level objective, the agent should activate an
objective-driven parent-loop workflow. The workflow should clarify just enough
with the user to establish measurable initiative-level objectives, then proceed
autonomously through Loom's existing owner graph.

The parent should create or refine the durable records that make the objective
recoverable, then repeatedly decompose the next tranche of work into bounded
tickets, execute those tickets through local edits or Ralph/subagents, reconcile
the results into ticket/evidence/critique/wiki truth, and decide whether to stop,
ask the user, or create the next tranche.

The loop is chat-initiated. It must not require a script, daemon, or outside
poller. A dedicated outer-loop subagent is allowed as a context-management
transport when the parent needs fresh synthesis, but it does not own objective
truth or execution state.

# Constraints

- The workflow must preserve Loom's existing owner model.
- The workflow must not introduce a required script, daemon, product CLI,
  dashboard, hidden database, or background poller.
- The workflow must not create a new canonical layer for "objective loop",
  "mayor", "driver", "convoy", or "agent identity" truth.
- The user starts the process through chat.
- The workflow may ask focused questions before proceeding when objectives,
  success metrics, risk tolerance, or product constraints are too ambiguous.
- Once objectives are clear enough, the workflow should proceed without requiring
  the user to approve every decomposition step.
- Continuity across compaction must come from Loom records, not transcript
  memory.
- Dedicated subagents may be used for outer-loop synthesis, Ralph execution,
  critique, wiki, or research, but the parent remains responsible for final
  reconciliation into owner records.
- The loop must stop or ask the user when it reaches a decision that would invent
  product direction, widen scope materially, accept unresolved risk, or spend a
  configured budget.

# Requirements

- REQ-001: The workflow starts by determining whether the request is a high-level
  objective requiring an initiative-level owner, a smaller plan/ticket-sized
  request, or a question that should stay in research/spec shaping.
- REQ-002: For high-level objectives, the workflow must elicit or define
  measurable success criteria before creating downstream tickets.
- REQ-003: The workflow must create or update the appropriate Loom owner records:
  initiative for objective and success metrics, research for uncertainty, spec
  for intended behavior, plan for sequencing, tickets for live execution,
  packets for bounded child work, evidence for observations, critique for review,
  and wiki for accepted explanation.
- REQ-004: The workflow must decompose work into tranches that can produce
  bounded tickets instead of attempting one monolithic execution pass.
- REQ-005: Each ticket created by the workflow must be independently legible,
  scoped, and clear enough for a local edit or Ralph iteration.
- REQ-006: The parent must execute or delegate only bounded work with explicit
  read/write scope, stop conditions, and output expectations.
- REQ-007: The parent must reconcile each child result into ticket truth before
  launching follow-on work that depends on it.
- REQ-008: After each tranche, the parent must reassess objective satisfaction,
  evidence sufficiency, critique disposition, and remaining gaps before creating
  more tickets.
- REQ-009: The workflow must support a dedicated outer-loop subagent for fresh
  synthesis when context accumulation would make the main session less reliable.
- REQ-010: A dedicated outer-loop subagent must return proposed owner-record
  changes, decomposition, risks, and next routes; it must not silently own final
  truth or closure.
- REQ-011: The loop must define explicit stop conditions, including objective
  satisfaction, need for human judgment, blocked tickets, unsafe write-scope
  overlap, missing evidence, unresolved critique, and budget/time limits.
- REQ-012: If context compaction happens, a fresh agent must be able to resume by
  reading Loom records rather than reconstructing the chat transcript.

# Scenarios

## Scenario 1: High-Level Product Request

Given the user asks for a broad outcome such as "build a small SaaS app," the
agent asks focused questions until the objective, constraints, and first success
metrics are clear enough. The agent creates an initiative, adds research/specs as
needed, creates a plan for the first tranche, creates bounded tickets, executes
them through Ralph/local edits, records evidence and critique, then reassesses
whether to create the next tranche.

## Scenario 2: Existing Initiative Continuation

Given an initiative and plan already exist, the agent reads the current owner
chain, identifies unfinished objective gaps, creates or advances the next tickets,
executes bounded work, reconciles evidence and critique, and updates the plan or
initiative status summary only with strategy-level truth.

## Scenario 3: Context Pressure

Given the main session is accumulating too much context, the parent compiles a
bounded outer-loop synthesis prompt or packet for a dedicated subagent. The
subagent reviews the objective chain and returns proposed next records, ticket
slices, risks, and stop conditions. The parent inspects the result and applies
the owner-record changes.

## Scenario 4: Human Decision Needed

Given the next step requires a product tradeoff the user has not delegated, the
agent stops the loop and asks a focused question instead of inventing direction.
After the user answers, the parent records the decision in the correct owner
layer and resumes.

# Acceptance

- ACC-001: A high-level objective can be transformed into a durable initiative
  with measurable success criteria and linked downstream work.
- ACC-002: The workflow can create the next ticket tranche after prior tickets
  complete, without requiring a new user instruction for every ticket.
- ACC-003: The workflow can use Ralph/subagents for bounded execution while the
  parent retains reconciliation authority.
- ACC-004: The workflow can use a dedicated outer-loop subagent for fresh
  objective synthesis without creating a new canonical truth layer.
- ACC-005: A fresh agent after compaction can resume the objective loop from Loom
  records alone.
- ACC-006: The workflow stops or asks the user at explicit boundaries rather than
  running blindly.
- ACC-007: No required script, daemon, product CLI, dashboard, or external poller
  is introduced.

# Open Questions

- What should the dedicated outer-loop agent be called if the product exposes one
  as an optional transport role?
- The objective-loop behavior will live in a new workflow-coordinator skill named
  `loom-drive`.
- How much user questioning should be required before the loop may proceed with
  reasonable defaults?
- What is the minimal template surface for an outer-loop synthesis handoff to a
  dedicated subagent?
