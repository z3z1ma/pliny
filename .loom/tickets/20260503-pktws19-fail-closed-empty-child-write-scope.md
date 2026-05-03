---
id: ticket:pktws19
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
---

# Summary

Make packet child write scope fail closed instead of allowing ambiguous empty
lists.

# Context

The shared packet frontmatter common shape currently shows empty
`child_write_scope.records` and `paths`, which can mean none, forgotten, or
unbounded.

# Why Now

Packet write scope is a launch-safety boundary.

# Scope

- Replace ambiguous empty child write scope examples with explicit `None - ...`
  entries.
- State that empty child write scope blocks launch.
- Reconcile directly related packet templates if they still imply empty scope.

# Out Of Scope

- Do not weaken Ralph strictness.
- Do not add a runtime validator or schema engine.

# Acceptance Criteria

- ACC-001: Shared packet frontmatter no longer teaches empty child write scope as
  a valid new-packet shape.
- ACC-002: Guidance says empty child write scope is ambiguous and launch-blocking.
- ACC-003: Packet-family templates remain consistent with fail-closed scope.
- ACC-004: Evidence records targeted child-write-scope searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-020`
- `ticket:pktws19#ACC-001`
- `ticket:pktws19#ACC-002`
- `ticket:pktws19#ACC-003`
- `ticket:pktws19#ACC-004`
- `ticket:pktws19#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-020` | pending | pending | open |
| `ticket:pktws19#ACC-001` | pending | pending | open |
| `ticket:pktws19#ACC-002` | pending | pending | open |
| `ticket:pktws19#ACC-003` | pending | pending | open |
| `ticket:pktws19#ACC-004` | pending | pending | open |
| `ticket:pktws19#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched files: `skills/loom-records/references/packet-frontmatter.md` and
packet templates if needed.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: fail-closed packet child write scope.
Write boundary: shared packet frontmatter and directly related packet templates.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, child write-scope observations, and
critique recommendation.

# Evidence

Expected: targeted searches for `child_write_scope`, empty list examples,
`None -`, launch-blocking wording, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: write scope controls child mutation authority.

Required critique profiles:

- packet-safety
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

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 8.
