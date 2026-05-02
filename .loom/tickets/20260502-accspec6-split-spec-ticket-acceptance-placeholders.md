---
id: ticket:accspec6
kind: ticket
status: ready
change_class: protocol-authority
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
  - ticket:tkrout5
---

# Summary

Split ticket acceptance placeholders between spec-owned acceptance and
ticket-local `ACC-*` criteria.

# Context

Council finding `NC-006` found ticket acceptance placeholders that encourage local
`ACC-*` creation even when a spec owns the reusable acceptance contract.

# Why Now

Ticket-local acceptance is useful, but specs own reusable behavior contracts.
Copied tickets should not blur that boundary.

# Scope

- Update ticket template acceptance guidance to show spec-owned and ticket-local
  branches.
- Keep `ACC-*` placeholders only in the ticket-local branch.
- Align claim coverage reference wording if needed.

# Out Of Scope

- Do not require every ticket to have a spec.
- Do not remove ticket-local acceptance for no-spec work.

# Acceptance Criteria

- ACC-001: Ticket template distinguishes spec-owned acceptance from ticket-local
  acceptance.
- ACC-002: Ticket-local `ACC-*` placeholders are not presented as the default when
  a spec owns acceptance.
- ACC-003: Claim coverage guidance stays aligned with ticket/spec boundaries.
- ACC-004: Evidence records acceptance-placeholder searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-006`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-006` | pending | pending | open |
| `ticket:accspec6#ACC-001` through `ticket:accspec6#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-tickets/templates/ticket.md` and
`skills/loom-records/references/claim-coverage.md`.

# Blockers

Depends on `ticket:tkrout5`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: ralph

Bounded iteration: acceptance placeholder branch cleanup.
Write boundary: targeted ticket template/claim coverage wording, this ticket, one
evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `ACC-*`, spec-owned acceptance, ticket-local
acceptance, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: acceptance ownership ambiguity can corrupt downstream closure.

Required critique profiles:

- owner-boundary
- records-grammar
- closure-honesty

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

- `ticket:tkrout5`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-006`.
