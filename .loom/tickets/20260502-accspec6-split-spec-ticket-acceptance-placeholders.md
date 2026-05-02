---
id: ticket:accspec6
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T23:06:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  packet:
    - packet:ralph-ticket-accspec6-20260502T225846Z
  evidence:
    - evidence:acceptance-placeholder-validation
  critique:
    - critique:acceptance-placeholder-ownership-review
external_refs: {}
depends_on:
  - ticket:tkrout5
---

# Summary

Split ticket acceptance placeholders between spec-owned acceptance and
ticket-local `ACC-*` criteria.

# Context

Council finding `NC-006` found ticket acceptance placeholders that encourage local
`ACC-*` creation even when a spec owns the reusable acceptance contract.

# Why Now

Ticket-local acceptance is useful, but specs own reusable behavior contracts.
Copied tickets should not blur that boundary.

# Scope

- Update ticket template acceptance guidance to show spec-owned and ticket-local
  branches.
- Keep `ACC-*` placeholders only in the ticket-local branch.
- Align claim coverage reference wording if needed.

# Out Of Scope

- Do not require every ticket to have a spec.
- Do not remove ticket-local acceptance for no-spec work.

# Acceptance Criteria

- ACC-001: Ticket template distinguishes spec-owned acceptance from ticket-local
  acceptance.
- ACC-002: Ticket-local `ACC-*` placeholders are not presented as the default when
  a spec owns acceptance.
- ACC-003: Claim coverage guidance stays aligned with ticket/spec boundaries.
- ACC-004: Evidence records acceptance-placeholder searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-006`
- `ticket:accspec6#ACC-001`
- `ticket:accspec6#ACC-002`
- `ticket:accspec6#ACC-003`
- `ticket:accspec6#ACC-004`
- `ticket:accspec6#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-006` | `evidence:acceptance-placeholder-validation` | `critique:acceptance-placeholder-ownership-review` | supported |
| `ticket:accspec6#ACC-001` | `evidence:acceptance-placeholder-validation` | `critique:acceptance-placeholder-ownership-review` | supported |
| `ticket:accspec6#ACC-002` | `evidence:acceptance-placeholder-validation` | `critique:acceptance-placeholder-ownership-review` | supported |
| `ticket:accspec6#ACC-003` | `evidence:acceptance-placeholder-validation` | `critique:acceptance-placeholder-ownership-review` | supported |
| `ticket:accspec6#ACC-004` | `evidence:acceptance-placeholder-validation` | `critique:acceptance-placeholder-ownership-review` | supported |
| `ticket:accspec6#ACC-005` | `critique:acceptance-placeholder-ownership-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-tickets/templates/ticket.md` and
`skills/loom-records/references/claim-coverage.md`.

# Blockers

None - dependency `ticket:tkrout5` is closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:sibpkt7`.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:acceptance-placeholder-validation` and oracle critique
`critique:acceptance-placeholder-ownership-review` support closure with no
findings.

# Evidence

- `evidence:acceptance-placeholder-validation` supports `ACC-001` through
  `ACC-004` with before/after searches for `ACC-*`, spec-owned acceptance,
  ticket-local acceptance, `acceptance contract`, `# Acceptance Criteria`, and
  `# Coverage`, plus `git diff --check`. Fresh for this source state as of
  2026-05-02T23:00:22Z.

Oracle critique `critique:acceptance-placeholder-ownership-review` supports
`ACC-005` with no findings.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: acceptance ownership ambiguity can corrupt downstream closure.

Required critique profiles:

- owner-boundary
- records-grammar
- closure-honesty

Findings:

`critique:acceptance-placeholder-ownership-review` - no findings; mandatory
oracle critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Acceptance owner branch wording was promoted directly into
  `skills/loom-tickets/templates/ticket.md`.
- Spec-vs-ticket acceptance owner guidance was promoted into
  `skills/loom-records/references/claim-coverage.md`.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched ticket and claim-coverage guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T23:05:14Z
Basis: Ralph packet `packet:ralph-ticket-accspec6-20260502T225846Z`; evidence
`evidence:acceptance-placeholder-validation`; oracle critique
`critique:acceptance-placeholder-ownership-review` with no findings.
Residual risks: validation is structural/manual. The wording relies on operators
removing the non-applicable acceptance branch; no runtime enforcement is
introduced by design.

# Dependencies

- `ticket:tkrout5`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-006`.
- 2026-05-02T22:58:46Z: Confirmed dependency `ticket:tkrout5` is closed,
  compiled Ralph packet `packet:ralph-ticket-accspec6-20260502T225846Z`, and
  moved ticket to `active`.
- 2026-05-02T23:00:22Z: Ralph child split the ticket template acceptance guidance
  into spec-owned and ticket-local branches, aligned claim coverage wording,
  recorded `evidence:acceptance-placeholder-validation`, and moved the ticket to
  `review_required` for mandatory oracle critique.
- 2026-05-02T23:03:12Z: Parent reconciled Ralph output, marked
  `packet:ralph-ticket-accspec6-20260502T225846Z` consumed, and confirmed the
  ticket is ready for mandatory oracle critique.
- 2026-05-02T23:05:14Z: Mandatory oracle critique
  `critique:acceptance-placeholder-ownership-review` passed with no findings.
  Parent recorded retrospective / promotion disposition and accepted closure.
