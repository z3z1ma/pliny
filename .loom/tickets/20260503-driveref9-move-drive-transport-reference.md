---
id: ticket:driveref9
kind: ticket
status: closed
change_class: documentation-explanation
risk_class: medium
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T03:06:40Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
  packet:
    - packet:ralph-ticket-driveref9-20260503T025733Z
  evidence:
    - evidence:drive-transport-reference-validation
  critique:
    - critique:drive-transport-reference-review
external_refs: {}
depends_on: []
---

# Summary

Move detailed `loom-drive` optional outer-loop subagent transport mechanics into a
reference while preserving behavior.

# Context

Older audit action 9 found `loom-drive/SKILL.md` carries valuable but detailed
transport mechanics that fit better in a reference under progressive disclosure.

# Why Now

The main drive skill should stay focused on activation, contract, loop, and read
order while deeper optional transport mechanics remain discoverable and citable.

# Scope

- Move detailed optional outer-loop subagent transport mechanics from
  `skills/loom-drive/SKILL.md` into a new reference.
- Keep concise main-skill guidance and read-order linkage.
- Preserve support-surface and truth-owner boundaries exactly.

# Out Of Scope

- Do not shorten frontmatter activation descriptions.
- Do not change drive behavior, handoff metadata semantics, or support-artifact
  ownership.
- Do not create a new workflow or owner layer.

# Acceptance Criteria

- ACC-001: `loom-drive/SKILL.md` keeps concise transport guidance and points to a
  reference for details.
- ACC-002: New reference preserves optional outer-loop transport mechanics,
  support-surface boundaries, and parent reconciliation requirements.
- ACC-003: Read order includes the new reference only when optional outer-loop
  subagent transport is relevant.
- ACC-004: Evidence records before/after drive transport/read-order searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-011`
- `ticket:driveref9#ACC-001`
- `ticket:driveref9#ACC-002`
- `ticket:driveref9#ACC-003`
- `ticket:driveref9#ACC-004`
- `ticket:driveref9#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-011` | `evidence:drive-transport-reference-validation` | `critique:drive-transport-reference-review` | supported |
| `ticket:driveref9#ACC-001` through `ticket:driveref9#ACC-005` | `evidence:drive-transport-reference-validation` | `critique:drive-transport-reference-review` | supported |

# Execution Notes

Likely touched surfaces are `skills/loom-drive/SKILL.md` and a new
`skills/loom-drive/references/outer-loop-subagent-transport.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:minpol10`.

Ralph packet `packet:ralph-ticket-driveref9-20260503T025733Z` was consumed in
scope, evidence was repaired and recorded, oracle critique passed after one
evidence-coverage finding was resolved, and acceptance is complete.

# Route Readiness

Acceptance review readiness:

Evidence `evidence:drive-transport-reference-validation` and oracle critique
`critique:drive-transport-reference-review` support closure with no unresolved
findings.

# Evidence

Recorded: `evidence:drive-transport-reference-validation`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: moving guidance between skill and reference can accidentally
drop support-surface or parent-reconciliation constraints.

Required critique profiles:

- workflow-boundary
- owner-boundary
- operator-clarity

Findings:

`critique:drive-transport-reference-review#DRVREF9-ORC-001` - resolved. Initial
oracle critique found the whitespace check did not cover the new untracked
reference; parent repaired evidence with intent-to-add plus a scoped `git diff
--check`, and final oracle re-critique passed with no unresolved findings.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Optional outer-loop subagent transport mechanics were promoted from the main
  drive skill body into `skills/loom-drive/references/outer-loop-subagent-transport.md`.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
drive skill and new drive reference.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T03:06:40Z
Basis: Ralph packet `packet:ralph-ticket-driveref9-20260503T025733Z`; evidence
`evidence:drive-transport-reference-validation`; oracle critique
`critique:drive-transport-reference-review` with initial finding resolved and no
unresolved findings.
Residual risks: extraction is documentation-only; future correctness depends on
operators following the conditional reference and template read-order guidance.

# Dependencies

None.

# Journal

- 2026-05-03T00:56:36Z: Created from older audit action 9.
- 2026-05-03T02:57:34Z: Marked active and compiled Ralph packet
  `packet:ralph-ticket-driveref9-20260503T025733Z` for drive optional transport
  reference extraction.
- 2026-05-03T03:00:29Z: Ralph iteration
  `packet:ralph-ticket-driveref9-20260503T025733Z` completed in scope. Evidence
  recorded in `evidence:drive-transport-reference-validation`; next route is
  mandatory oracle critique.
- 2026-05-03T03:04:20Z: Initial oracle critique found the whitespace evidence did
  not cover the new untracked reference. Parent added the new reference as
  intent-to-add and updated evidence with a path-limited `git diff --check` that
  covers both changed drive files.
- 2026-05-03T03:06:40Z: Mandatory oracle critique
  `critique:drive-transport-reference-review` passed after resolving
  `DRVREF9-ORC-001`. Parent recorded retrospective / promotion disposition and
  accepted closure.
