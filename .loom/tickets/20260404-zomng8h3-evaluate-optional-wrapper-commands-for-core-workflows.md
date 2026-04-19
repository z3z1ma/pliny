---
id: ticket:zomng8h3
kind: ticket
status: closed
created_at: 2026-04-04T23:57:49Z
updated_at: 2026-04-19T23:34:12Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:prove-core-loom-workflow
  plan:
    - plan:bootstrap-core-workflow-backlog
  spec:
    - spec:minimum-proven-core-workflow-surface
  ticket:
    - ticket:1ypcbj0m
depends_on:
  - ticket:1ypcbj0m
---

# Summary

Evaluate and, only if justified, keep or add the smallest optional
harness-wrapper command surface for canonical Loom workflows so the repository's
wrapper prompts stay useful without becoming part of Loom core.

# Context

The rewrite moved command wrappers out of the protocol core. The repository may
still keep top-level `commands/` prompts as harness sugar, but the core method
must be legible from rules, skills, templates, and canonical records.

That means this ticket is no longer about expanding a required command surface.
It is about deciding, after the proof slice, whether any wrapper commands still
earn their complexity and how they should be framed truthfully.

# Why Now

Once `ticket:1ypcbj0m` proves one real workflow slice, the next highest-leverage
usability question is whether the repo should keep a small optional wrapper
surface and, if so, what the smallest honest set looks like.

# Scope

- use the result of `ticket:1ypcbj0m` to judge whether wrapper commands help
  operator discovery enough to justify their maintenance cost
- if wrappers are justified, keep or add only a minimal set under top-level
  `commands/`
- ensure every retained wrapper remains a pure Markdown prompt definition that
  routes to the correct owning skill and generic `.loom/...` paths only
- align any retained wrappers with the rewrite-era vocabulary and with the
  owning skill docs

# Non-goals

- do not make command wrappers part of the Loom protocol core
- do not create wrapper commands for every skill just for symmetry
- do not duplicate full skill manuals inside wrapper files
- do not point operators at build-only, source-only, or non-package-local paths

# Acceptance Criteria

- the ticket records a truthful decision about whether wrapper commands are
  still justified after the proof slice
- if wrappers are retained, `commands/` contains only a small, clearly optional
  set that is consistent with the owning skills and templates
- wrapper guidance uses the current YAML, `wiki`, `packets`, and `evidence`
  vocabulary where relevant
- no retained wrapper implies that the core Loom workflow depends on wrappers to
  function

# Execution Notes

1. Use the result of `ticket:1ypcbj0m` to judge the smallest stable wrapper set,
   including the possibility that no expansion is needed.
2. Update only the wrapper files that genuinely help discovery.
3. Reconcile any affected references so the wrapper surface is useful and not
   contradictory.
4. Manually compare the wrapper prompts against the owning skills and current
   workspace tree.
5. Reconcile the ticket with the accepted wrapper posture and any remaining
   follow-up scope.

# Evidence

No wrapper decision evidence exists yet.

Expected evidence for this ticket includes:

- manual comparison of retained wrapper prompts against the owning skill docs
- inspection that retained wrappers point at generic `rules/`, `skills/`, and
  `.loom/...` paths rather than retired script-era surfaces
- a truthful ticket journal showing whether wrappers were kept, narrowed, or
  left unchanged

# Critique Disposition

Critique is optional unless the wrapper decision materially changes how future
operators are expected to enter Loom.

# Wiki Disposition

Wiki follow-through is not expected unless the wrapper decision reveals a wider
accepted workflow pattern worth preserving beyond the wrapper files themselves.

# Dependencies

- `ticket:1ypcbj0m` should land first or at least narrow the honest wrapper set
- the repository's current optional wrapper-file style under `commands/`
- the owning rule and skill surfaces that describe the core operator path

# Journal

- 2026-04-04: created `ticket:zomng8h3` as the proposed follow-up for turning
  the proved core workflow path into a discoverable command surface.
- 2026-04-17: narrowed the ticket so wrapper commands are now explicitly
  optional harness sugar rather than a required core-protocol milestone.
- 2026-04-19: closed per user confirmation that this ticket is completed.
