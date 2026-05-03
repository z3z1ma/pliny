---
id: ticket:readwsh23
kind: ticket
status: ready
change_class: documentation-explanation
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

Add a README note that workspace and harness metadata are support metadata.

# Context

The README support-surface table names packet, memory, and support, while corpus
doctrine also treats `.loom/workspace.md` and `.loom/harness.md` as support
metadata.

# Why Now

The README is a high-level orientation surface and should not leave workspace /
harness metadata ambiguous.

# Scope

- Add a small README note that workspace and harness metadata help entry,
  routing, and environment recovery without owning project truth.

# Out Of Scope

- Do not expand README into full workspace doctrine.
- Do not make workspace/harness metadata canonical project truth.

# Acceptance Criteria

- ACC-001: README states workspace and harness metadata are support metadata.
- ACC-002: README says those metadata surfaces do not own project truth.
- ACC-003: README support surface framing stays concise.
- ACC-004: Evidence records targeted README support metadata searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-024`
- `ticket:readwsh23#ACC-001`
- `ticket:readwsh23#ACC-002`
- `ticket:readwsh23#ACC-003`
- `ticket:readwsh23#ACC-004`
- `ticket:readwsh23#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-024` | pending | pending | open |
| `ticket:readwsh23#ACC-001` | pending | pending | open |
| `ticket:readwsh23#ACC-002` | pending | pending | open |
| `ticket:readwsh23#ACC-003` | pending | pending | open |
| `ticket:readwsh23#ACC-004` | pending | pending | open |
| `ticket:readwsh23#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `README.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: README workspace/harness support metadata note.
Write boundary: README support surface section only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, README framing observations, and critique
recommendation.

# Evidence

Expected: targeted searches for workspace, harness, support metadata, project
truth boundary, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: README frames product truth for new operators.

Required critique profiles:

- product-framing
- support-boundary
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

- `ticket:shipacc1`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 12.
