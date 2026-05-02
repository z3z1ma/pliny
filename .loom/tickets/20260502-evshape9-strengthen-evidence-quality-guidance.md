---
id: ticket:evshape9
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T18:58:43Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
external_refs: {}
depends_on:
  - ticket:retrod3p
---

# Summary

Strengthen evidence quality guidance and ticket evidence teaching.

# Context

Council finding `CR-009` found evidence records carry acceptance weight but lack a
dedicated evidence-shape/quality reference covering freshness, scope, limitations,
and support/challenge strength.

# Why Now

Tickets and critique rely on evidence. Evidence should be inspectable without
overclaiming.

# Scope

- Add or expand evidence quality guidance under `loom-evidence`.
- Teach freshness, environment, observed result, limitations, support/challenge,
  invalidation/supersession, and change-class expectations.
- Expand ticket evidence examples or references where acceptance depends on
  evidence sufficiency.

# Out Of Scope

- Do not create an evidence schema runtime.
- Do not make evidence own acceptance or critique verdicts.
- Do not require heavy evidence for trivial local edits.

# Acceptance Criteria

- ACC-001: Evidence skill has dedicated evidence-quality guidance.
- ACC-002: Ticket evidence teaching links evidence sufficiency to acceptance
  without making evidence the owner of closure.
- ACC-003: Guidance distinguishes observed artifacts, inference, limitations,
  freshness, invalidation, and supersession.
- ACC-004: Evidence records before/after evidence-quality searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-009`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-009` | pending | pending | open |
| `ticket:evshape9#ACC-001` through `ticket:evshape9#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-evidence/SKILL.md`, possibly a new
`skills/loom-evidence/references/evidence-shape.md`, ticket evidence sections, and
acceptance gate references.

# Blockers

Depends on `ticket:retrod3p`.

# Next Move / Next Route

Ralph implementation packet after dependency closes.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: add evidence quality guidance and align ticket evidence
teaching.
Write boundary: `skills/loom-evidence/**`, targeted `skills/loom-tickets/**`,
this ticket, one evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: searches for evidence freshness, limitations, invalidation/supersession,
support/challenge, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique; evidence quality affects
acceptance honesty.

Required critique profiles:

- evidence-sufficiency
- operator-clarity
- routing-safety

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

Not deferred.

# Wiki Disposition

Pending retrospective decision after critique.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

- `ticket:retrod3p`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-009`.
