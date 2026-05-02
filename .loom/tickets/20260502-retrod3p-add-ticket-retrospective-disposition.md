---
id: ticket:retrod3p
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T19:41:37Z
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
    - packet:ralph-ticket-retrod3p-20260502T193339Z
  evidence:
    - evidence:ticket-retrospective-disposition-validation
  critique:
    - critique:ticket-retrospective-disposition-review
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
| `initiative:skills-corpus-council-precision-pass#OBJ-003` | `evidence:ticket-retrospective-disposition-validation` | `critique:ticket-retrospective-disposition-review` | supported |
| `ticket:retrod3p#ACC-001` | `evidence:ticket-retrospective-disposition-validation` | `critique:ticket-retrospective-disposition-review` | supported |
| `ticket:retrod3p#ACC-002` | `evidence:ticket-retrospective-disposition-validation` | `critique:ticket-retrospective-disposition-review` | supported |
| `ticket:retrod3p#ACC-003` | `evidence:ticket-retrospective-disposition-validation` | `critique:ticket-retrospective-disposition-review` | supported |
| `ticket:retrod3p#ACC-004` | `evidence:ticket-retrospective-disposition-validation` | `critique:ticket-retrospective-disposition-review` | supported |
| `ticket:retrod3p#ACC-005` | `critique:ticket-retrospective-disposition-review` | `critique:ticket-retrospective-disposition-review` passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-tickets/templates/ticket.md`,
`skills/loom-tickets/references/acceptance-gate.md`, `skills/loom-records/references/retrospective.md`,
and `skills/loom-retrospective/SKILL.md`.

# Blockers

None - `ticket:rtvocab1` is closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:authst4p`.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence and critique disposition: `evidence:ticket-retrospective-disposition-validation`
and `critique:ticket-retrospective-disposition-review` support acceptance with no
findings.
Residual risks: older tickets may still use wiki-only disposition language until
they are touched; the current product surfaces now define the broader disposition.

# Evidence

`evidence:ticket-retrospective-disposition-validation` records before/after
searches for `Wiki Disposition`, `Retrospective`, `Promotion`, acceptance gate
sections, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: this changes closure discipline.

Required critique profiles:

- protocol-change
- operator-clarity
- routing-safety

Findings:

Recorded in `critique:ticket-retrospective-disposition-review`:

- None - no findings.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle critique passed with no findings.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Ticket closure grammar was promoted into `skills/loom-tickets/templates/ticket.md`,
  `skills/loom-tickets/references/acceptance-gate.md`, `skills/loom-tickets/SKILL.md`,
  `skills/loom-records/references/retrospective.md`, `skills/loom-retrospective/SKILL.md`,
  and `skills/loom-bootstrap/references/05-critique-and-wiki.md`.

Deferred / not-required rationale:

Not deferred. This ticket's durable lesson was promoted directly into the owner
product surfaces listed above; no separate wiki page, research record, spec,
constitution decision, or memory entry is needed.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation is now in the
ticket and retrospective owner surfaces.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T19:41:37Z
Basis: Ralph packet `packet:ralph-ticket-retrod3p-20260502T193339Z`; evidence
`evidence:ticket-retrospective-disposition-validation`; oracle critique
`critique:ticket-retrospective-disposition-review` with no findings.
Residual risks: older tickets may still show wiki-only disposition until touched;
the product template and guidance now define broader ticket-owned promotion
disposition for future work.

# Dependencies

- `ticket:rtvocab1`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-003`.
- 2026-05-02T19:33:39Z: Started Ralph iteration
  `packet:ralph-ticket-retrod3p-20260502T193339Z` from baseline
  `1ff2b52a3fcab827c8a9f17ada55b9800382137b`.
- 2026-05-02T19:35:56Z: Ralph iteration added ticket retrospective /
  promotion disposition grammar, recorded validation evidence, and moved ticket
  to `review_required` for mandatory critique.
- 2026-05-02T19:41:37Z: Oracle critique passed with no findings. Recorded
  acceptance and retrospective / promotion disposition; closed ticket.
