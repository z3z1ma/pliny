---
id: ticket:claimmx5
kind: ticket
status: ready
change_class: protocol-authority
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

Add local claim matrix status guidance to ticket template copy surfaces.

# Context

Council finding `NC2-005` found that the ticket template's claim matrix leaves the
`Status` column unconstrained locally, inviting invented values such as `done` or
`passed`.

# Why Now

The canonical claim matrix vocabulary exists in claim coverage, but agents copying
the ticket template should see the allowed values at the point of edit.

# Scope

- Add a concise pointer in the ticket template to canonical claim matrix status
  values.
- Keep the canonical vocabulary owned by `skills/loom-records/references/claim-coverage.md`.
- Avoid duplicating long claim-coverage doctrine in the ticket template.

# Out Of Scope

- Do not change claim coverage status meanings.
- Do not add runtime validation.

# Acceptance Criteria

- ACC-001: Ticket template names or points to allowed claim matrix statuses:
  `open`, `supported`, `supported_pending_review`, `challenged`,
  `accepted_risk`, and `superseded`.
- ACC-002: Template still allows removing the matrix or writing `None - reason`
  when no matrix applies.
- ACC-003: Claim coverage remains the canonical vocabulary owner.
- ACC-004: Evidence records before/after claim matrix searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-007`
- `ticket:claimmx5#ACC-001`
- `ticket:claimmx5#ACC-002`
- `ticket:claimmx5#ACC-003`
- `ticket:claimmx5#ACC-004`
- `ticket:claimmx5#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-007` | pending | pending | open |
| `ticket:claimmx5#ACC-001` through `ticket:claimmx5#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces are `skills/loom-tickets/templates/ticket.md` and,
possibly, a short backlink in claim coverage if needed.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: ticket template claim matrix status guidance.
Write boundary: ticket template/claim coverage if needed, this ticket, one
evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `Claim Matrix`, allowed status values, and
`git diff --check`.

# Critique Disposition

Risk class: low

Critique policy: mandatory

Policy rationale: user instruction requires oracle critique for every ticket;
template status vocabulary affects future acceptance consistency.

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

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-005`.
