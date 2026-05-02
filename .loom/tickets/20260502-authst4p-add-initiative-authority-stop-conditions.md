---
id: ticket:authst4p
kind: ticket
status: ready
change_class: protocol-authority
risk_class: high
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T18:58:43Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
external_refs: {}
depends_on:
  - ticket:rtvocab1
---

# Summary

Add initiative guidance for delegated autonomy, authority limits, and objective
level stop conditions.

# Context

Council finding `CR-004` found `loom-drive` says initiatives own delegated
autonomy and objective-level stop conditions, but initiative template/reference do
not cue those fields.

# Why Now

Autonomous drive sessions should not rely on transcript memory for authority
boundaries.

# Scope

- Add optional delegated authority and stop-condition prompts to initiative
  template/reference.
- Align drive continuity contract with the initiative template language.
- Keep the section optional for non-drive initiatives.

# Out Of Scope

- Do not require all initiatives to use autonomous drive.
- Do not grant autonomy outside recorded user delegation.
- Do not create a new authority record type.

# Acceptance Criteria

- ACC-001: Initiative template cues delegated authority/autonomy limits and
  objective-level stop conditions.
- ACC-002: Initiative reference explains when the fields are required or optional.
- ACC-003: Drive continuity guidance points to the same owner fields.
- ACC-004: Evidence records before/after authority/stop-condition searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-004`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-004` | pending | pending | open |
| `ticket:authst4p#ACC-001` through `ticket:authst4p#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-initiatives/templates/initiative.md`,
`skills/loom-initiatives/references/initiative-shape.md`, and `skills/loom-drive/references/continuity-contract.md`.

# Blockers

Depends on `ticket:rtvocab1`.

# Next Move / Next Route

Ralph implementation packet after dependency closes.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: add initiative delegated authority/stop-condition cues and
align drive continuity language.
Write boundary: initiative/drive guidance, this ticket, one evidence record, one
critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: targeted delegated-authority/stop-condition searches and
`git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: this governs autonomous objective boundaries.

Required critique profiles:

- protocol-change
- operator-clarity
- routing-safety

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

Not deferred.

# Wiki Disposition

Pending retrospective decision after critique.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

- `ticket:rtvocab1`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-004`.
