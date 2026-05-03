---
id: ticket:wssupp4
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T00:56:36Z
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
external_refs: {}
depends_on: []
---

# Summary

Complete workspace/support lifecycle and query grammar without making support
surfaces canonical.

# Context

Council finding `NC2-004` and older audit actions 1 and 5 found residual gaps in
workspace/support status and query grammar even though `.loom/support/` framing is
mostly now present.

# Why Now

Workspace and support files help recovery. If lifecycle/query guidance omits them,
fresh agents may treat them as accidental or, conversely, as canonical owner
layers.

# Scope

- Add `kind: workspace` lifecycle guidance.
- Extend query/discovery examples for `.loom/workspace.md`, `.loom/harness.md`,
  and optional `.loom/support/` paths.
- Preserve the noncanonical support boundary for workspace metadata, harness
  records, memory, packets, and support artifacts.

# Out Of Scope

- Do not make `.loom/support/` part of required bootstrap materialization.
- Do not make workspace/harness records own project truth.
- Do not add a validator or schema engine.

# Acceptance Criteria

- ACC-001: Status lifecycle includes `kind: workspace` with clear lifecycle
  values.
- ACC-002: Query/linking guidance discovers workspace, harness, and support paths
  without treating them as canonical owners.
- ACC-003: Naming/path guidance remains consistent with lazy-materialized
  `.loom/support/drive-handoffs/` support.
- ACC-004: Evidence records before/after workspace/support searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-006`
- `ticket:wssupp4#ACC-001`
- `ticket:wssupp4#ACC-002`
- `ticket:wssupp4#ACC-003`
- `ticket:wssupp4#ACC-004`
- `ticket:wssupp4#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-006` | pending | pending | open |
| `ticket:wssupp4#ACC-001` through `ticket:wssupp4#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include status lifecycle, query/linking, naming/IDs, and
workspace tree guidance.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: workspace/support lifecycle and query grammar cleanup.
Write boundary: workspace/support grammar references, this ticket, one evidence
record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `kind: workspace`, `.loom/workspace.md`,
`.loom/harness.md`, `.loom/support`, `drive-handoffs`, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: workspace/support grammar affects recovery and owner-boundary
safety.

Required critique profiles:

- owner-boundary
- records-grammar
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

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-004` and older audit
  actions 1 and 5.
