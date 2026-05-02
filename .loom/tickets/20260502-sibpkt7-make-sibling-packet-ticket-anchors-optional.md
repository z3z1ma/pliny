---
id: ticket:sibpkt7
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
  - ticket:pktprov4
---

# Summary

Make ticket references optional in critique/wiki packet templates when the target
is not ticket-centered.

# Context

Council finding `NC-007` found critique/wiki packet templates that still assume
ticket-centered targets or parent merge scopes.

# Why Now

Critique and wiki are sibling workflows. Their packets may target records, pages,
or source sets without a ticket anchor.

# Scope

- Update critique and wiki packet templates to allow ticket-less targets with
  `None - rationale` examples where appropriate.
- Preserve ticket-centered examples where tickets are real targets.
- Keep critique/wiki packet discipline separate from Ralph.

# Out Of Scope

- Do not remove ticket links where tickets actually own execution.
- Do not make critique/wiki packets canonical owner layers.

# Acceptance Criteria

- ACC-001: Critique packet template supports non-ticket review targets.
- ACC-002: Wiki packet template supports non-ticket synthesis targets.
- ACC-003: Ticket refs and parent merge scope are explicit with `None - rationale`
  where absent.
- ACC-004: Evidence records sibling packet template searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-007`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-007` | pending | pending | open |
| `ticket:sibpkt7#ACC-001` through `ticket:sibpkt7#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-critique/templates/critique-packet.md`
and `skills/loom-wiki/templates/wiki-packet.md`.

# Blockers

Depends on `ticket:pktprov4`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: ralph

Bounded iteration: critique/wiki packet optional ticket-anchor cleanup.
Write boundary: targeted critique/wiki packet templates, this ticket, one evidence
record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for ticket refs, `None - rationale`, parent merge
scope, critique/wiki packet templates, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: sibling packet templates must not make tickets mandatory where
the workflow target is not ticket-owned.

Required critique profiles:

- owner-boundary
- records-grammar
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

- `ticket:pktprov4`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-007`.
