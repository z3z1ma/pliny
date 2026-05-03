---
id: ticket:pktorph21
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

Route orphan packet repair by packet family.

# Context

Repair guidance now has multiple packet families, but orphan packet repair still
reads as though problems route mainly to Ralph.

# Why Now

Ralph, critique, and wiki packets have separate workflow owners and should not be
repaired through the wrong route.

# Scope

- Update orphan packet repair routing to inspect `packet_kind` or path family.
- Route Ralph, critique, wiki, and unknown packet families to the right owner or
  records repair.

# Out Of Scope

- Do not add packet families.
- Do not migrate historical packets.

# Acceptance Criteria

- ACC-001: Orphan packet routing names `ralph`, `critique`, and `wiki` packet
  family repair routes.
- ACC-002: Unknown packet family routes to records repair before downstream work.
- ACC-003: Packet family ownership remains distinct from ticket truth.
- ACC-004: Evidence records targeted orphan packet routing searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-022`
- `ticket:pktorph21#ACC-001`
- `ticket:pktorph21#ACC-002`
- `ticket:pktorph21#ACC-003`
- `ticket:pktorph21#ACC-004`
- `ticket:pktorph21#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-022` | pending | pending | open |
| `ticket:pktorph21#ACC-001` | pending | pending | open |
| `ticket:pktorph21#ACC-002` | pending | pending | open |
| `ticket:pktorph21#ACC-003` | pending | pending | open |
| `ticket:pktorph21#ACC-004` | pending | pending | open |
| `ticket:pktorph21#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-records/references/repair-and-drift.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: orphan packet repair routing by packet family.
Write boundary: records repair-and-drift reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, packet family routing observations, and
critique recommendation.

# Evidence

Expected: targeted searches for orphan packet, packet_kind, ralph, critique, wiki,
unknown family, records repair, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: repair routing must preserve packet-family ownership.

Required critique profiles:

- repair-routing
- packet-family
- workflow-boundary

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

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 10.
