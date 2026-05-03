---
id: ticket:pktorph21
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T08:17:57Z
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
  critique:
    - critique:orphan-packet-family-routing-review
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
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-022` | `evidence:orphan-packet-family-routing-validation` | `critique:orphan-packet-family-routing-review` | supported |
| `ticket:pktorph21#ACC-001` | `evidence:orphan-packet-family-routing-validation` | `critique:orphan-packet-family-routing-review` | supported |
| `ticket:pktorph21#ACC-002` | `evidence:orphan-packet-family-routing-validation` | `critique:orphan-packet-family-routing-review` | supported |
| `ticket:pktorph21#ACC-003` | `evidence:orphan-packet-family-routing-validation` | `critique:orphan-packet-family-routing-review` | supported |
| `ticket:pktorph21#ACC-004` | `evidence:orphan-packet-family-routing-validation` | `critique:orphan-packet-family-routing-review` | supported |
| `ticket:pktorph21#ACC-005` | `evidence:orphan-packet-family-routing-validation` | `critique:orphan-packet-family-routing-review` | supported |

# Execution Notes

Likely touched file: `skills/loom-records/references/repair-and-drift.md`.

# Blockers

None - prerequisite `ticket:shipacc1` is closed and pushed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:askpost22`.

Ralph packet `packet:ralph-ticket-pktorph21-20260503T081332Z` completed in scope,
evidence was recorded, mandatory critique passed with no findings, and acceptance
is complete.

# Route Readiness

Ralph readiness:
Bounded iteration: orphan packet repair routing by packet family.
Write boundary: records repair-and-drift reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, packet family routing observations, and
critique recommendation.

Acceptance review readiness:
Evidence `evidence:orphan-packet-family-routing-validation` and mandatory critique
`critique:orphan-packet-family-routing-review` support closure.

# Evidence

Expected: targeted searches for orphan packet, packet_kind, ralph, critique, wiki,
unknown family, records repair, and `git diff --check`.

Recorded:

- `evidence:orphan-packet-family-routing-validation`

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: repair routing must preserve packet-family ownership.

Required critique profiles:

- repair-routing
- packet-family
- workflow-boundary

Findings:

`critique:orphan-packet-family-routing-review`: no findings; mandatory critique
passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Orphan packet repair routing by packet family was promoted into records repair
  and drift guidance.

Deferred / not-required rationale:

No separate wiki, research, spec, constitution, or memory record is needed. The
durable lesson is local to repair-and-drift guidance.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in records
repair-and-drift guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T08:17:57Z
Basis: Ralph packet `packet:ralph-ticket-pktorph21-20260503T081332Z`; evidence
`evidence:orphan-packet-family-routing-validation`; mandatory critique
`critique:orphan-packet-family-routing-review` with no findings.
Residual risks: Future operators must still treat kind/path conflicts as
contradictory metadata and route them to records repair first; the authored
guidance supports that.

# Dependencies

- `ticket:shipacc1`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 10.
- 2026-05-03T08:13:33Z: Parent confirmed prerequisites are closed and pushed,
  moved this ticket to active, and compiled Ralph iteration 1.
- 2026-05-03T08:15:26Z: Ralph child returned `stop`; parent accepted the scoped
  implementation output, recorded evidence, consumed the packet, and moved to
  mandatory critique.
- 2026-05-03T08:17:57Z: Mandatory critique
  `critique:orphan-packet-family-routing-review` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
