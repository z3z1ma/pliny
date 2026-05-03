---
id: ticket:critfail3
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
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

Make the ticket template locally fail closed for mandatory critique disposition.

# Context

Council finding `NC2-002` found that the ticket template lists critique
disposition statuses but does not locally say mandatory critique cannot close as
`deferred` or `not_required`.

# Why Now

Fresh agents often copy templates before reading every reference. The ticket
template should carry the closure-critical mandatory critique rule directly.

# Scope

- Add a fail-closed note to the ticket template critique disposition section.
- Preserve the distinction between mandatory, recommended, and optional critique.
- Keep ticket-owned finding dispositions separate from critique-owned finding
  states and verdicts.

# Out Of Scope

- Do not change the ticket state machine.
- Do not make recommended critique a hard closure blocker unless a ticket or human
  gate requires it.

# Acceptance Criteria

- ACC-001: Ticket template says mandatory critique remains pending/blocking until
  final critique exists.
- ACC-002: Ticket template says open medium/high mandatory critique findings need
  ticket-owned dispositions before closure.
- ACC-003: Template keeps `deferred` / `not_required` closure-compatible only for
  recommended/optional critique with rationale, not mandatory critique.
- ACC-004: Evidence records before/after critique disposition searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-005`
- `ticket:critfail3#ACC-001`
- `ticket:critfail3#ACC-002`
- `ticket:critfail3#ACC-003`
- `ticket:critfail3#ACC-004`
- `ticket:critfail3#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-005` | pending | pending | open |
| `ticket:critfail3#ACC-001` through `ticket:critfail3#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces are `skills/loom-tickets/templates/ticket.md` and, only if
needed, `skills/loom-tickets/references/acceptance-gate.md`.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: ticket template mandatory critique fail-closed note.
Write boundary: ticket template/acceptance reference if needed, this ticket, one
evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `Critique policy`, `mandatory`, `deferred`,
`not_required`, `Disposition status`, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: ticket template closure gates directly shape ticket acceptance.

Required critique profiles:

- closure-honesty
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

- 2026-05-03T00:56:36Z: Created from council finding `NC2-002`.
