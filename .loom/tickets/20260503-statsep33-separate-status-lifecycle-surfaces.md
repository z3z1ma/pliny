---
id: ticket:statsep33
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T18:43:23Z
updated_at: 2026-05-03T18:44:36Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  evidence:
    - evidence:status-lifecycle-surface-separation-validation
  critique:
    - critique:status-lifecycle-surface-separation-review
external_refs: {}
depends_on: []
---

# Summary

Separate canonical owner statuses, ticket execution states, and support-surface
statuses in `skills/loom-records/references/status-lifecycle.md`.

# Context

The user observed that the status lifecycle reference mixed canonical owner
layers, tickets, packets, workspace metadata, support handoffs, memory, and
support artifacts in one layer-specific list. The prose boundary was accurate,
but the visual shape made the owner/support split harder to scan.

# Why Now

Status vocabulary is shared grammar. The reference should make the owner/support
boundary visually obvious before operators copy statuses into records.

# Scope

- Split the status sets into `Canonical Owner Record Statuses`, `Ticket Execution
  States`, and `Support-Surface Statuses`.
- Keep ticket statuses as a pointer to `skills/loom-tickets/references/state-machine.md`.
- Split transition guidance into canonical owner transitions and support-surface
  transitions, with packet transitions remaining in their own section.

# Out Of Scope

- Do not change allowed status values.
- Do not add runtime enums, validators, or schema requirements.

# Acceptance Criteria

- ACC-001: Canonical owner record statuses are visually separated from support
  statuses.
- ACC-002: Ticket execution states are called out as live ticket states with a
  pointer to the ticket state-machine reference.
- ACC-003: Support-surface statuses are grouped separately and still say they do
  not make support surfaces canonical truth owners.
- ACC-004: Transition guidance preserves the same owner/support separation.
- ACC-005: Structural validation and critique support acceptance.

# Coverage

Covers:

- ticket:statsep33#ACC-001
- ticket:statsep33#ACC-002
- ticket:statsep33#ACC-003
- ticket:statsep33#ACC-004
- ticket:statsep33#ACC-005

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| ticket:statsep33#ACC-001 | evidence:status-lifecycle-surface-separation-validation | critique:status-lifecycle-surface-separation-review | satisfied |
| ticket:statsep33#ACC-002 | evidence:status-lifecycle-surface-separation-validation | critique:status-lifecycle-surface-separation-review | satisfied |
| ticket:statsep33#ACC-003 | evidence:status-lifecycle-surface-separation-validation | critique:status-lifecycle-surface-separation-review | satisfied |
| ticket:statsep33#ACC-004 | evidence:status-lifecycle-surface-separation-validation | critique:status-lifecycle-surface-separation-review | satisfied |
| ticket:statsep33#ACC-005 | evidence:status-lifecycle-surface-separation-validation | critique:status-lifecycle-surface-separation-review | satisfied |

# Execution Notes

Implemented as a local edit to the shared records grammar reference. The change
reorganized headings and grouping without changing the allowed status vocabulary.

# Blockers

None.

# Next Move / Next Route

Next route: stop

# Route Readiness

Stop readiness:

stop_kind: satisfied

stop_reason: Status lifecycle guidance now visually separates canonical owner
statuses, ticket execution states, and support-surface statuses; validation and
critique passed.

owner_record: ticket:statsep33

resume_condition: None - work is accepted and closed; reopen only if a new audit
finding or failed validation challenges this acceptance decision.

closure_claim: yes

# Evidence

Evidence status: sufficient for structural acceptance.

Evidence record:

- evidence:status-lifecycle-surface-separation-validation

# Critique Disposition

Risk class: medium

Critique policy: completed

Policy rationale: the change affects shared record grammar and owner/support
operator clarity, but is a localized structural reorganization.

Findings:

None - `critique:status-lifecycle-surface-separation-review` found no blockers.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- The owner/support separation was promoted directly into the owning records
  grammar reference: `skills/loom-records/references/status-lifecycle.md`.

Deferred / not-required rationale:

No separate wiki, research, spec, plan, initiative, constitution, or memory
promotion is required because the accepted guidance now lives in the shared
records grammar surface that owns it.

# Wiki Disposition

N/A - no wiki route selected.

# Acceptance Decision

Accepted by: OpenCode
Accepted at: 2026-05-03T18:44:36Z
Basis: `evidence:status-lifecycle-surface-separation-validation` and
`critique:status-lifecycle-surface-separation-review` support all acceptance
criteria, and no blockers remain.
Residual risks: This is a structural documentation validation only; future edits
to status vocabulary should re-check owner/support grouping and ticket-state
boundaries.

# Dependencies

None.

# Journal

- 2026-05-03T18:43:23Z: Split status lifecycle status and transition guidance by
  canonical owner records, ticket execution states, and support surfaces, then
  recorded evidence and critique.
- 2026-05-03T18:44:36Z: Validated the changed reference and new records,
  reconciled acceptance, and closed the ticket.
