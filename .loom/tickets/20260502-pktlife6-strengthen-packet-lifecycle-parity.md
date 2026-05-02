---
id: ticket:pktlife6
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
  - ticket:pktgram5
---

# Summary

Strengthen critique/wiki packet lifecycle and parent merge reconciliation parity
with Ralph packet discipline.

# Context

Council finding `CR-006` found critique/wiki packet templates can leave
`parent_merge_scope` empty and do not strongly require status movement from
`compiled` after reconciliation.

# Why Now

Packet output must be reconciled into owner truth rather than left in support
artifacts.

# Scope

- Require explicit critique/wiki packet merge targets or `None - rationale`.
- Add Done Means guidance for packet status movement to terminal states.
- Align critique/wiki packet templates with shared packet lifecycle grammar.

# Out Of Scope

- Do not make critique/wiki packets Ralph packets.
- Do not require packetization for every critique or wiki pass.
- Do not change canonical critique/wiki ownership.

# Acceptance Criteria

- ACC-001: Critique/wiki packet templates require parent merge targets or explicit
  rationale.
- ACC-002: Critique/wiki packet guidance requires terminal lifecycle status after
  reconciliation.
- ACC-003: Domain skills explain parent merge notes and owner-layer reconciliation.
- ACC-004: Evidence records lifecycle/template searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-006`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-006` | pending | pending | open |
| `ticket:pktlife6#ACC-001` through `ticket:pktlife6#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-critique`, `skills/loom-wiki`, and
shared packet frontmatter lifecycle guidance.

# Blockers

Depends on `ticket:pktgram5`.

# Next Move / Next Route

Ralph implementation packet after dependency closes.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: align critique/wiki packet lifecycle and parent merge
requirements.
Write boundary: critique/wiki packet templates/references, shared packet lifecycle
guidance, this ticket, one evidence record, one critique record, and one Ralph
packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: searches for `parent_merge_scope`, `compiled`, terminal packet statuses,
and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: packet lifecycle affects support artifact reconciliation and
closure honesty.

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

- `ticket:pktgram5`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-006`.
