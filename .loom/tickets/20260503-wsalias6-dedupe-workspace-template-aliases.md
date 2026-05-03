---
id: ticket:wsalias6
kind: ticket
status: ready
change_class: record-hygiene
risk_class: low
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T00:56:36Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
external_refs: {}
depends_on: []
---

# Summary

Deduplicate `repo_aliases` in the workspace template so frontmatter is the single
authoritative alias surface.

# Context

Council finding `NC2-006` found the workspace template duplicates `repo_aliases`
in frontmatter and body YAML, which can drift if a fresh agent edits only one.

# Why Now

Workspace metadata supports scope recovery. Duplicated alias truth in a template
undermines the frontmatter/body boundary.

# Scope

- Keep frontmatter `repo_aliases` authoritative.
- Replace or simplify the body YAML duplicate with prose that points to
  frontmatter.
- Preserve workspace support-only truth boundaries.

# Out Of Scope

- Do not change workspace ID shape or scope semantics.
- Do not make workspace metadata canonical project truth.

# Acceptance Criteria

- ACC-001: Workspace template no longer duplicates `repo_aliases` as a second YAML
  body block.
- ACC-002: Workspace template clearly points readers to frontmatter for aliases.
- ACC-003: Workspace notes still say aliases do not own project behavior,
  strategy, or execution truth.
- ACC-004: Evidence records before/after workspace template searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-008`
- `ticket:wsalias6#ACC-001`
- `ticket:wsalias6#ACC-002`
- `ticket:wsalias6#ACC-003`
- `ticket:wsalias6#ACC-004`
- `ticket:wsalias6#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-008` | pending | pending | open |
| `ticket:wsalias6#ACC-001` through `ticket:wsalias6#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surface is `skills/loom-workspace/templates/workspace.md`.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: workspace template alias dedupe.
Write boundary: workspace template, this ticket, one evidence record, one
critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `repo_aliases`, body YAML alias blocks, and
`git diff --check`.

# Critique Disposition

Risk class: low

Critique policy: mandatory

Policy rationale: user instruction requires oracle critique for every ticket;
template duplication can create graph drift.

Required critique profiles:

- template-safety
- owner-boundary

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Pending after critique.

# Wiki Disposition

Pending retrospective decision after critique.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-006`.
