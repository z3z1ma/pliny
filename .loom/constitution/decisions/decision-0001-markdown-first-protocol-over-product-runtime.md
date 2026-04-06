---
{
  "created_at": "2026-04-01T17:43:00Z",
  "id": "decision:0001",
  "kind": "decision",
  "links": {
    "roadmap": [
      "roadmap:bootstrap-the-markdown-first-protocol-corpus"
    ]
  },
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "active",
  "updated_at": "2026-04-06T06:53:44Z"
}
---

# Decision

Loom in this repository is defined first as a visible Markdown protocol corpus rather than as a monolithic runtime, service, or product CLI.

The repository itself should remain the inspectable source of system meaning: rules, skills, canonical records, packets, and helper behavior should be understandable from what is committed here.

# Why This Decision Exists

`CONSTITUTION.md` locks the repository onto a Markdown-first, harness-agnostic direction where the durable asset is the work discipline rather than one implementation shell.

The current codebase already reflects that choice through `rules/`, `skills/`, canonical `.loom/` subtrees, and committed standalone skill-local CLIs instead of a central runtime product.

# Alternatives Considered

- treating Loom primarily as a monolithic CLI with Markdown as an export or storage format
- introducing a long-running orchestration service or canonical database as the center of the system
- hiding shared behavior behind runtime indirection instead of making the protocol surfaces visible in-repo

# Consequences

- visible Markdown rules and records outrank packaging or runtime convenience
- committed skill-local CLIs are the shipped helper layer rather than a hidden generated runtime
- future adapters and accelerators stay derivative unless a later constitutional change explicitly promotes them
- downstream specs, plans, docs, and tickets should explain how they align with the protocol corpus instead of assuming a hidden engine will fill the gap

# Supersession

This supersedes any assumption that Loom's primary durable artifact should be a package, service, or CLI whose behavior outranks the Markdown corpus.
