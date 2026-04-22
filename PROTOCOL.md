# Loom Protocol

Loom is a Markdown-native protocol for AI-mediated software work.

It is not a runtime. The durable product is the record grammar and operating
discipline that lets agents work over one visible graph.

## Invariant Grammar

Loom is built from seven primitives:

- Owners
- Claims
- Packets
- Evidence
- Critique
- Acceptance
- Promotion

These primitives are enough to express planning, implementation, debugging,
review, release packaging, retrospectives, codebase mapping, and wiki
synthesis without adding new truth-owner layers for each workflow.

## Transaction Shape

Meaningful software work should leave behind:

```text
intent
owner
scope
contract
write boundary
proof
critique
acceptance
promotion
```

The packet is the bounded contract. The ticket is the live execution ledger.
Evidence records proof. Critique records challenge. Wiki records accepted
explanation. Retrospective promotes lessons into their owner layers.

## Core Protocol And Workflows

The core protocol is the persisted owner graph.

Core protocol layers are the persisted surfaces that own truth:

```text
constitution
initiative
research
spec
plan
ticket
packet
evidence
critique
wiki
memory
workspace support records
```

Workflows are compositions through those layers:

```text
brainstorm
debug
spike
sketch
map
work
review
accept
ship
retrospective
repair
wiki write/audit
```

A workflow can be useful without becoming a new ontology. It should route into
the owner graph and leave truth in the layer that owns it.

Harness adapters may install, translate, wrap, or invoke Loom. They must not
define Loom truth.

## Check Principle

Markdown protocol first. Optional validators second.

A validator or installer can project Loom state, but it must not become the
authority for Loom semantics.
