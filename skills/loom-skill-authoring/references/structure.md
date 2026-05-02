# Recommended Structure

```text
skills/<skill-name>/
├── SKILL.md
├── references/
└── templates/
```

Use `templates/` only when the skill really owns an artifact shape.

## SKILL.md frontmatter

Every Loom skill should include:

- `name`: the directory-level skill name
- `description`: the activation description; start with the situation that
  should cause an agent to load the skill and include the owner boundary when
  ambiguity is likely
- `compatibility`: the broad protocol/runtime assumptions, usually
  `Markdown-native, script-free Loom protocol.` for core Loom skills
- `metadata.skill_kind`: the kind of skill surface, not a project-truth owner
  claim

Use `metadata.skill_kind` to describe the skill surface without confusing it
with owner-layer truth. Common values include:

- `owner-layer` for a canonical Loom truth owner such as tickets, specs,
  evidence, critique, wiki, or research
- `workflow` for a bounded procedure that routes truth into existing owners
- `workflow-coordinator`, `control-plane`, `inner-loop`, `shared-grammar`,
  `support-layer`, `bootstrap`, or `authoring` when those more specific surfaces
  match the skill boundary

Owner-layer skills should name `metadata.owns_layer`, and the value should be the
canonical layer the skill owns. Support-layer skills may also name
`metadata.owns_layer` when they own a named non-canonical support layer such as
memory; that value does not make the support layer canonical truth. Workflow,
workflow-coordinator, shared-grammar, and authoring skills should route to owner
layers instead of claiming `metadata.owns_layer`.

Use `references/` for:

- shape details
- review questions
- deeper nuance
- examples that should not bloat the main skill file
