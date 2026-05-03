---
id: ticket:drvcont13
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
---

# Summary

Add `continue` to the drive tranche route-priority table.

# Context

`route-vocabulary.md` recognizes `continue`, but drive tranche priority does not
name when the correct move is to continue inside the current owner chain.

# Why Now

Without a priority row, drive can over-route work that is already governed by an
owner record.

# Scope

- Add a `continue` priority row for already-governed next tranches.
- Clarify that this is route-token `continue`, not a Ralph child outcome.

# Out Of Scope

- Do not change Ralph child outcome vocabulary.
- Do not make `continue` a default when owner truth is missing.

# Acceptance Criteria

- ACC-001: Drive route priority includes a `continue` row for already-governed
  next tranches.
- ACC-002: Guidance distinguishes route-token `continue` from Ralph child output.
- ACC-003: Existing owner-record reconciliation remains required before continuing.
- ACC-004: Evidence records targeted `continue` route searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-014`
- `ticket:drvcont13#ACC-001`
- `ticket:drvcont13#ACC-002`
- `ticket:drvcont13#ACC-003`
- `ticket:drvcont13#ACC-004`
- `ticket:drvcont13#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-014` | pending | pending | open |
| `ticket:drvcont13#ACC-001` | pending | pending | open |
| `ticket:drvcont13#ACC-002` | pending | pending | open |
| `ticket:drvcont13#ACC-003` | pending | pending | open |
| `ticket:drvcont13#ACC-004` | pending | pending | open |
| `ticket:drvcont13#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-drive/references/tranche-decision-protocol.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: add drive `continue` priority.
Write boundary: drive tranche decision reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, `continue` route observations, and
critique recommendation.

# Evidence

Expected: targeted searches for `continue`, route-priority row, Ralph child
outcome distinction, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: drive routing controls autonomous continuation.

Required critique profiles:

- workflow-boundary
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

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 2.
