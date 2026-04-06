---
{
  "created_at": "2026-04-01T18:07:00Z",
  "id": "decision:0004",
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

Loom skills in this repository remain flat sibling subsystems, and each distributed skill bundle must stay self-contained with its own standalone script committed directly in the skill bundle.

No skill should depend on hidden inheritance from another skill in order to function correctly when loaded.

# Why This Decision Exists

`CONSTITUTION.md` locks in both the flat sibling skill rule and the self-contained distribution rule because they keep subsystem behavior visible, inspectable, and portable across harnesses.

The current repository already implements that choice through top-level skills, skill-local references, and skill-local `scripts/*.py` files that are edited directly rather than generated from a central runtime layer.

# Alternatives Considered

- nested or inheriting skills with hidden parent behavior
- a central runtime package that every loaded skill must import to work correctly
- allowing build assembly to become the true owner of behavior while the skill Markdown stays thin

# Consequences

- every skill should remain understandable from its own `SKILL.md`, references, and bundled scripts
- each skill's CLI behavior should be visible in that skill's own script file
- build assembly remains a distribution mechanism, not a new ontology layer
- future skill additions should preserve flat routing and self-contained operation unless a later constitutional change explicitly reopens this choice

# Supersession

This supersedes any assumption that hidden skill inheritance, central runtime coupling, or assembly-time indirection may become the normal way skills gain their operating behavior.
