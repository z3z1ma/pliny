---
id: ticket:critph28
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T06:20:11Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-third-pass-follow-up-validation
external_refs: {}
depends_on:
  - ticket:shipacc1
  - ticket:gitstat26
---

# Summary

Make critique packet placeholders consistently safe and quoted.

# Context

The critique packet template uses quoted `<TBD: ...>` form for many fields but
still has some generic or unquoted placeholder shapes.

# Why Now

Critique packets are copied during high-risk review work and should be YAML-safe
until filled.

# Scope

- Quote remaining copyable placeholder values in critique packet frontmatter.
- Prefer `<TBD: ...>` placeholders with explicit replacement instructions.

# Out Of Scope

- Do not change critique packet semantics.
- Do not add a packet validator.

# Acceptance Criteria

- ACC-001: Critique packet copyable frontmatter placeholders use quoted
  `<TBD: ...>` form consistently where YAML scalar safety matters.
- ACC-002: Template still points to current critique packet grammar.
- ACC-003: No critique packet field becomes fake precision or a required runtime.
- ACC-004: Evidence records targeted critique placeholder searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-029`
- `ticket:critph28#ACC-001`
- `ticket:critph28#ACC-002`
- `ticket:critph28#ACC-003`
- `ticket:critph28#ACC-004`
- `ticket:critph28#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-029` | pending | pending | open |
| `ticket:critph28#ACC-001` | pending | pending | open |
| `ticket:critph28#ACC-002` | pending | pending | open |
| `ticket:critph28#ACC-003` | pending | pending | open |
| `ticket:critph28#ACC-004` | pending | pending | open |
| `ticket:critph28#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-critique/templates/critique-packet.md`.

# Blockers

Blocked until `ticket:shipacc1` and packet metadata hardening tickets close.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: critique packet placeholder quoting.
Write boundary: critique packet template only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, placeholder observations, and critique
recommendation.

# Evidence

Expected: targeted searches for unquoted placeholders, `<TBD:`, critique packet
frontmatter, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: critique packet templates are high-copy review surfaces.

Required critique profiles:

- template-safety
- packet-safety
- operator-clarity

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

- `ticket:shipacc1`
- `ticket:gitstat26`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass secondary polish finding.
