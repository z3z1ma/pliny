---
id: ticket:revtgt7x
kind: ticket
status: ready
change_class: record-hygiene
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
  - ticket:pktlife6
---

# Summary

Canonicalize or explicitly document `review_target` shape across critique records
and critique packets.

# Context

Council finding `CR-007` found `review_target` appears as a scalar in critique
records and a mapping in critique packets.

# Why Now

Shared fields should be grep-friendly and validation-friendly without requiring a
runtime parser.

# Scope

- Decide whether `review_target` is one canonical shape or two explicitly allowed
  variants.
- Update critique templates and frontmatter grammar accordingly.
- Preserve usability for direct artifact critique and packetized critique.

# Out Of Scope

- Do not bulk-normalize every historical critique record unless necessary.
- Do not add schema validation.
- Do not change critique ownership.

# Acceptance Criteria

- ACC-001: `review_target` grammar is explicit in shared frontmatter or critique
  references.
- ACC-002: Critique record and critique packet templates align with that grammar.
- ACC-003: The chosen shape remains easy to grep and human-read.
- ACC-004: Evidence records before/after `review_target` searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-007`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-007` | pending | pending | open |
| `ticket:revtgt7x#ACC-001` through `ticket:revtgt7x#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-critique/templates/critique.md`,
`skills/loom-critique/templates/critique-packet.md`, and `skills/loom-records/references/frontmatter.md`.

# Blockers

Depends on `ticket:pktlife6`.

# Next Move / Next Route

Ralph implementation packet after dependency closes.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: align `review_target` grammar and critique templates.
Write boundary: critique/frontmatter grammar surfaces, this ticket, one evidence
record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: `review_target` shape searches and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique for every ticket; shared fields
affect record grammar.

Required critique profiles:

- records-grammar
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

- `ticket:pktlife6`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-007`.
