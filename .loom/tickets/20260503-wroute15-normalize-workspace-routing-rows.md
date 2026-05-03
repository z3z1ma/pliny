---
id: ticket:wroute15
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

Normalize workspace routing rows to separate route tokens from owner or
coordinator skill names.

# Context

Workspace routing currently mixes route-token language with skill-name-only rows,
which can blur saved route values and skill invocation labels.

# Why Now

Fresh agents rely on workspace routing early. It should model route-token grammar
consistently.

# Scope

- Normalize routing rows to include route token and owner/coordinator where
  applicable.
- Keep support-only skills such as memory out of project-truth route tokens.

# Out Of Scope

- Do not add route tokens.
- Do not demote actual workflow coordinator routes.

# Acceptance Criteria

- ACC-001: Workspace routing rows consistently distinguish route token from
  owner/coordinator skill.
- ACC-002: Support-only memory guidance is not presented as a project-truth route.
- ACC-003: Route vocabulary remains the canonical saved-field token source.
- ACC-004: Evidence records targeted workspace routing searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-016`
- `ticket:wroute15#ACC-001`
- `ticket:wroute15#ACC-002`
- `ticket:wroute15#ACC-003`
- `ticket:wroute15#ACC-004`
- `ticket:wroute15#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-016` | pending | pending | open |
| `ticket:wroute15#ACC-001` | pending | pending | open |
| `ticket:wroute15#ACC-002` | pending | pending | open |
| `ticket:wroute15#ACC-003` | pending | pending | open |
| `ticket:wroute15#ACC-004` | pending | pending | open |
| `ticket:wroute15#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-workspace/references/routing.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: workspace routing row normalization.
Write boundary: workspace routing reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, routing row observations, and critique
recommendation.

# Evidence

Expected: targeted searches for route token, owner/coordinator, support skill,
memory, route vocabulary, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: workspace routing is an early cold-start decision surface.

Required critique profiles:

- route-vocabulary
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

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 4.
