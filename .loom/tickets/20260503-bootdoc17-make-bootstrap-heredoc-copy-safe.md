---
id: ticket:bootdoc17
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
---

# Summary

Make the bootstrap here-doc file creation example copy-safe.

# Context

Bootstrap tooling warns placeholders must be replaced, but its research here-doc
example still writes to a literal `.loom/research/<slug>.md` path if copied.

# Why Now

Bootstrap examples are high-leverage copy surfaces for fresh agents.

# Scope

- Replace the literal placeholder path with a safer variable pattern.
- Keep a local placeholder scan near the example.
- Preserve Markdown-native shell guidance without adding helpers.

# Out Of Scope

- Do not add a command wrapper or runtime validator.
- Do not expand bootstrap into a full template catalog.

# Acceptance Criteria

- ACC-001: Bootstrap here-doc example no longer writes to literal `<slug>` path.
- ACC-002: Example includes or points to a local placeholder scan for the saved
  file.
- ACC-003: Bootstrap remains concise and Markdown-native.
- ACC-004: Evidence records targeted copy-safety searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-018`
- `ticket:bootdoc17#ACC-001`
- `ticket:bootdoc17#ACC-002`
- `ticket:bootdoc17#ACC-003`
- `ticket:bootdoc17#ACC-004`
- `ticket:bootdoc17#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-018` | pending | pending | open |
| `ticket:bootdoc17#ACC-001` | pending | pending | open |
| `ticket:bootdoc17#ACC-002` | pending | pending | open |
| `ticket:bootdoc17#ACC-003` | pending | pending | open |
| `ticket:bootdoc17#ACC-004` | pending | pending | open |
| `ticket:bootdoc17#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-bootstrap/references/06-filesystem-and-tooling.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: copy-safe bootstrap here-doc example.
Write boundary: bootstrap filesystem/tooling reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, copy-safety observations, and critique
recommendation.

# Evidence

Expected: targeted searches for `<slug>`, path variable, placeholder scan, and
`git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: bootstrap examples are copied by cold agents.

Required critique profiles:

- template-safety
- operator-clarity
- workflow-boundary

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

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 6.
