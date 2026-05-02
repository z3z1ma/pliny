---
id: ticket:readme11
kind: ticket
status: ready
change_class: documentation-explanation
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
  - ticket:routewf10
  - ticket:phsafe8
  - ticket:critrec9
---

# Summary

Clarify README product-surface framing so `skills/` is the package surface and
other files are explanatory, maintainer, adapter, example, or packaging support.

# Context

Council finding `NC-011` found README wording that may blur the product surface
with repo support docs, adapters, or examples.

# Why Now

Public package framing should reinforce the skills-only product boundary and avoid
making support surfaces look like protocol truth owners.

# Scope

- Review README product-surface and install/framing language.
- Clarify `skills/` as the protocol product surface.
- Keep support docs/adapters/examples framed as explanatory or packaging support.

# Out Of Scope

- Do not rewrite the README for style alone.
- Do not change install mechanics or add command surfaces.

# Acceptance Criteria

- ACC-001: README clearly names `skills/` as the product surface.
- ACC-002: README does not imply support docs, adapters, examples, or packaging
  files own protocol truth.
- ACC-003: README remains clear for public readers.
- ACC-004: Evidence records README framing searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-011`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-011` | pending | pending | open |
| `ticket:readme11#ACC-001` through `ticket:readme11#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surface is `README.md`; inspect nearby install/framing docs only if
README changes need consistency checks.

# Blockers

Depends on `ticket:routewf10`, `ticket:phsafe8`, and `ticket:critrec9`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: ralph

Bounded iteration: README product-surface framing cleanup.
Write boundary: `README.md`, this ticket, one evidence record, one critique
record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after README searches for product surface/support/adapters/examples
framing and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: README public framing can misrepresent protocol authority.

Required critique profiles:

- product-framing
- owner-boundary
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

- `ticket:routewf10`
- `ticket:phsafe8`
- `ticket:critrec9`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-011`.
