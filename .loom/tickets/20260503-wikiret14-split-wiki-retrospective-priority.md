---
id: ticket:wikiret14
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T06:20:11Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-third-pass-follow-up-validation
external_refs: {}
depends_on:
  - ticket:shipacc1
  - ticket:drvcont13
---

# Summary

Split the drive route-priority row that currently groups `wiki` and
`retrospective`.

# Context

Wiki capture and retrospective compounding are adjacent follow-through routes,
but they do not own the same workflow truth.

# Why Now

Drive priority should not blur accepted explanation capture with a broader
promotion pass across owner layers.

# Scope

- Split the route-priority row into separate `wiki` and `retrospective` cases.
- Keep both routes available and correctly ordered.

# Out Of Scope

- Do not change wiki or retrospective record kinds.
- Do not create a new retrospective directory or ledger.

# Acceptance Criteria

- ACC-001: Drive priority has a distinct `wiki` row for accepted reusable
  explanation or architecture concept capture.
- ACC-002: Drive priority has a distinct `retrospective` row for compounding /
  promotion across owner layers.
- ACC-003: Reconciliation guidance still routes wiki and retrospective results to
  their correct owner layers.
- ACC-004: Evidence records targeted wiki/retrospective priority searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-015`
- `ticket:wikiret14#ACC-001`
- `ticket:wikiret14#ACC-002`
- `ticket:wikiret14#ACC-003`
- `ticket:wikiret14#ACC-004`
- `ticket:wikiret14#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-015` | pending | pending | open |
| `ticket:wikiret14#ACC-001` | pending | pending | open |
| `ticket:wikiret14#ACC-002` | pending | pending | open |
| `ticket:wikiret14#ACC-003` | pending | pending | open |
| `ticket:wikiret14#ACC-004` | pending | pending | open |
| `ticket:wikiret14#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-drive/references/tranche-decision-protocol.md`.

# Blockers

Blocked until `ticket:shipacc1` and `ticket:drvcont13` close.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: split wiki and retrospective drive priority rows.
Write boundary: drive tranche decision reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, row separation observations, and critique
recommendation.

# Evidence

Expected: targeted searches for `wiki`, `retrospective`, route priority,
reconciliation guidance, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: drive priority controls follow-through routing.

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

- `ticket:shipacc1`
- `ticket:drvcont13`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 3.
