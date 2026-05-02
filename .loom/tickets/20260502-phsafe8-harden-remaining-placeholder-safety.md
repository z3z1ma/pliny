---
id: ticket:phsafe8
kind: ticket
status: ready
change_class: record-hygiene
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T22:03:13Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
external_refs: {}
depends_on:
  - ticket:accspec6
  - ticket:sibpkt7
---

# Summary

Harden remaining copyable placeholders and accepted-status defaults that can look
save-ready.

# Context

Council finding `NC-008` found remaining template/example surfaces that may still
save unsafe placeholders or accepted statuses over placeholder content.

# Why Now

Templates should fail closed when copied. Placeholder text should be obviously
unsafe to save as project truth.

# Scope

- Targeted scan of `skills/**/templates` and relevant examples in `skills/**/references`.
- Harden remaining copyable `TBD`, `Replace with`, or accepted-status placeholder
  defaults that can look valid.
- Preserve useful instructional examples.

# Out Of Scope

- Do not rewrite all templates for style.
- Do not remove examples that are clearly non-copyable instruction.

# Acceptance Criteria

- ACC-001: Remaining unsafe placeholders in touched surfaces are fail-closed.
- ACC-002: Accepted/final statuses are not defaulted over placeholder content.
- ACC-003: Template usefulness is preserved.
- ACC-004: Evidence records placeholder/status searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-008`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-008` | pending | pending | open |
| `ticket:phsafe8#ACC-001` through `ticket:phsafe8#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-wiki/templates/index.md`,
`skills/loom-bootstrap/references/06-filesystem-and-tooling.md`, and
`skills/loom-initiatives/templates/initiative.md`, plus any targeted scan results.

# Blockers

Depends on `ticket:accspec6` and `ticket:sibpkt7`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: ralph

Bounded iteration: remaining placeholder/accepted-status safety cleanup.
Write boundary: targeted template/reference wording, this ticket, one evidence
record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `TBD`, `Replace with`, placeholder accepted
statuses, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: unsafe placeholders can create false project truth.

Required critique profiles:

- template-safety
- records-grammar
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

- `ticket:accspec6`
- `ticket:sibpkt7`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-008`.
