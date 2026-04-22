# Loom - Markdown-Native Control Plane

Loom is a harness-agnostic protocol for long-horizon AI knowledge work.

It treats the filesystem as the interface, Markdown as the durable medium, and
fresh-context packet execution as the default way to do bounded implementation,
review, and knowledge-compilation work.

This package is intentionally **not** a runtime, service, daemon, MCP, or product CLI.

It ships:

- always-on `rules/` that teach the model how Loom thinks and how Loom must be used
- on-demand `skills/` that teach the model how to operate each subsystem in detail
- optional `commands/` wrappers for harnesses that support slash-command style prompts
- Markdown templates and query recipes instead of bundled Python helpers
- a cohesive explanation layer: **Loom Wiki**

Loom is best understood as a source-of-truth type system plus a transaction
protocol for fallible AI workers. The workers are disposable. The graph is
durable. The parent is the transaction coordinator. Tickets are the execution
ledger. Evidence is the proof store. Critique is the verifier. Wiki is the
accepted explanation layer.

## The Core Shape

Loom has three primitives:

- **layers**: typed owners for different kinds of truth
- **loops**: outer-loop shaping and inner-loop execution
- **packets**: bounded contracts for fresh-context work

The layer model is the type system:

| Layer | Owns |
| --- | --- |
| constitution | durable identity, principles, hard constraints, precedent |
| initiative | strategic outcome |
| research | investigated evidence, options, rejected paths, null results |
| spec | intended behavior and acceptance contract |
| plan | sequencing and rollout strategy |
| ticket | live execution state |
| packet | bounded child-worker contract |
| evidence | proof artifacts |
| critique | adversarial findings and verdicts |
| wiki | accepted explanation |
| memory | optional support context only |

The rule that keeps the graph coherent is simple: truth ownership is by layer,
not by recency.

For software work, the codebase owns current implementation reality while specs
and tickets own intended behavior. Evidence bridges the two, and critique
judges whether the bridge is strong enough.

## The Two Loops

### Outer loop

The outer loop scopes and re-scopes the work.

Its normal progression is:

`constitution -> initiative -> research/spec -> plan -> ticket`

The four most important binding layers are:

`constitution -> initiative -> plan -> ticket`

Research and specs are optional amplifiers. They tighten evidence and behavior when the work needs them, but they do not replace the backbone.

### Inner loop

The inner loop is **Ralph**.

Ralph is one bounded packet, one fresh worker, one iteration, one reconciliation
pass.

A parent agent compiles a packet, launches or delegates one fresh-context execution step, receives a bounded outcome, merges truth back into the ticket, and either continues, stops, escalates, or routes into critique/wiki.

Critique and Wiki are Ralph variants with different output contracts.

The deeper invariant is ownership-preserving mutation: every durable claim,
behavior, proof, risk, and explanation lands in the artifact that owns that
kind of truth.

## Repository Layout

```text
.
├── README.md
├── INSTALL.md
├── ARCHITECTURE.md
├── AGENTS.md
├── Makefile
├── commands/         # optional harness-wrapper prompt files
├── examples/         # golden protocol fixtures and traces, not truth owners
├── optional-utilities/
├── rules/
└── skills/
```

Load `rules/*.md` in order as always-on doctrine. Expose the frontmatter
`name` and `description` from each `skills/*/SKILL.md`, then hydrate the full
skill only when relevant.

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
├── critique/
├── wiki/
├── packets/
│   ├── ralph/
│   ├── critique/
│   └── wiki/
├── evidence/
└── memory/        # optional
```

## Installation Model

The intended installation pattern is simple:

1. load `rules/*.md` as always-on context, in numeric order
2. keep skill names/descriptions from `skills/*/SKILL.md` always visible
3. hydrate the full `skills/<name>/SKILL.md` only when that skill is relevant
4. let the model read templates and references from that skill as needed

Read `INSTALL.md` for the recommended adoption path.

## Command Map

The optional `commands/` surface groups the same protocol routes into familiar
operator commands:

| Phase | Commands |
| --- | --- |
| Orient | `/loom-orient`, `/loom-status` |
| Shape | `/loom-brainstorm`, `/loom-research`, `/loom-spike`, `/loom-sketch`, `/loom-spec`, `/loom-decide`, `/loom-plan`, `/loom-ticket`, `/loom-map` |
| Execute | `/loom-work`, `/loom-debug` |
| Verify | `/loom-review`, `/loom-accept` |
| Assimilate | `/loom-wiki`, `/loom-retrospective` |
| Package | `/loom-ship` |
| Maintain | `/loom-repair` |

Commands are convenience wrappers. They do not replace the rules, skills, or
canonical records.

## Product Tiers

Loom is split by role:

- **Protocol kernel**: rules, workspace, records, constitution, tickets, Ralph,
  critique, wiki
- **Dev pack**: initiatives, research, specs, plans, debugging, spikes,
  codebase atlas, shipping
- **Maintenance guidance**: status, repair, acceptance, validation, conformance
- **Harness adapters**: optional command wrappers and installer translations
- **Optional utilities**: local helper skills under `optional-utilities/`, not
  installed as part of the default protocol surface

## Current Roadmap Direction

The current phase is protocol sharpening, not platform expansion.

The package now includes first-pass surfaces for:

- shared non-ticket status lifecycle grammar
- claim-level coverage from specs through tickets, packets, evidence, and critique
- change classes that guide evidence, critique, and verification posture
- packet freshness and context-budget guidance
- workspace scope aliases for multi-repo or multi-worktree resolution
- named critique risk profiles
- codebase atlas, debug, spike, sketch, execution-wave, external-reference, ship, and retrospective-prevention workflows as routes through existing layers
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
