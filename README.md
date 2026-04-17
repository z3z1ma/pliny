# Loom — Markdown-Native Protocol

Loom is a harness-agnostic protocol for long-horizon AI work.

It treats the filesystem as the interface, Markdown as the durable medium, and fresh-context packet execution as the default way to do bounded implementation, review, and knowledge-compilation work.

This package is intentionally **not** a runtime, service, daemon, MCP, or product CLI.

It ships:

- always-on `rules/` that teach the model how Loom thinks and how Loom must be used
- on-demand `skills/` that teach the model how to operate each subsystem in detail
- Markdown templates and query recipes instead of bundled Python helpers
- a cohesive replacement for the old docs layer: **Loom Wiki**

## The Core Shape

Loom has two loops.

### Outer loop

The outer loop scopes and re-scopes the work.

Its normal progression is:

`constitution -> initiative -> research/spec -> plan -> ticket`

The four most important binding layers are:

`constitution -> initiative -> plan -> ticket`

Research and specs are optional amplifiers. They tighten evidence and behavior when the work needs them, but they do not replace the backbone.

### Inner loop

The inner loop is **Ralph**.

Ralph is one bounded packet, one fresh worker, one iteration, one reconciliation pass.

A parent agent compiles a packet, launches or delegates one fresh-context execution step, receives a bounded outcome, merges truth back into the ticket, and either continues, stops, escalates, or routes into critique/wiki.

Critique and Wiki are Ralph variants with different output contracts.

## Repository Layout

```text
.
├── README.md
├── INSTALL.md
├── ARCHITECTURE.md
├── RULES.md
├── SKILLS.md
├── MIGRATION.md
├── rules/
└── skills/
```

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

1. load `rules/*.md` as always-on context, in order
2. keep `SKILLS.md` or the skill names/descriptions always visible
3. hydrate the full `skills/<name>/SKILL.md` only when that skill is relevant
4. let the model read templates and references from that skill as needed

Read `INSTALL.md` for the recommended adoption path.

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
