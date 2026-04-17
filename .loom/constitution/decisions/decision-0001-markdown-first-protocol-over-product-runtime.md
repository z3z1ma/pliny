---
id: decision:0001
kind: decision
status: active
created_at: 2026-04-01T17:43:00Z
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

Loom in this repository is defined first as a visible Markdown protocol corpus
and operator method rather than as a bundled runtime, service, product CLI, or
helper-script pack.

The repository itself should remain the inspectable source of system meaning:
rules, skills, templates, references, canonical records, packets, and optional
wrappers should be understandable from what is committed here.

# Why This Decision Exists

The rewrite intentionally removes shipped Python helpers and moves record
creation, packet compilation, validation guidance, and graph inspection recipes
into visible Markdown.

That keeps Loom portable across harnesses and makes the durable asset the work
discipline itself rather than one implementation shell.

# Alternatives Considered

- treating Loom primarily as a monolithic CLI with Markdown as an export or
  storage format
- introducing a long-running orchestration service or canonical database as the
  center of the system
- shipping helper CLIs as part of the core bundle instead of teaching the
  method directly in rules, skills, templates, and references
- hiding shared behavior behind runtime indirection instead of making the
  protocol surfaces visible in-repo

# Consequences

- visible Markdown rules and records outrank packaging or runtime convenience
- no shipped Python scripts are required for the core Loom package
- templates, native Unix recipes, and direct record editing are the primary
  mechanism for scaffolding and inspection
- future adapters, wrappers, or accelerators stay derivative unless a later
  constitutional change explicitly promotes them
- downstream specs, plans, wiki pages, and tickets should explain how they
  align with the protocol corpus instead of assuming a hidden engine will fill
  the gap

# Supersession

This supersedes any assumption that Loom's primary durable artifact should be a
package, service, helper runtime, or CLI whose behavior outranks the Markdown
corpus.
