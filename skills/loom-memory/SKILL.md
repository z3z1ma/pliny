---
name: loom-memory
description: "Maintain optional support memory without letting it become shadow truth. Use for hot memory, observations, entities, action items, and memory housekeeping when those support continuity, but keep canonical project truth in the main Loom layers."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: memory
---

# loom-memory

Memory is optional support context.

It exists to preserve useful continuity without letting the support layer become a second project ledger.

## What This Skill Owns

- hot memory
- observations
- entities
- action items
- memory housekeeping and retrieval discipline

## The Boundary

Memory helps the agent remember.
Memory does not outrank canonical Loom records.

If a fact is really project truth, put it in the right Loom owner layer.

## Use This Skill When

- the project benefits from small support-context files
- an entity or observation should be remembered outside the canonical execution graph
- hot memory needs pruning
- memory retrieval and linking need maintenance

## Do Not Use This Skill When

- the fact belongs in constitution, research, spec, plan, ticket, critique, wiki, or evidence
- memory is starting to act like a secret source of truth
- you are trying to avoid updating the real owner record

## Memory Domains

This package assumes two default domains:

- `system/`
- `user/`

You may add more if a project has a real reason, but do not sprawl casually.

## L0 Header Rule

Every active memory file should start with a one-line `<!-- L0: ... -->` header.

That allows cheap scanning before deep reading.

## Done Means

- the memory fact is stored in the right memory file
- canonical truth still lives in the canonical Loom layer
- memory remains small, linked, and pruned

## Read In This Order

Read immediately for memory work:

1. `references/memory-model.md` when deciding whether a fact belongs in memory
   or a canonical owner layer.

Then read conditionally:

2. `references/retrieval.md` when searching memory without letting it become
   shadow truth.
3. `references/housekeeping.md` when pruning stale support context or
   reconciling memory against canonical records.
4. The relevant template only when creating the specific memory shape requested.
