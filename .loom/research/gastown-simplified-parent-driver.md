---
id: research:gastown-simplified-parent-driver
kind: research
status: active
created_at: 2026-04-28T00:00:00Z
updated_at: 2026-04-28T00:00:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
external_refs:
  github:
    - https://github.com/steveyegge/gastown
---

# Question

How should Loom recreate the useful part of the Gastown experience in a much
simpler way, centered on Ralph/subagents, so a user can give a high-level
objective and the parent agent can keep decomposing, executing, reconciling, and
replanning until the objective is satisfied or human input is needed?

# Why This Matters

Gastown demonstrates a strong multi-agent operator experience: a user can state
a high-level request, a coordinating agent can decompose it into durable work,
assign work to agents, watch worker health, recover from stale sessions, and keep
the system moving. The valuable step change is not just polling existing tickets;
it is allowing the parent to continue the outer loop as well as the inner loop.

For Loom, that means the parent must be able to create or refine initiatives,
research, specs, plans, and tickets as the objective evolves, then run Ralph
iterations beneath those records and repeat. Loom already has the owner graph for
this kind of work, but it does not yet name the lightest autonomous driver loop
that alternates between objective shaping, ticket creation, Ralph execution, and
acceptance review.

The decision matters because `constitution:main` forbids making Loom a runtime,
daemon, product CLI, dashboard, hidden database, or canonical orchestration
service. A Gastown-inspired workflow must therefore keep durable truth in Loom
records and treat any polling mechanism as transport or optional harness sugar.

# Scope

This note covers a first-pass architecture recommendation for a simplified
Gastown-like autonomous parent loop in this repository. It covers high-level
objective intake, repeated decomposition into Loom owners, parent polling,
chat-session versus script tradeoffs, and how the loop maps onto existing Loom
owners. It excludes implementing the loop, designing a full scheduler, dashboard,
merge queue, external federation, persistent identity system, or Beads-compatible
ledger.

# Method

Read the active Loom constitution, workspace record, public Loom docs, existing
Superpowers adaptation research, and the current Gastown README from GitHub.
Mapped Gastown concepts to Loom owner layers and rejected anything that conflicts
with Loom's anti-runtime boundary.

# Sources

- `.loom/constitution/constitution.md`
- `.loom/workspace.md`
- `README.md`
- `ARCHITECTURE.md`
- `PROTOCOL.md`
- `.loom/research/superpowers-skill-workflow-adaptation.md`
- `https://raw.githubusercontent.com/steveyegge/gastown/main/README.md`, fetched 2026-04-28

# Evidence

## Operator Clarification

The operator clarified that the valuable Gastown-like behavior is not merely
polling. The desired step change is that a user can provide a very high-level
request and the system can tease out measurable objectives, create the initiative
and downstream decomposition, execute through Ralph/subagents, reconcile results,
create the next tickets, and repeat until the objective is satisfied enough or
human involvement is needed.

The operator also clarified two constraints:

- no scripts or external polling process should be required for the first design;
  the user sends a chat message and the agent-driven workflow proceeds from there
- a dedicated outer-loop agent may be useful to limit context accumulation in
  the main chat, but that agent should be treated as a transport/execution role,
  not as a new canonical truth layer

## Gastown Surface

Gastown describes itself as a multi-agent orchestration system with persistent
work tracking. Its main concepts include:

- Mayor: primary AI coordinator.
- Rigs: project containers around git repositories.
- Crew members: personal workspaces.
- Polecats: worker agents with persistent identity and ephemeral sessions.
- Hooks: git worktree-backed persistent storage for agent work.
- Convoys and Beads: durable work tracking units.
- Witness, Deacon, Dogs: watchdog and supervisor layers for stuck-agent
  detection and recovery.
- Refinery: merge queue processor.
- Scheduler: dispatch capacity governor.

The README's recommended workflow starts with the Mayor, creates a convoy,
assigns issues to worker agents, monitors progress, and summarizes results.
Gastown also supports minimal mode where the system tracks state while runtime
sessions are started manually.

## Loom Surface

Current Loom already owns the durable pieces needed for a simplified version:

- tickets own live execution state, blockers, acceptance disposition, and next
  route
- Ralph packets own bounded child-worker contracts
- evidence owns observed outputs
- critique owns adversarial findings and verdicts
- plans own sequencing and execution waves
- `loom-git` owns branch/worktree isolation and provenance
- workspace/harness records may describe transport, but do not own project truth

The constitution explicitly rejects a required runtime, daemon, MCP, dashboard,
product CLI, hidden database, helper ontology, and canonical truth outside the
designated `.loom/` subtrees.

## Concept Mapping

| Gastown concept | Loom analogue | Adaptation |
| --- | --- | --- |
| Mayor | parent agent | Use the current parent agent as the workflow driver and reconciliation authority. |
| Convoy | plan execution wave plus ticket set | Do not add a new work unit; express grouped work through plans and tickets. |
| Bead | ticket | Tickets remain the sole live ledger. |
| Polecat | Ralph child/subagent | Child identity is optional transport metadata, not canonical truth. |
| Hook | packet plus worktree plus evidence | Split contract, implementation isolation, and observation into existing owners. |
| Witness/Deacon | parent polling pass | Start with one explicit parent-driver loop before any watchdog hierarchy. |
| Scheduler | execution-wave capacity rule | Keep capacity as plan/driver policy unless repeated use proves a need for optional tooling. |
| Refinery | ship plus critique plus ticket acceptance | Do not add merge queue behavior to core protocol. |

## The Missing Capability

The first-pass "poll ready tickets" interpretation is too small. It only drains
an existing queue. The stronger Gastown-style value is **objective-driven
continuation**:

```text
high-level objective
-> initiative/spec/research/plan shaping
-> ticket creation
-> Ralph execution
-> evidence/critique/acceptance reconciliation
-> next decomposition decision
-> repeat until objective satisfaction or explicit stop
```

In Loom terms, the parent cannot be only a Ralph packet launcher. It must be an
outer-loop driver that can decide whether the next move is more research, a spec
clarification, a plan update, a new ticket, a Ralph iteration, critique,
retrospective promotion, or a human question.

For a large request such as "build a SaaS app," the parent should not try to
compile one giant plan and then run forever blindly. It should maintain an
initiative-level objective with success metrics, create a plan for the next
meaningful tranche, issue bounded tickets, execute them, re-evaluate the
initiative against evidence, and then generate the next tranche.

# Rejected Options

- Adding a required daemon was rejected because it conflicts with
  `constitution:main` and would make orchestration behavior a runtime surface
  instead of a protocol route.
- Adding Gastown-style `Mayor`, `Polecat`, `Convoy`, `Hook`, `Witness`, or
  `Deacon` as canonical Loom layers was rejected because Loom already has owner
  layers for the underlying truths.
- Keeping the real parent loop only in chat was rejected as the durable design
  because a stopped chat session is not recoverable by a fresh agent unless the
  objective, decomposition, ticket queue, packets, evidence, and acceptance state
  are reflected in Loom records.
- Limiting the loop to polling ready tickets was rejected because it cannot
  satisfy high-level objectives that require the parent to discover and create
  the next tickets after each tranche lands.
- Building a full scheduler, dashboard, merge queue, federation, or persistent
  worker identity system as the first step was rejected as out of scope and too
  close to recreating Gastown instead of simplifying it.

# Null Results

- No new canonical owner layer appears necessary for the first simplified
  Gastown-style workflow.
- No evidence from the current Loom graph suggests that a background service is
  allowed as core product behavior.

# Conclusions

The smallest compatible design is an **objective-driven parent loop**: a
repeatable operator or optional harness procedure that starts from an initiative
or high-level objective, shapes enough research/spec/plan context to create the
next bounded tickets, executes one or more tickets through Ralph/local
edit/critique/evidence routes, reconciles the result into ticket and owner truth,
then asks whether the objective is satisfied or what decomposition should happen
next.

Polling is necessary but not sufficient. The parent needs two nested loops:

- outer continuation loop: inspect objective state, acceptance gaps, risks, and
  evidence; create or refine owner records and tickets for the next tranche
- inner execution loop: choose ready ticket or execution wave, compile and launch
  bounded Ralph work, reconcile output, and route to evidence/critique/acceptance

The likely product shape is a dedicated Loom skill that teaches this objective
loop to the current agent. The skill may instruct the current parent to use a
fresh outer-loop subagent for objective shaping and tranche planning when context
pressure is high, but the current parent still owns reconciliation and ticket
truth. A dedicated agent can be useful as a role, but it should not become a
canonical layer or hidden daemon.

This loop should be specified as protocol guidance before it is automated. If it
is automated later, the automation should be a thin optional harness adapter or
local script that performs ordinary file operations and subagent launches. It
must not own work state or become required for Loom correctness.

The parent should not literally "never stop" without boundaries. It should keep
working while the objective has unsatisfied, decomposable work and stop only when
one of these conditions is true:

- the initiative objective or current tranche is satisfied
- no ready ticket or execution-wave item exists and the next work cannot be
  safely decomposed without human input
- a ticket is blocked and needs operator input
- child write scopes would overlap or the integration state is unsafe
- required evidence or critique cannot be produced
- the next step requires product/behavior judgment the agent should not invent
- a configured budget, time limit, or safety limit is reached

# Recommendations

Create a small spec and plan for an `objective-driven parent loop` workflow with
these initial rules:

1. Inputs are existing Loom records: initiative objective and success metrics,
   research/spec gaps, plan execution waves, ready tickets, packet freshness,
   evidence state, critique disposition, and git/worktree safety.
2. The driver runs in the parent role, not the child role.
3. Each outer-loop iteration decides whether to update research, update a spec,
   update a plan, create tickets, ask the human, or move to execution.
4. Each inner-loop iteration chooses exactly one local edit, one Ralph packet,
   one critique pass, one evidence capture, one wiki/retrospective pass, or one
   acceptance review route.
5. Every child launch has an explicit packet or equivalent bounded contract.
6. Every child return is reconciled into the owning ticket before another child
   is launched for the same ticket.
7. After a tranche completes, the parent re-evaluates the initiative objective
   and creates the next tranche rather than stopping merely because the current
   tickets are closed.
8. Parallelism is allowed only through plan execution waves and non-overlapping
   child write scopes.
9. Transport is pluggable: current chat session first, optional script later,
   harness-native subagents when available.
10. A script may poll, select candidates, and invoke subagents, but the script's
    state is cache/support state only; tickets remain the live ledger and
    initiatives/plans/specs own objective, sequencing, and behavior truth.

For the user's immediate question, the recommended first implementation is:

- define the objective-driven parent loop in Loom guidance and a golden example
  that starts from a vague high-level request
- prove it manually in the chat session on one real objective, including creating
  the next ticket after a ticket completes
- add an optional thin script only after the repeated scan/select/launch/reconcile
  mechanics become the bottleneck

# Open Questions

- Should the first durable product change be a new `loom-workspace` objective
  continuation reference, a `loom-plans` execution-wave/tranche reference, or a
  `loom-ralph` parent-driver reference?
- What minimal machine-readable fields are needed for polling without turning
  Loom into a helper-dependent format?
- What fields should an initiative expose so a parent can determine whether the
  high-level objective is satisfied enough to stop?
- Should the parent driver prefer sequential work until manually configured for
  parallel Ralph, or should execution waves opt into parallelism by default when
  write scopes are disjoint?
- Which harness should be used for the first optional proof: OpenCode subagents,
  Claude CLI, Codex CLI, or a transport-neutral shell wrapper?

# Linked Work

- `spec:objective-driven-parent-loop`
