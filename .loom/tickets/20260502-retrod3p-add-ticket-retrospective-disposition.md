---
id: ticket:retrod3p
kind: ticket
status: ready
change_class: protocol-authority
risk_class: high
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
  - ticket:rtvocab1
---

# Summary

Add a standard ticket closure home for retrospective and promotion disposition.

# Context

Council finding `CR-003` found retrospective framed as the compounding gate for
non-trivial closure while the ticket template exposes mainly `Wiki Disposition`,
not a broader promotion disposition.

# Why Now

Tickets own closure. They should explicitly say whether durable lessons were
promoted, deferred, or not required.

# Scope

- Add `Retrospective / Promotion Disposition` or equivalent ticket closure section.
- Align ticket acceptance gate, ticket template, and retrospective references.
- Preserve wiki disposition as one possible promotion route without making it the
  only closure follow-through.

# Out Of Scope

- Do not create a new retrospective record kind or ledger.
- Do not require promotion when no durable lesson exists.
- Do not make retrospective replace ticket acceptance.

# Acceptance Criteria

- ACC-001: Ticket template has a standard section for retrospective/promotion
  disposition.
- ACC-002: Acceptance gate explains when promotion disposition blocks, completes,
  defers, or is not required.
- ACC-003: Retrospective guidance routes lessons to existing owner layers only.
- ACC-004: Evidence records template/reference comparisons and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-003`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-003` | pending | pending | open |
| `ticket:retrod3p#ACC-001` through `ticket:retrod3p#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-tickets/templates/ticket.md`,
`skills/loom-tickets/references/acceptance-gate.md`, `skills/loom-records/references/retrospective.md`,
and `skills/loom-retrospective/SKILL.md`.

# Blockers

Depends on `ticket:rtvocab1`.

# Next Move / Next Route

Ralph implementation packet after dependency closes.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: add ticket retrospective/promotion disposition grammar.
Write boundary: ticket/retrospective references and templates, this ticket, one
evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: targeted searches for `Wiki Disposition`, `Retrospective`, `Promotion`,
acceptance gate sections, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: this changes closure discipline.

Required critique profiles:

- protocol-change
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

- `ticket:rtvocab1`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-003`.
