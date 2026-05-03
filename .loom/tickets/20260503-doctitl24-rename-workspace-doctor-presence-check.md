---
id: ticket:doctitl24
kind: ticket
status: closed
change_class: documentation-explanation
risk_class: low
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T08:35:48Z
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
    - critique:workspace-doctor-presence-label-review
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
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-025` | `evidence:workspace-doctor-presence-label-validation` | `critique:workspace-doctor-presence-label-review` | supported |
| `ticket:doctitl24#ACC-001` | `evidence:workspace-doctor-presence-label-validation` | `critique:workspace-doctor-presence-label-review` | supported |
| `ticket:doctitl24#ACC-002` | `evidence:workspace-doctor-presence-label-validation` | `critique:workspace-doctor-presence-label-review` | supported |
| `ticket:doctitl24#ACC-003` | `evidence:workspace-doctor-presence-label-validation` | `critique:workspace-doctor-presence-label-review` | supported |
| `ticket:doctitl24#ACC-004` | `evidence:workspace-doctor-presence-label-validation` | `critique:workspace-doctor-presence-label-review` | supported |
| `ticket:doctitl24#ACC-005` | `evidence:workspace-doctor-presence-label-validation` | `critique:workspace-doctor-presence-label-review` | supported |

# Execution Notes

Likely touched file: `skills/loom-workspace/references/doctor.md`.

# Blockers

None - prerequisite `ticket:shipacc1` is closed and pushed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to the next open ticket.

Ralph packet `packet:ralph-ticket-doctitl24-20260503T083039Z` completed in scope,
evidence was recorded, mandatory critique passed with no findings, and acceptance
is complete.

# Route Readiness

Ralph readiness:
Bounded iteration: workspace doctor heading rename.
Write boundary: workspace doctor reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, heading/boundary observations, and critique
recommendation.

Acceptance review readiness:
Evidence `evidence:workspace-doctor-presence-label-validation` and mandatory
critique `critique:workspace-doctor-presence-label-review` support closure.

# Evidence

Expected: targeted searches for `Canonical Presence Checks`, replacement heading,
support/canonical wording, and `git diff --check`.

Recorded:

- `evidence:workspace-doctor-presence-label-validation`

# Critique Disposition

Risk class: low

Critique policy: mandatory

Policy rationale: user requested mandatory critique for every ticket.

Required critique profiles:

- terminology-clarity
- support-boundary

Findings:

`critique:workspace-doctor-presence-label-review`: no findings; mandatory
critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Workspace doctor terminology and support-boundary clarification were promoted
  into `skills/loom-workspace/references/doctor.md`.

Deferred / not-required rationale:

No separate wiki, research, spec, constitution, or memory record is needed. The
durable explanation is local to the workspace doctor reference.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
workspace doctor reference.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T08:35:48Z
Basis: Ralph packet `packet:ralph-ticket-doctitl24-20260503T083039Z`; evidence
`evidence:workspace-doctor-presence-label-validation`; mandatory critique
`critique:workspace-doctor-presence-label-review` with no findings.
Residual risks: Low residual risk that the concise doctor note is not a full
canonical/support path taxonomy; accepted because this ticket is a narrow
terminology correction.

# Dependencies

- `ticket:shipacc1`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass secondary polish finding.
- 2026-05-03T08:30:38Z: Parent confirmed prerequisite is closed and pushed,
  moved this ticket to active, and compiled Ralph iteration 1.
- 2026-05-03T08:32:49Z: Ralph child returned `stop`; parent accepted the scoped
  implementation output, recorded evidence, consumed the packet, and moved to
  mandatory critique.
- 2026-05-03T08:35:48Z: Mandatory critique
  `critique:workspace-doctor-presence-label-review` passed with no findings.
  Parent recorded retrospective / promotion disposition and accepted closure.
