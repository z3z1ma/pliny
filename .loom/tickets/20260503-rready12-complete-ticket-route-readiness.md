---
id: ticket:rready12
kind: ticket
status: ready
change_class: protocol-authority
risk_class: high
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

Make ticket route readiness cover every legal route a ready ticket may name.

# Context

The ticket readiness reference lists the legal route vocabulary but only gives
route-readiness details for a subset. Missing branches make routes like
`research`, `spec`, `plan`, `ticket`, `workspace_status`, `records_repair`,
`continue`, and `stop` too easy to name without enough safety facts.

# Why Now

Ready tickets should be resumable without chat history regardless of the chosen
next route.

# Scope

- Add explicit readiness guidance for the missing legal routes.
- Keep guidance concise and route-neutral.
- Update the ticket template route-readiness prompt if needed.

# Out Of Scope

- Do not add route tokens.
- Do not make every route Ralph-shaped.

# Acceptance Criteria

- ACC-001: Readiness guidance covers every legal route token listed in the
  reference.
- ACC-002: New route branches name the minimal safety facts required for each
  route.
- ACC-003: `continue` and `stop` readiness distinguish route tokens from Ralph
  child outcomes.
- ACC-004: Evidence records targeted route readiness searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-013`
- `ticket:rready12#ACC-001`
- `ticket:rready12#ACC-002`
- `ticket:rready12#ACC-003`
- `ticket:rready12#ACC-004`
- `ticket:rready12#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-013` | pending | pending | open |
| `ticket:rready12#ACC-001` | pending | pending | open |
| `ticket:rready12#ACC-002` | pending | pending | open |
| `ticket:rready12#ACC-003` | pending | pending | open |
| `ticket:rready12#ACC-004` | pending | pending | open |
| `ticket:rready12#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched files: `skills/loom-tickets/references/readiness.md` and possibly
`skills/loom-tickets/templates/ticket.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: route-complete ticket readiness guidance.
Write boundary: ticket readiness reference and directly related ticket template
prompt only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, route coverage observations, and critique
recommendation.

# Evidence

Expected: targeted searches for all legal routes, newly added route-readiness
branches, `continue` / `stop` wording, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: route readiness controls whether tickets can safely launch
downstream routes.

Required critique profiles:

- route-coverage
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

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 1.
