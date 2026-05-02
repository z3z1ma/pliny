---
id: ticket:supp0x2a
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

Make `.loom/support/` handling explicit and non-canonical wherever saved support
artifacts and workspace shape are taught.

# Context

Council finding `CR-002` found `.loom/support/drive-handoffs/` taught by drive but
not consistently reflected in workspace tree, README runtime tree, status, or
support artifact doctrine.

# Why Now

Support paths must be discoverable without becoming hidden shadow truth.

# Scope

- Decide the corpus wording for `.loom/support/` as optional, lazy-materialized,
  non-canonical support surface.
- Align workspace tree/status, drive handoff, and records/frontmatter guidance.
- Update README only if product framing would otherwise diverge from skills.

# Out Of Scope

- Do not make `.loom/support/` a canonical owner layer.
- Do not require saved drive handoffs for normal operation.
- Do not add support artifact runtime tooling.

# Acceptance Criteria

- ACC-001: `.loom/support/` is either consistently documented as optional
  non-canonical support or saved support handoffs are demoted from product
  guidance.
- ACC-002: Workspace tree/status and drive handoff guidance agree.
- ACC-003: Support surfaces explicitly do not own objective state, live ticket
  state, acceptance, evidence sufficiency, critique verdicts, wiki truth,
  canonical truth, or packet lifecycle.
- ACC-004: Evidence records before/after support-path searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-002`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-002` | pending | pending | open |
| `ticket:supp0x2a#ACC-001` through `ticket:supp0x2a#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-workspace/references/workspace-tree.md`,
`skills/loom-drive`, `skills/loom-records/references/frontmatter.md`, and README
runtime tree if needed.

# Blockers

Depends on `ticket:rtvocab1`.

# Next Move / Next Route

Ralph implementation packet after dependency closes.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: align optional `.loom/support/` doctrine and discovery.
Write boundary: support-surface documentation/templates, this ticket, one evidence
record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, targeted support-path searches, evidence,
ticket update, and critique recommendation.

# Evidence

Expected: targeted `.loom/support`, `drive-handoffs`, and support ownership
searches; workspace tree comparison; `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: support-surface wording can create shadow paths if ambiguous.

Required critique profiles:

- protocol-change
- records-grammar
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

- 2026-05-02T18:58:43Z: Created from council finding `CR-002`.
