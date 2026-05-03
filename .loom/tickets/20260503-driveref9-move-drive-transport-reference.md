---
id: ticket:driveref9
kind: ticket
status: ready
change_class: documentation-explanation
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

Move detailed `loom-drive` optional outer-loop subagent transport mechanics into a
reference while preserving behavior.

# Context

Older audit action 9 found `loom-drive/SKILL.md` carries valuable but detailed
transport mechanics that fit better in a reference under progressive disclosure.

# Why Now

The main drive skill should stay focused on activation, contract, loop, and read
order while deeper optional transport mechanics remain discoverable and citable.

# Scope

- Move detailed optional outer-loop subagent transport mechanics from
  `skills/loom-drive/SKILL.md` into a new reference.
- Keep concise main-skill guidance and read-order linkage.
- Preserve support-surface and truth-owner boundaries exactly.

# Out Of Scope

- Do not shorten frontmatter activation descriptions.
- Do not change drive behavior, handoff metadata semantics, or support-artifact
  ownership.
- Do not create a new workflow or owner layer.

# Acceptance Criteria

- ACC-001: `loom-drive/SKILL.md` keeps concise transport guidance and points to a
  reference for details.
- ACC-002: New reference preserves optional outer-loop transport mechanics,
  support-surface boundaries, and parent reconciliation requirements.
- ACC-003: Read order includes the new reference only when optional outer-loop
  subagent transport is relevant.
- ACC-004: Evidence records before/after drive transport/read-order searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-011`
- `ticket:driveref9#ACC-001`
- `ticket:driveref9#ACC-002`
- `ticket:driveref9#ACC-003`
- `ticket:driveref9#ACC-004`
- `ticket:driveref9#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-011` | pending | pending | open |
| `ticket:driveref9#ACC-001` through `ticket:driveref9#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces are `skills/loom-drive/SKILL.md` and a new
`skills/loom-drive/references/outer-loop-subagent-transport.md`.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: drive optional transport reference extraction.
Write boundary: drive skill/reference files, this ticket, one evidence record,
one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for optional outer-loop subagent transport,
support artifact boundaries, read order, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: moving guidance between skill and reference can accidentally
drop support-surface or parent-reconciliation constraints.

Required critique profiles:

- workflow-boundary
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

- 2026-05-03T00:56:36Z: Created from older audit action 9.
