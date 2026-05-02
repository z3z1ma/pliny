---
id: ticket:drvgram3
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T22:03:13Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
external_refs: {}
depends_on:
  - ticket:pktsupp1
---

# Summary

Document or simplify drive outer-loop handoff metadata so fresh agents do not
guess field semantics.

# Context

Council finding `NC-003` found `source_snapshot`, `drive_checkpoint`, and
`gate_status` in the drive handoff template without reference-level grammar.

# Why Now

Drive handoffs are support artifacts. Their metadata should be legible without
creating hidden schema requirements or packet confusion.

# Scope

- Audit drive outer-loop handoff template and drive continuity/checkpoint
  references.
- Either document the handoff fields or simplify the template to existing shared
  support/source grammar.
- Keep drive handoff metadata support-local, not canonical truth.

# Out Of Scope

- Do not make drive handoffs packets.
- Do not add a schema, runtime, or command wrapper.

# Acceptance Criteria

- ACC-001: Drive handoff metadata fields are documented or removed.
- ACC-002: Field semantics do not conflict with Ralph packet grammar.
- ACC-003: Handoff metadata remains support-local and non-canonical.
- ACC-004: Evidence records handoff metadata searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-003`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-003` | pending | pending | open |
| `ticket:drvgram3#ACC-001` through `ticket:drvgram3#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-drive/templates/outer-loop-handoff.md`,
`skills/loom-drive/references/continuity-contract.md`, and
`skills/loom-drive/references/checkpoint-resume-protocol.md`.

# Blockers

Depends on `ticket:pktsupp1`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: ralph

Bounded iteration: drive handoff metadata grammar cleanup.
Write boundary: targeted drive template/reference wording, this ticket, one
evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `source_snapshot`, `drive_checkpoint`,
`gate_status`, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: undocumented support grammar creates recovery ambiguity.

Required critique profiles:

- records-grammar
- owner-boundary
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

- `ticket:pktsupp1`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-003`.
