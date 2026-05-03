---
id: ticket:readrte29
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
  - ticket:readwsh23
---

# Summary

Frame the README routing table as introductory and point to route vocabulary for
complete saved-field grammar.

# Context

The README has an introductory routing table, while `route-vocabulary.md` owns the
complete saved-field route vocabulary.

# Why Now

New readers should not treat the README table as the complete route-token source.

# Scope

- Add concise README wording that the route table is introductory.
- Point to `skills/loom-records/references/route-vocabulary.md` as the complete
  saved-field vocabulary owner.

# Out Of Scope

- Do not duplicate the full route vocabulary in README.
- Do not change route tokens.

# Acceptance Criteria

- ACC-001: README routing table is framed as introductory.
- ACC-002: README points to `route-vocabulary.md` for complete saved-field route
  grammar.
- ACC-003: README remains concise and product-facing.
- ACC-004: Evidence records targeted README route-table searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-030`
- `ticket:readrte29#ACC-001`
- `ticket:readrte29#ACC-002`
- `ticket:readrte29#ACC-003`
- `ticket:readrte29#ACC-004`
- `ticket:readrte29#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-030` | pending | pending | open |
| `ticket:readrte29#ACC-001` | pending | pending | open |
| `ticket:readrte29#ACC-002` | pending | pending | open |
| `ticket:readrte29#ACC-003` | pending | pending | open |
| `ticket:readrte29#ACC-004` | pending | pending | open |
| `ticket:readrte29#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `README.md`.

# Blockers

Blocked until `ticket:shipacc1` and `ticket:readwsh23` close.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: README route-table introductory framing.
Write boundary: README routing section only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, README route framing observations, and
critique recommendation.

# Evidence

Expected: targeted searches for introductory, route vocabulary, saved-field
grammar, route table, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: README route framing can mislead fresh operators.

Required critique profiles:

- route-vocabulary
- product-framing
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
- `ticket:readwsh23`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass secondary polish finding.
