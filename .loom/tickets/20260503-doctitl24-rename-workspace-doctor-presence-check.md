---
id: ticket:doctitl24
kind: ticket
status: ready
change_class: documentation-explanation
risk_class: low
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

Rename workspace doctor presence checks so support paths are not labeled
canonical.

# Context

Workspace doctor uses `Canonical Presence Checks` while the checked paths include
support surfaces such as packets.

# Why Now

Terminology should not imply support paths are canonical owner layers.

# Scope

- Rename the heading or wording to avoid calling support paths canonical.
- Preserve the check behavior.

# Out Of Scope

- Do not change workspace bootstrap behavior.
- Do not remove useful path checks.

# Acceptance Criteria

- ACC-001: Workspace doctor no longer labels support-inclusive path checks as
  canonical presence checks.
- ACC-002: The guidance still helps inspect required / expected workspace paths.
- ACC-003: Support-vs-canonical boundary remains clear.
- ACC-004: Evidence records targeted doctor heading searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-025`
- `ticket:doctitl24#ACC-001`
- `ticket:doctitl24#ACC-002`
- `ticket:doctitl24#ACC-003`
- `ticket:doctitl24#ACC-004`
- `ticket:doctitl24#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-025` | pending | pending | open |
| `ticket:doctitl24#ACC-001` | pending | pending | open |
| `ticket:doctitl24#ACC-002` | pending | pending | open |
| `ticket:doctitl24#ACC-003` | pending | pending | open |
| `ticket:doctitl24#ACC-004` | pending | pending | open |
| `ticket:doctitl24#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-workspace/references/doctor.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: workspace doctor heading rename.
Write boundary: workspace doctor reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, heading/boundary observations, and critique
recommendation.

# Evidence

Expected: targeted searches for `Canonical Presence Checks`, replacement heading,
support/canonical wording, and `git diff --check`.

# Critique Disposition

Risk class: low

Critique policy: mandatory

Policy rationale: user requested mandatory critique for every ticket.

Required critique profiles:

- terminology-clarity
- support-boundary

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

- 2026-05-03T06:20:11Z: Created from third-pass secondary polish finding.
