---
id: ticket:critrec9
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
  - ticket:critgate2
---

# Summary

Normalize critique recommendation vocabulary so it cannot be mistaken for ticket
states or route tokens.

# Context

Council finding `NC-009` found critique recommendation prose such as
`close-ready` that can blur critique recommendations with canonical ticket state.

# Why Now

Critique should recommend acceptance posture without mutating ticket truth or
teaching non-canonical status values.

# Scope

- Update critique template/references to separate recommendation prose from ticket
  lifecycle states and route tokens.
- Preserve critique ownership of findings/verdicts and ticket ownership of closure.
- Align with route vocabulary where route values are named.

# Out Of Scope

- Do not remove acceptance recommendations from critique.
- Do not give critique records closure authority.

# Acceptance Criteria

- ACC-001: Critique recommendation vocabulary is clearly non-canonical unless it
  names an existing ticket state or route token explicitly.
- ACC-002: Critique guidance says recommendations do not mutate ticket state.
- ACC-003: Ticket and critique ownership boundaries remain clear.
- ACC-004: Evidence records recommendation/status vocabulary searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-009`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-009` | pending | pending | open |
| `ticket:critrec9#ACC-001` through `ticket:critrec9#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-critique/templates/critique.md` and
related critique finding/recommendation references.

# Blockers

Depends on `ticket:critgate2`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: ralph

Bounded iteration: critique recommendation vocabulary cleanup.
Write boundary: targeted critique template/reference wording, this ticket, one
evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `close-ready`, recommendation/status wording,
route tokens in critique guidance, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: critique/ticket boundary ambiguity can corrupt acceptance state.

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

- `ticket:critgate2`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-009`.
