---
id: 20260209203339-hydrate-wikilinks-on-memory-writes-e60e31b9
title: Hydrate wikilinks on memory writes
tags:
- links
- memory
scopes:
- kind: file
  raw: src/agent_loom/memory/hydrate.py
  path: src/agent_loom/memory/hydrate.py
visibility: shared
status: active
created_at: "2026-02-09T20:33:39Z"
updated_at: "2026-02-09T20:33:39Z"
---

Memory notes now hydrate Obsidian-style double-bracket links at write-time (add/edit).

Behavior:
- On add/edit, the note body is scanned for double-bracket links outside fenced code blocks.
- Each link target is normalized to a slug and resolved to an existing note id when possible.
- If no match exists, Loom auto-creates a stub note (same visibility as the source note) to obtain a canonical timestamped id, then rewrites the original note to point at it.
- Rewrites use alias form so the human-readable display remains stable (target becomes the canonical note id; display remains the concept name).
- JSON output includes a hydration section with rewrites + any created stub notes, so an agent can learn which ids were generated.
