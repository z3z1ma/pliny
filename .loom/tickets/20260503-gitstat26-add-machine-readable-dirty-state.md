---
id: ticket:gitstat26
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
  - ticket:netgate25
---

# Summary

Make packet Git dirty state machine-readable.

# Context

Packet source fingerprints currently use broad `clean|dirty|unknown` values,
which hide whether tracked files, untracked files, or both caused dirty state.

# Why Now

Fresh workers and parents need clear launch-freshness signals.

# Scope

- Add or clarify machine-readable dirty categories such as `dirty_tracked`,
  `dirty_untracked`, and `dirty_mixed`.
- Preserve human-readable detail in `git_status_detail`.
- Update packet templates if needed.

# Out Of Scope

- Do not require a Git helper runtime.
- Do not change Git itself as truth owner for file history.

# Acceptance Criteria

- ACC-001: Packet fingerprint guidance names machine-readable dirty categories.
- ACC-002: Guidance preserves `clean` and `unknown` with rationale when needed.
- ACC-003: `git_status_detail` remains available for human context.
- ACC-004: Evidence records targeted dirty-state searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-027`
- `ticket:gitstat26#ACC-001`
- `ticket:gitstat26#ACC-002`
- `ticket:gitstat26#ACC-003`
- `ticket:gitstat26#ACC-004`
- `ticket:gitstat26#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-027` | pending | pending | open |
| `ticket:gitstat26#ACC-001` | pending | pending | open |
| `ticket:gitstat26#ACC-002` | pending | pending | open |
| `ticket:gitstat26#ACC-003` | pending | pending | open |
| `ticket:gitstat26#ACC-004` | pending | pending | open |
| `ticket:gitstat26#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched files: `skills/loom-records/references/packet-frontmatter.md`,
Ralph packet contract, and packet templates.

# Blockers

Blocked until `ticket:shipacc1` and `ticket:netgate25` close.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: machine-readable packet Git dirty state.
Write boundary: packet frontmatter guidance, Ralph packet contract, and directly
related packet templates.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, dirty-state observations, and critique
recommendation.

# Evidence

Expected: targeted searches for `dirty_tracked`, `dirty_untracked`,
`dirty_mixed`, `git_status_detail`, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: Git state is a launch-safety fingerprint.

Required critique profiles:

- packet-safety
- git-provenance
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
- `ticket:netgate25`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass secondary polish finding.
