---
id: ticket:tmplph8x
kind: ticket
status: closed
change_class: record-hygiene
risk_class: medium
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T20:46:18Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  packet:
    - packet:ralph-ticket-tmplph8x-20260502T203733Z
  evidence:
    - evidence:template-placeholder-validation
  critique:
    - critique:template-placeholder-safety-review
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
| `initiative:skills-corpus-council-precision-pass#OBJ-008` | `evidence:template-placeholder-validation` | `critique:template-placeholder-safety-review` | supported |
| `ticket:tmplph8x#ACC-001` | `evidence:template-placeholder-validation` | `critique:template-placeholder-safety-review` | supported |
| `ticket:tmplph8x#ACC-002` | `evidence:template-placeholder-validation` | `critique:template-placeholder-safety-review` | supported |
| `ticket:tmplph8x#ACC-003` | `evidence:template-placeholder-validation` | `critique:template-placeholder-safety-review` | supported |
| `ticket:tmplph8x#ACC-004` | `evidence:template-placeholder-validation` | `critique:template-placeholder-safety-review` | supported |
| `ticket:tmplph8x#ACC-005` | `critique:template-placeholder-safety-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces are `skills/**/templates/*.md` only unless references need
small supporting wording.

Ralph iteration `packet:ralph-ticket-tmplph8x-20260502T203733Z` audited and
hardened template placeholders without eliminating useful examples or adding
runtime validation.

# Blockers

None - tickets `retrod3p`, `authst4p`, and `pktgram5` are closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:evshape9`.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence `evidence:template-placeholder-validation` and oracle critique
`critique:template-placeholder-safety-review` support closure with no findings.

# Evidence

Recorded: `evidence:template-placeholder-validation` with targeted before/after
searches for `ACC-001`, pipe-style enum placeholders, empty write-scope arrays,
angle-bracket placeholders, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique; templates train future agents.

Required critique profiles:

- records-grammar
- operator-clarity

Findings:

Recorded in `critique:template-placeholder-safety-review`:

- None - no findings.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle critique passed with no findings.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Placeholder-safety improvements were promoted directly into the copied
  templates that own the unsafe defaults:
  `skills/loom-critique/templates/critique-packet.md`,
  `skills/loom-critique/templates/critique.md`,
  `skills/loom-drive/templates/outer-loop-handoff.md`,
  `skills/loom-ralph/templates/ralph-packet.md`,
  `skills/loom-specs/templates/spec.md`,
  `skills/loom-tickets/templates/ticket.md`, and
  `skills/loom-wiki/templates/wiki-packet.md`.

Deferred / not-required rationale:

Not deferred. The durable lesson was promoted into the affected product
templates; no separate wiki page, research record, spec, constitution decision,
or memory entry is needed.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted guidance now lives in the
template surfaces operators copy.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T20:46:18Z
Basis: Ralph packet `packet:ralph-ticket-tmplph8x-20260502T203733Z`; evidence
`evidence:template-placeholder-validation`; oracle critique
`critique:template-placeholder-safety-review` with no findings.
Residual risks: placeholder validation is structural and search-based; useful
examples and compact metadata placeholders remain where they are visibly
placeholder-shaped or instructional.

# Dependencies

- `ticket:retrod3p`
- `ticket:authst4p`
- `ticket:pktgram5`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-008`.
- 2026-05-02T20:37:33Z: Started Ralph iteration
  `packet:ralph-ticket-tmplph8x-20260502T203733Z` from baseline
  `dab8a56fed213d83770d7715d58445684c36cae1`.
- 2026-05-02T20:40:40Z: Ralph child hardened high-risk template placeholders,
  recorded `evidence:template-placeholder-validation`, and moved the ticket to
  `review_required` for mandatory oracle critique.
- 2026-05-02T20:46:18Z: Oracle critique passed with no findings. Recorded
  acceptance and retrospective / promotion disposition; closed ticket.
