---
id: ticket:pktsupp1
kind: ticket
status: ready
change_class: protocol-authority
risk_class: high
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
depends_on: []
---

# Summary

Clarify that packets own their own support-artifact lifecycle status without
owning project truth or ticket live state.

# Context

Council finding `NC-001` found packet/support wording that can be read as saying
packets do not own lifecycle status, while shared lifecycle grammar gives packets
`compiled`, `consumed`, `superseded`, and `abandoned`.

# Why Now

Fresh agents must reconcile packet lifecycle after Ralph, critique, and wiki
packet use without accidentally treating packets as canonical owner layers.

# Scope

- Audit packet/support lifecycle wording in records, workspace, and naming
  references.
- Clarify the split between packet support lifecycle status and canonical project
  truth ownership.
- Preserve packet non-canonical support-artifact doctrine.

# Out Of Scope

- Do not make packets own live ticket state, critique verdicts, accepted wiki
  truth, or intended behavior.
- Do not add lifecycle automation or validators.

# Acceptance Criteria

- ACC-001: Product guidance says packets own their own packet lifecycle status.
- ACC-002: Product guidance still says packets do not own project truth or ticket
  live state.
- ACC-003: Packet lifecycle values align with shared status lifecycle grammar.
- ACC-004: Evidence records before/after lifecycle wording searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-001`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-001` | pending | pending | open |
| `ticket:pktsupp1#ACC-001` through `ticket:pktsupp1#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-records/references/naming-and-ids.md`,
`skills/loom-workspace/references/workspace-tree.md`, and
`skills/loom-records/references/status-lifecycle.md`.

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet.

# Route Readiness

Route: ralph

Bounded iteration: packet support lifecycle wording repair.
Write boundary: targeted `skills/**` wording, this ticket, one evidence record,
one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for packet lifecycle / support truth wording and
`git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: packet lifecycle grammar affects handoff recovery and support
artifact authority.

Required critique profiles:

- owner-boundary
- records-grammar
- routing-safety

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

None.

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-001`.
