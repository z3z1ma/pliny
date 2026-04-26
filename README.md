# Loom - Markdown-Native Control Plane

Loom is a harness-agnostic protocol for long-horizon AI knowledge work.

It treats the filesystem as the interface, Markdown as the durable medium, and
fresh-context packets as the default way to delegate bounded implementation.
Critique and wiki work may reuse packet discipline, but their domain workflows
own review and synthesis.

This package is intentionally **not** a runtime, service, daemon, MCP, or product CLI.

It ships:

- a mandatory `loom-bootstrap` skill with ordered doctrine references that teach
  the model how Loom thinks and how Loom must be used
- on-demand `skills/` that teach the model how to operate each subsystem in detail
- Markdown templates and query recipes instead of bundled Python helpers
- a cohesive explanation layer: **Loom Wiki**

Read `PROTOCOL.md` for the stable protocol summary.

Loom is best understood as a source-of-truth type system plus a transaction
protocol for fallible AI workers. The workers are disposable. The graph is
durable. The parent is the transaction coordinator. Tickets are the execution
ledger. Evidence stores observed artifacts. Critique pressure-tests claims.
Wiki is the accepted explanation layer.

## The Core Shape

Loom has three operating axes:

- **layers**: typed owners for different kinds of truth
- **loops**: outer-loop shaping and inner-loop execution
- **packets**: bounded contracts for fresh-context work

A Loom transaction uses the kernel roles defined in `PROTOCOL.md`: owners,
claims, packets, evidence, critique, acceptance disposition, and promotion.

The layer model is the type system. Canonical owner layers own project truth;
support surfaces help recovery and handoff without becoming truth owners.

| Layer | Owns |
| --- | --- |
| constitution | durable identity, principles, hard constraints, precedent |
| initiative | strategic outcome |
| research | evidence synthesis, investigations, options, rejected paths, null results |
| spec | intended behavior and acceptance contract |
| plan | sequencing and rollout strategy |
| ticket | live execution state |
| evidence | observed artifacts |
| critique | adversarial findings and verdicts |
| wiki | accepted explanation |
| packet | bounded child-worker contract, not project truth |
| memory | optional support context only |

The rule that keeps the graph coherent is simple: truth ownership is by layer,
not by recency.

For software work, the codebase owns current implementation reality. Specs own
reusable intended behavior and acceptance contracts. Tickets own scoped execution,
ticket-local criteria when no spec exists, and acceptance disposition. Evidence
bridges implementation to claims, and critique judges whether the bridge is
strong enough.

## The Two Loops

### Outer loop

The outer loop scopes and re-scopes the work.

Its backbone progression is:

`constitution -> initiative -> plan -> ticket`

Use conditional gates before plan or ticket:

- route to research when evidence synthesis, tradeoffs, or conclusions are missing
- route to spec when intended behavior or acceptance criteria are fuzzy

### Inner loop

The inner loop is **Ralph**.

Ralph is one bounded packet, one fresh worker, one iteration, one reconciliation
pass.

A parent agent compiles a packet, launches or delegates one fresh-context execution step, receives a bounded outcome, merges truth back into the ticket, and either continues, stops, escalates, or routes into critique/wiki.

Critique and Wiki may reuse packet discipline, but their domain workflows own
review and synthesis. They are sibling routes, not Ralph-governed execution.

The deeper invariant is ownership-preserving mutation: every durable claim,
behavior, evidence artifact, risk, and explanation lands in the artifact that owns that
kind of truth.

### Transaction spine

Every non-trivial Loom transaction follows the same spine:

`route -> shape -> ready -> execute -> reconcile -> verify -> accept -> promote -> close`

If a step cannot be completed honestly, route backward to the owner that can fix
the gap instead of advancing on vibes.

## Repository Layout

```text
.
├── README.md
├── PROTOCOL.md
├── INSTALL.md
├── ARCHITECTURE.md
├── AGENTS.md
├── examples/         # golden protocol fixtures and traces, not truth owners
├── optional-utilities/
└── skills/
```

Expose the frontmatter `name` and `description` from each `skills/*/SKILL.md`.
Agents must use `skills/loom-bootstrap` first unless its ordered bootstrap
references are already loaded in the current context by a harness adapter. Then
hydrate the task-specific skill when relevant.

Inside a Loom-enabled project, the canonical runtime tree is expected to look roughly like this:

```text
.loom/
├── constitution/
│   ├── constitution.md
│   ├── decisions/
│   └── roadmap/
├── initiatives/
├── research/
├── specs/
├── plans/
├── tickets/
├── evidence/
├── critique/
├── wiki/
├── packets/
│   ├── ralph/
│   ├── critique/
│   └── wiki/
└── memory/        # optional
```

## Installation Model

The intended installation pattern is simple:

1. install or expose `skills/` as the Loom package
2. keep skill names/descriptions from `skills/*/SKILL.md` visible
3. use `skills/loom-bootstrap` first unless the same ordered doctrine is already
   loaded by the adapter
4. hydrate the full `skills/<name>/SKILL.md` only when that skill is relevant
5. let the model read templates and references from that skill as needed

Read `INSTALL.md` for the recommended adoption path, native install or
registration commands, and harness-specific caveats.

## Protocol Core And Workflows

The core protocol is the visible graph of canonical owner layers plus durable
support surfaces.

Canonical owner layers:

- constitution
- initiative
- research
- spec
- plan
- ticket
- evidence
- critique
- wiki

Durable support surfaces:

- packet
- memory
- workspace support records

Workflows such as brainstorm, debug, spike, sketch, map, Git-backed isolation,
review, accept, ship, retrospective, repair, and wiki write/audit are
compositions through those layers. They should not create new truth owners
unless a genuinely new kind of truth exists.

Harness adapters expose the skill package through each harness's native skill or
plugin system. They may preload `loom-bootstrap` references where the harness
supports it cleanly, but they do not own semantics. Optional utilities stay under
`optional-utilities/` and are not part of the default protocol install.

## Current Roadmap Direction

The current phase is protocol sharpening, not platform expansion.

The package now includes first-pass surfaces for:

- shared non-ticket status lifecycle grammar
- claim-level coverage from specs through tickets, packets, evidence, and critique
- change classes that guide evidence, critique, and verification posture
- packet freshness and context-budget guidance
- workspace scope aliases for multi-repo or multi-worktree resolution
- Git branch and worktree discipline for Ralph-backed implementation isolation
- named critique risk profiles
- guidance for codebase atlas, debug, spike, sketch, execution-wave, external-reference, ship, golden-example, and retrospective-prevention workflows as routes through existing layers
- golden examples and fixture slices that make the protocol evaluable across harnesses

The next proving step is to exercise those surfaces in real Loom work and
reconcile any stale dogfooding records that still teach older shapes.

## Design Goal

A capable agent should be able to enter a Loom workspace cold and do all of the following without hidden runtime magic:

- determine what layer owns the next truth change
- find the right files with native tools
- scaffold or edit the right record from Markdown templates
- compile a Ralph packet as a Markdown contract
- launch a fresh worker through whatever harness is available
- reconcile the result back into ticket truth
- run adversarial critique
- promote accepted understanding into the wiki
- leave a durable, searchable corpus behind

That is Loom.
