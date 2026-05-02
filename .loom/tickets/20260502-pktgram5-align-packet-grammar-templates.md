---
id: ticket:pktgram5
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

Align shared packet frontmatter grammar and Ralph/critique/wiki packet templates.

# Context

Council finding `CR-005` found drift around `context_budget.posture`, `iteration`,
`change_class`, optional `risk_class`, source freshness checks, and packet ID vs
filename mapping.

# Why Now

Packet templates are operational teaching surfaces. They need to embody shared
grammar before lifecycle parity and critique target cleanup proceed.

# Scope

- Align `skills/loom-records/references/packet-frontmatter.md` with Ralph,
  critique, and wiki packet templates.
- Clarify `iteration`, `change_class`, optional `risk_class`, ID/filename mapping,
  context budget defaults, and freshness stop conditions.
- Preserve distinction between Ralph implementation packets and critique/wiki
  sibling packet workflows.

# Out Of Scope

- Do not make critique/wiki packets Ralph-governed.
- Do not add a packet parser or schema runtime.
- Do not normalize historical packets unless needed for current references.

# Acceptance Criteria

- ACC-001: Packet frontmatter reference and packet templates agree on required
  and optional fields.
- ACC-002: Packet ID and filename conventions are explicit.
- ACC-003: `change_class`, optional `risk_class`, `iteration`, context budget, and
  source freshness expectations are documented or removed consistently.
- ACC-004: Evidence records packet-template comparison and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-005` | pending | pending | open |
| `ticket:pktgram5#ACC-001` through `ticket:pktgram5#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-records/references/packet-frontmatter.md`,
`skills/loom-ralph/templates/ralph-packet.md`, `skills/loom-critique/templates/critique-packet.md`,
and `skills/loom-wiki/templates/wiki-packet.md`.

# Blockers

Depends on `ticket:rtvocab1`.

# Next Move / Next Route

Ralph implementation packet after dependency closes.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: align shared packet grammar and packet templates.
Write boundary: packet references/templates, this ticket, one evidence record, one
critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, packet-template comparison, evidence,
ticket update, and critique recommendation.

# Evidence

Expected: targeted packet-field searches, template/reference comparison, and
`git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: packet grammar governs bounded child authority.

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

- 2026-05-02T18:58:43Z: Created from council finding `CR-005`.
