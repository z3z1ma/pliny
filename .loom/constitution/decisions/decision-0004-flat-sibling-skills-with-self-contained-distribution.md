---
id: decision:0004
kind: decision
status: active
created_at: 2026-04-01T18:07:00Z
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

Loom skills in this repository remain flat sibling subsystems, and each
distributed skill bundle must stay self-contained through its own `SKILL.md`,
references, and templates rather than through bundled scripts or hidden
inheritance.

No skill should depend on hidden inheritance from another skill in order to
function correctly when loaded.

# Why This Decision Exists

The rewrite assumes a stronger model that can read, search, scaffold, and edit
records directly, so the skill bundle should teach the method rather than ship
one required code path.

Flat sibling skills and self-contained Markdown surfaces keep subsystem
behavior visible, inspectable, and portable across harnesses.

# Alternatives Considered

- nested or inheriting skills with hidden parent behavior
- a central runtime package that every loaded skill must import to work
  correctly
- bundling per-skill scripts as the true owner of behavior while the skill
  Markdown stays thin
- allowing build assembly to become the true owner of behavior while the skill
  Markdown stays thin

# Consequences

- every skill should remain understandable from its own `SKILL.md`,
  references, and templates
- no skill should require bundled code to express its normal record grammar,
  packet shape, or operating flow
- optional wrappers remain secondary transport or convenience layers, not the
  skill's true source of behavior
- build assembly remains a distribution mechanism, not a new ontology layer
- future skill additions should preserve flat routing and self-contained
  operation unless a later constitutional change explicitly reopens this choice

# Supersession

This supersedes any assumption that hidden skill inheritance, central runtime
coupling, or assembly-time indirection may become the normal way skills gain
their operating behavior.
