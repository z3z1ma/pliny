---
id: ticket:shipdec2
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T17:02:36Z
updated_at: 2026-05-03T17:04:52Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  evidence:
    - evidence:ship-drive-decoupling-validation
  critique:
    - critique:ship-drive-decoupling-review
external_refs: {}
depends_on: []
---

# Summary

Decouple `loom-ship` packaging preconditions from `loom-drive` hard preflight
gates while preserving drive-owned gate requirements when drive is the parent
workflow.

# Context

The prior fourth-pass audit patch made `loom-ship` say to run drive hard preflight
gates before packaging. That over-couples independent workflow skills: `loom-ship`
can run outside drive, while `loom-drive` may still require drive gates before it
routes to `ship`.

# Why Now

The user identified the coupling before commit. The product surface should make
skill independence clear now rather than preserving a misleading workflow
dependency.

# Scope

- Replace drive-specific preflight wording inside `loom-ship` with ship-owned
  packaging preconditions.
- Keep drive-specific hard-gate requirements in `loom-drive` references.
- State that drive gates apply to `ship` only when drive is the parent workflow.

# Out Of Scope

- Do not remove drive's right to gate `ship` inside drive-managed work.
- Do not add a new shared gate runtime, command wrapper, or validator.

# Acceptance Criteria

- ACC-001: `loom-ship` no longer tells all shipping routes to run drive hard
  preflight gates.
- ACC-002: `loom-ship` still blocks packaging when ticket/evidence/critique,
  scope, safety, Git/worktree, or handoff truth is not ready.
- ACC-003: Drive references still gate `ship` when drive is the parent workflow.
- ACC-004: Structural validation and critique support the change.

# Coverage

Covers:

- ticket:shipdec2#ACC-001
- ticket:shipdec2#ACC-002
- ticket:shipdec2#ACC-003
- ticket:shipdec2#ACC-004

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| ticket:shipdec2#ACC-001 | evidence:ship-drive-decoupling-validation | critique:ship-drive-decoupling-review | supported |
| ticket:shipdec2#ACC-002 | evidence:ship-drive-decoupling-validation | critique:ship-drive-decoupling-review | supported |
| ticket:shipdec2#ACC-003 | evidence:ship-drive-decoupling-validation | critique:ship-drive-decoupling-review | supported |
| ticket:shipdec2#ACC-004 | evidence:ship-drive-decoupling-validation | critique:ship-drive-decoupling-review | supported |

# Execution Notes

Use a tiny local edit. The write boundary is limited to `loom-ship` guidance and
this ticket's validation/critique records.

# Blockers

None.

# Next Move / Next Route

Next route: stop

# Route Readiness

Stop readiness:

Stop reason or condition: ship/drive preflight wording is decoupled, evidence and
mandatory critique are recorded, and no owner work remains for this ticket.

Owner record making the stop truthful: `ticket:shipdec2`.

External action or future trigger that could reopen work: later review finding or
user request that challenges this workflow-boundary wording.

# Evidence

Recorded: `evidence:ship-drive-decoupling-validation` captures targeted wording
searches, `git diff --check`, new ticket whitespace scan, and frontmatter parsing.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: skill-boundary wording affects workflow independence and
operator routing.

Required critique profiles:

- owner-boundary
- workflow-boundary
- closure-honesty

Findings:

- `critique:ship-drive-decoupling-review#FIND-001` — `resolved` by this ticket
  reconciliation: linked evidence/critique, claim matrix updated to `supported`,
  critique disposition completed, retrospective / promotion disposition completed,
  and acceptance recorded.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- The durable workflow-boundary correction is promoted directly into the touched
  `loom-ship` product guidance surfaces.

Deferred / not-required rationale:

No separate wiki, research, spec, plan, initiative, constitution, evidence, or
memory promotion is needed beyond the linked evidence and critique records.

# Wiki Disposition

N/A - no wiki promotion route currently expected.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T17:04:52Z
Basis: product-surface edits; `evidence:ship-drive-decoupling-validation`;
mandatory critique `critique:ship-drive-decoupling-review` with the only finding
resolved by ticket reconciliation.
Residual risks: validation and critique are textual because this repository has
no app runtime or automated behavioral test suite.

# Dependencies

None.

# Journal

- 2026-05-03T17:02:36Z: Created and moved directly to `active` for the
  user-requested decoupling correction.
- 2026-05-03T17:04:52Z: Recorded evidence and mandatory critique, reconciled the
  critique finding, accepted the ticket, recorded promotion disposition, and
  closed with next route `stop`.
