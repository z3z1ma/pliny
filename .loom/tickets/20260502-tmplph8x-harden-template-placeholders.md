---
id: ticket:tmplph8x
kind: ticket
status: ready
change_class: record-hygiene
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
  - ticket:authst4p
  - ticket:pktgram5
---

# Summary

Harden templates so placeholders cannot be mistaken for accepted record content.

# Context

Council finding `CR-008` found real-looking placeholders such as generic `ACC-001`
claims and pipe-style enum fields can be saved as if valid.

# Why Now

Templates are copied more often than references. Unsafe defaults pollute the truth
graph.

# Scope

- Audit `skills/**/templates/*.md` for saveable placeholder pollution.
- Replace dangerous placeholder prose with explicit `<TBD: replace before saving>`
  or safe instructional text.
- Preserve useful examples where they are clearly examples, not default truth.

# Out Of Scope

- Do not eliminate all examples.
- Do not add schema/runtime validation.
- Do not rewrite templates beyond placeholder safety.

# Acceptance Criteria

- ACC-001: Templates avoid generic acceptance claims or enum placeholders that look
  valid when saved unchanged.
- ACC-002: Required user-filled fields are marked unmistakably.
- ACC-003: Examples remain useful but cannot be confused with canonical truth.
- ACC-004: Evidence records placeholder searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-008`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-008` | pending | pending | open |
| `ticket:tmplph8x#ACC-001` through `ticket:tmplph8x#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces are `skills/**/templates/*.md` only unless references need
small supporting wording.

# Blockers

Depends on tickets `retrod3p`, `authst4p`, and `pktgram5`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: audit and harden template placeholders.
Write boundary: `skills/**/templates/*.md`, this ticket, one evidence record, one
critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, placeholder searches, evidence, ticket
update, and critique recommendation.

# Evidence

Expected: targeted searches for `<`, `|`, `ACC-001`, `TBD`, generic placeholder
phrases, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique; templates train future agents.

Required critique profiles:

- records-grammar
- operator-clarity

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
- `ticket:authst4p`
- `ticket:pktgram5`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-008`.
