---
id: ticket:ralphg20
kind: ticket
status: ready
change_class: protocol-authority
risk_class: high
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
  - ticket:gitstat26
---

# Summary

Add Ralph launch hard gates for unresolved placeholders and ticket route
authorization.

# Context

Ralph packet templates are strong, but the launch checklist does not explicitly
block unresolved template placeholders or packets whose target ticket does not
authorize `next_route: ralph`.

# Why Now

A well-formed packet should not become an unauthorized or placeholder-filled work
order.

# Scope

- Add launch checks for unresolved placeholders / example IDs / generic `<...>`
  tokens.
- Add launch check that target ticket's next route is `ralph` and readiness fields
  match the packet.

# Out Of Scope

- Do not change child outcome vocabulary.
- Do not add automated validators.

# Acceptance Criteria

- ACC-001: Ralph launch checklist blocks unresolved placeholders or example IDs.
- ACC-002: Ralph launch checklist verifies target ticket `next_route: ralph` and
  readiness match.
- ACC-003: Gates preserve parent-side packet authorization and ticket truth.
- ACC-004: Evidence records targeted launch gate searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-021`
- `ticket:ralphg20#ACC-001`
- `ticket:ralphg20#ACC-002`
- `ticket:ralphg20#ACC-003`
- `ticket:ralphg20#ACC-004`
- `ticket:ralphg20#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-021` | pending | pending | open |
| `ticket:ralphg20#ACC-001` | pending | pending | open |
| `ticket:ralphg20#ACC-002` | pending | pending | open |
| `ticket:ralphg20#ACC-003` | pending | pending | open |
| `ticket:ralphg20#ACC-004` | pending | pending | open |
| `ticket:ralphg20#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched files: `skills/loom-ralph/templates/ralph-packet.md` and possibly
`skills/loom-ralph/references/packet-contract.md`.

# Blockers

Blocked until `ticket:shipacc1` and packet metadata hardening tickets close.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: Ralph launch hard gates.
Write boundary: Ralph packet template and directly related launch contract
guidance.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, launch gate observations, and critique
recommendation.

# Evidence

Expected: targeted searches for placeholder gate, `next_route: ralph`, readiness
match, launch checklist, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: launch checks authorize fresh child execution.

Required critique profiles:

- packet-safety
- ticket-truth
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
- `ticket:gitstat26`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 9.
