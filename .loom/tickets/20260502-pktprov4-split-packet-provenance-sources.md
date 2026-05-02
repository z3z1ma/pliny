---
id: ticket:pktprov4
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

Define the split between packet `source_fingerprint.compiled_from` provenance and
the packet `sources` context set.

# Context

Council finding `NC-004` found semantic overlap between `compiled_from` and
`sources` in packet frontmatter guidance and packet templates.

# Why Now

Packet provenance should remain inspectable without performative duplication or
inconsistent source lists.

# Scope

- Clarify `compiled_from` as provenance for packet compilation baseline.
- Clarify `sources` as context sources the child/reviewer/synthesizer should read.
- Align Ralph, critique, and wiki packet templates with the split.

# Out Of Scope

- Do not add a parser or schema.
- Do not make critique/wiki packets Ralph-governed.

# Acceptance Criteria

- ACC-001: Shared packet frontmatter defines the provenance/context split.
- ACC-002: Ralph, critique, and wiki packet templates align with the split.
- ACC-003: Packet family boundaries remain intact.
- ACC-004: Evidence records packet provenance/source searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-004`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-004` | pending | pending | open |
| `ticket:pktprov4#ACC-001` through `ticket:pktprov4#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-records/references/packet-frontmatter.md`
and packet templates under `skills/loom-ralph`, `skills/loom-critique`, and
`skills/loom-wiki`.

# Blockers

Depends on `ticket:pktsupp1`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: ralph

Bounded iteration: packet provenance/source grammar alignment.
Write boundary: targeted packet references/templates, this ticket, one evidence
record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `compiled_from`, `sources:`, packet templates,
and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: packet provenance ambiguity weakens replayable handoff contracts.

Required critique profiles:

- records-grammar
- routing-safety
- owner-boundary

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

- 2026-05-02T22:03:13Z: Created from council finding `NC-004`.
