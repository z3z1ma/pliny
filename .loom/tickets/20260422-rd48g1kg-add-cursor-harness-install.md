---
id: ticket:rd48g1kg
kind: ticket
status: closed
change_class: release-packaging
created_at: 2026-04-22T20:51:34Z
updated_at: 2026-04-28T18:47:27Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:harness-install-surfaces
  evidence:
    - evidence:cursor-harness-install-validation
external_refs:
  cursor_docs:
    - https://cursor.com/docs/rules
    - https://cursor.com/docs/commands
    - https://cursor.com/changelog/2-4
depends_on: []
---

# Summary

Add Cursor as a supported harness for the existing Makefile installer.

# Context

The installer already maps Loom's shipped `rules/`, `skills/`, and optional
`commands/` into several harness-specific user config surfaces. Cursor has
distinct surfaces for project rules, commands, and Agent Skills, so the adapter
needs an honest mapping rather than a copy of another harness shape.

# Why Now

The operator asked for Cursor support in the existing `make install
harness=<name>` flow after researching how Cursor handles rules, skills, and
commands.

# Scope

- research Cursor rule, skill, and command surfaces
- add `harness=cursor` support to `scripts/install-loom.sh`
- include Cursor in aggregate `harness=all`
- document the Cursor mapping in `INSTALL.md`
- add an adapter fixture that describes the expected Cursor install surface
- validate install and uninstall in a temporary `HOME`

# Non-goals

- do not mutate Cursor settings beyond the managed Loom block in User Rules
- do not add a required runtime or installer dependency
- do not change Loom's core rule, skill, or command semantics
- do not install optional utility skills as part of the default protocol surface

# Acceptance Criteria

- `make install harness=cursor` creates the expected Cursor user-level Loom
  surfaces under a temporary `HOME`
- `make uninstall harness=cursor` removes only Loom-managed Cursor surfaces
- `make install harness=all` includes Cursor without breaking existing harnesses
- Cursor install documentation reflects the researched mapping
- command wrappers remain adapter surfaces rather than protocol owners

# Coverage

Covers:
- research:harness-install-surfaces#cursor-install-surface

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| research:harness-install-surfaces#cursor-install-surface | evidence:cursor-harness-install-validation | none required | supported |

# Execution Notes

Cursor project rules use `.cursor/rules/*.mdc`, but global always-on rules are
Cursor User Rules. The installer should put the Loom rule corpus into a managed
User Rules block and keep skills and commands in their native Cursor surfaces.

# Evidence

Evidence gathered:

- evidence:cursor-harness-install-validation

# Critique Disposition

Risk class: medium

Required critique profiles:
- operator-clarity

Findings:
- none

Status: not_required

# Wiki Disposition

No wiki promotion expected. `INSTALL.md`, the research record, and the adapter
fixture should be enough durable explanation for this packaging change.

# Acceptance Decision

Accepted by: operator
Accepted at: 2026-04-28T18:47:27Z
Basis: Operator accepted Cursor harness install support after linked validation evidence and critique disposition.
Residual risks: Cursor's plugin/rules/skills surfaces may evolve; future adapter changes should revalidate against current Cursor docs.

# Dependencies

Cursor's support for Agent Skills and global commands should remain compatible
with the documented or support-described surfaces.

# Journal

- 2026-04-22: created ticket and started implementation of Cursor harness
  install support.
- 2026-04-22: added Cursor install/uninstall support, documentation, adapter
  fixture, and validation evidence. Left ticket pending final acceptance.
- 2026-04-28T18:47:27Z: Operator accepted the completed work and closed the ticket.
