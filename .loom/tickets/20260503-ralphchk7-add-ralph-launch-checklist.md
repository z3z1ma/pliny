---
id: ticket:ralphchk7
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T00:56:36Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
external_refs: {}
depends_on: []
---

# Summary

Add Ralph parent launch checklist guidance and clarify packet `consumed` does not
mean accepted work.

# Context

Older audit action 3 found that Ralph launch readiness could be easier to fake
because the packet template does not locally force a parent checklist before
launch.

# Why Now

Ralph packets are the fresh-context execution contract. Launch preflight should be
visible in the copied packet, and packet lifecycle status should not be confused
with ticket acceptance.

# Scope

- Add a parent launch checklist to the Ralph packet template or equivalent Ralph
  packet contract surface.
- Ensure checklist covers source freshness, write scope, merge scope, git context,
  verification posture, stop conditions, and output contract.
- Clarify in shared packet frontmatter or Ralph guidance that `consumed` means
  output returned and parent notes exist, not accepted work.

# Out Of Scope

- Do not add a packet runtime validator.
- Do not make packets canonical project truth.
- Do not change critique/wiki packet family semantics unless a shared wording
  touch is necessary.

# Acceptance Criteria

- ACC-001: Ralph packet copy surface includes or points to a concrete parent
  launch checklist.
- ACC-002: Checklist makes source freshness, non-overlapping child write scope,
  parent merge scope, execution context, verification posture, stop conditions,
  and output contract explicit.
- ACC-003: Packet lifecycle guidance states `consumed` is not accepted work;
  ticket/owner records decide acceptance.
- ACC-004: Evidence records before/after Ralph checklist and packet status
  searches plus `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-009`
- `ticket:ralphchk7#ACC-001`
- `ticket:ralphchk7#ACC-002`
- `ticket:ralphchk7#ACC-003`
- `ticket:ralphchk7#ACC-004`
- `ticket:ralphchk7#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-009` | pending | pending | open |
| `ticket:ralphchk7#ACC-001` through `ticket:ralphchk7#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-ralph/templates/ralph-packet.md`,
`skills/loom-ralph/references/packet-contract.md`, and
`skills/loom-records/references/packet-frontmatter.md`.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: Ralph launch checklist and consumed/accepted boundary.
Write boundary: Ralph/shared packet guidance, this ticket, one evidence record,
one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for parent launch checklist, source freshness,
`consumed`, accepted/acceptance wording, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: Ralph packet contracts shape implementation safety and ticket
truth reconciliation.

Required critique profiles:

- packet-safety
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

None.

# Journal

- 2026-05-03T00:56:36Z: Created from older audit action 3.
