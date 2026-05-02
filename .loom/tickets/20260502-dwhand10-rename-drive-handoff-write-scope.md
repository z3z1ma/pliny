---
id: ticket:dwhand10
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
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
  - ticket:supp0x2a
  - ticket:authst4p
---

# Summary

Remove the drive handoff `write_scope` collision with packet write-scope grammar.

# Context

Council finding `CR-010` found drive outer-loop handoff `write_scope` can collide
with packet write-scope/legacy packet scope semantics.

# Why Now

The same grep key should not mean both proposal-time handoff permission and packet
child write boundary.

# Scope

- Rename drive handoff `write_scope` to a clearly support-local field such as
  `handoff_write_scope` or `proposal_write_scope`.
- Update drive handoff template, drive references, and records/frontmatter notes.
- Preserve explicit statement that this field is not Ralph `child_write_scope`.

# Out Of Scope

- Do not rename Ralph `child_write_scope`.
- Do not make drive handoffs packets.
- Do not add migration tooling for historical support artifacts.

# Acceptance Criteria

- ACC-001: Drive handoff template no longer uses ambiguous `write_scope`.
- ACC-002: References explain the replacement field as proposal-time support
  permission, not packet child authority.
- ACC-003: Searches show no remaining ambiguous drive-handoff `write_scope` use.
- ACC-004: Evidence records before/after searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-010`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-010` | pending | pending | open |
| `ticket:dwhand10#ACC-001` through `ticket:dwhand10#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-drive/templates/outer-loop-handoff.md`,
`skills/loom-drive/SKILL.md`, and `skills/loom-records/references/frontmatter.md`.

# Blockers

Depends on tickets `rtvocab1`, `supp0x2a`, and `authst4p`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: rename drive handoff write-scope field and reconcile docs.
Write boundary: drive handoff surfaces, records/frontmatter support notes, this
ticket, one evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: targeted searches for `write_scope`, `handoff_write_scope`,
`proposal_write_scope`, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique; field collision affects authority
audits.

Required critique profiles:

- records-grammar
- routing-safety
- operator-clarity

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
- `ticket:supp0x2a`
- `ticket:authst4p`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-010`.
