---
id: ticket:critgate2
kind: ticket
status: ready
change_class: protocol-authority
risk_class: high
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

Tighten bootstrap closure wording so mandatory critique cannot be read as
deferrable before closure.

# Context

Council finding `NC-002` found wording in bootstrap validation/critique doctrine
that says required critique has happened or is explicitly deferred, which can
blur mandatory and recommended critique policies.

# Why Now

Closure discipline should fail closed for mandatory critique while still allowing
ticket-owned rationale for recommended critique disposition.

# Scope

- Update bootstrap validation and critique/wiki references to distinguish
  mandatory critique from recommended critique.
- Preserve ticket-owned acceptance and critique finding disposition boundaries.
- Keep recommended critique disposition flexible where policy allows it.

# Out Of Scope

- Do not make optional critique mandatory.
- Do not move closure authority out of tickets.

# Acceptance Criteria

- ACC-001: Mandatory critique clearly blocks closure until completed and required
  findings are dispositioned.
- ACC-002: Recommended critique can be completed, deferred, or not required only
  with ticket-owned rationale.
- ACC-003: Bootstrap validation and critique/wiki wording are consistent.
- ACC-004: Evidence records critique-gate wording searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-002`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-002` | pending | pending | open |
| `ticket:critgate2#ACC-001` through `ticket:critgate2#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-bootstrap/references/07-validation-and-honesty.md`
and `skills/loom-bootstrap/references/05-critique-and-wiki.md`.

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet after `ticket:pktsupp1` closes by plan sequence.

# Route Readiness

Route: ralph

Bounded iteration: mandatory/recommended critique closure gate wording.
Write boundary: targeted bootstrap references, this ticket, one evidence record,
one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for required/mandatory/recommended critique closure
wording and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: closure-gate ambiguity can weaken fail-closed acceptance.

Required critique profiles:

- closure-honesty
- operator-clarity
- routing-safety

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

Plan sequence follows `ticket:pktsupp1`.

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-002`.
