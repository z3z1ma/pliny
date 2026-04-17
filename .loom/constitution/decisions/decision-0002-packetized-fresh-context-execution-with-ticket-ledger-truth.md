---
id: decision:0002
kind: decision
status: active
created_at: 2026-04-01T17:44:00Z
updated_at: 2026-04-17T23:48:34Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
---

# Decision

Bounded execution in Loom should happen through packetized fresh-context child
iterations, while tickets remain the sole canonical ledger of live execution
state.

Packets and evidence support bounded work, replayability, and proof, but they
must not become shadow truth that replaces the canonical record graph.

# Why This Decision Exists

The rewrite keeps the same execution discipline while removing helper-script
dependence: the parent now authors the packet contract directly from templates
and visible guidance instead of relying on a compiler CLI.

That keeps scope, provenance, and reconciliation explicit and inspectable.

# Alternatives Considered

- allowing long-lived transcripts to act as the primary execution context
  instead of curated packets
- treating packets, evidence, or plan documents as the live execution ledger
- allowing child iterations to infer write scope or completion without explicit
  packet and parent reconciliation contracts

# Consequences

- parent contexts own workflow judgment, scope resolution, packet compilation,
  and reconciliation
- child contexts own only bounded work inside the packet contract
- Ralph, critique, and wiki flows should prefer fresh harness contexts
- no outcome should be treated as complete until canonical records and evidence
  reflect the result truthfully
- ticket, critique, wiki, and evidence records must stay aligned so no second
  ledger emerges

# Supersession

This supersedes any assumption that long-lived transcripts, packet artifacts,
evidence files, or plan notes can act as the live execution ledger in place of
ticket truth.
