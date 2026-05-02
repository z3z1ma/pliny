---
id: ticket:tkrout5
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
depends_on: []
---

# Summary

Make one ticket section own the next-route token and keep route readiness focused
on readiness details.

# Context

Council finding `NC-005` found that the ticket template repeats route-token
selection in both `Next Move / Next Route` and `Route Readiness`.

# Why Now

Duplicate route fields can drift and confuse fresh agents about which value owns
the next governed move.

# Scope

- Update ticket template/readiness guidance so one section owns the route token.
- Make the readiness section describe route-specific readiness, not duplicate
  route truth.
- Preserve ticket ownership of live execution state.

# Out Of Scope

- Do not remove route readiness guidance.
- Do not add route automation or validators.

# Acceptance Criteria

- ACC-001: Ticket template has one route-token owner.
- ACC-002: Route readiness describes readiness details without duplicating route
  truth.
- ACC-003: Ticket live-state ownership remains clear.
- ACC-004: Evidence records route-field searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-005` | pending | pending | open |
| `ticket:tkrout5#ACC-001` through `ticket:tkrout5#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-tickets/templates/ticket.md` and
`skills/loom-tickets/references/readiness.md`.

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet after prior plan-sequence tickets close.

# Route Readiness

Route: ralph

Bounded iteration: ticket route field ownership cleanup.
Write boundary: targeted ticket template/reference wording, this ticket, one
evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `Next Move / Next Route`, `Route Readiness`,
`Route:`, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: route-field drift can mislead recovery and acceptance routing.

Required critique profiles:

- routing-safety
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

Plan sequence follows `ticket:pktprov4`.

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-005`.
