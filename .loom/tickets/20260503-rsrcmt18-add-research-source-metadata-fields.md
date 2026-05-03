---
id: ticket:rsrcmt18
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T06:20:11Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-third-pass-follow-up-validation
external_refs: {}
depends_on:
  - ticket:shipacc1
---

# Summary

Add copyable source metadata fields to the research template.

# Context

Research source-handling doctrine is stronger than the template's prose-only
`# Sources` section.

# Why Now

Research is a primary place where external documents can accidentally become
shadow truth if provenance, freshness, and trust limits are not explicit.

# Scope

- Add source metadata prompts to `skills/loom-research/templates/research.md`.
- Align fields with source-handling doctrine.

# Out Of Scope

- Do not require full raw source dumps.
- Do not make external sources canonical project truth.

# Acceptance Criteria

- ACC-001: Research template prompts for title/type, URL or path, observed time,
  version/date/commit, freshness risk, recheck trigger, and trust rationale.
- ACC-002: Template preserves research as evidence synthesis, not external source
  authority.
- ACC-003: Source-handling reference remains consistent with template fields.
- ACC-004: Evidence records targeted source metadata searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-019`
- `ticket:rsrcmt18#ACC-001`
- `ticket:rsrcmt18#ACC-002`
- `ticket:rsrcmt18#ACC-003`
- `ticket:rsrcmt18#ACC-004`
- `ticket:rsrcmt18#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-019` | pending | pending | open |
| `ticket:rsrcmt18#ACC-001` | pending | pending | open |
| `ticket:rsrcmt18#ACC-002` | pending | pending | open |
| `ticket:rsrcmt18#ACC-003` | pending | pending | open |
| `ticket:rsrcmt18#ACC-004` | pending | pending | open |
| `ticket:rsrcmt18#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-research/templates/research.md`; source-handling
reference only if alignment wording is needed.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: research source metadata template fields.
Write boundary: research template and directly related source-handling wording
only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, source metadata observations, and critique
recommendation.

# Evidence

Expected: targeted searches for source metadata fields, freshness/recheck/trust
wording, source authority boundary, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: research source metadata affects external-source trust.

Required critique profiles:

- trust-boundary
- operator-clarity
- template-safety

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

- `ticket:shipacc1`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 7.
