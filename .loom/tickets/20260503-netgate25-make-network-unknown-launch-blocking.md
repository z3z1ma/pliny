---
id: ticket:netgate25
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
  - ticket:pktws19
---

# Summary

Make `network: unknown` a launch blocker unless justified.

# Context

Packet execution context allows `network: unknown`, but launch safety should fail
closed when network posture is unknown and unjustified.

# Why Now

Network access affects safety, reproducibility, and trust boundaries for fresh
workers.

# Scope

- Clarify packet execution context guidance for `network: unknown`.
- Update packet templates if needed so unknown requires a rationale and blocks
  launch when unsafe.

# Out Of Scope

- Do not forbid all network use.
- Do not add a runtime policy engine.

# Acceptance Criteria

- ACC-001: Packet guidance says `network: unknown` is a launch blocker unless a
  rationale makes it safe.
- ACC-002: Templates prompt for explicit network posture or rationale.
- ACC-003: Guidance preserves allowed/forbidden network choices.
- ACC-004: Evidence records targeted network posture searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-026`
- `ticket:netgate25#ACC-001`
- `ticket:netgate25#ACC-002`
- `ticket:netgate25#ACC-003`
- `ticket:netgate25#ACC-004`
- `ticket:netgate25#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-026` | pending | pending | open |
| `ticket:netgate25#ACC-001` | pending | pending | open |
| `ticket:netgate25#ACC-002` | pending | pending | open |
| `ticket:netgate25#ACC-003` | pending | pending | open |
| `ticket:netgate25#ACC-004` | pending | pending | open |
| `ticket:netgate25#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched files: `skills/loom-records/references/packet-frontmatter.md` and
packet templates that carry `network` posture.

# Blockers

Blocked until `ticket:shipacc1` and `ticket:pktws19` close.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: network unknown launch gate.
Write boundary: packet frontmatter guidance and directly related packet templates.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, network posture observations, and critique
recommendation.

# Evidence

Expected: targeted searches for `network: unknown`, launch blocker, rationale,
allowed/forbidden choices, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: network posture is a fresh-worker safety boundary.

Required critique profiles:

- packet-safety
- trust-boundary
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
- `ticket:pktws19`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass secondary polish finding.
