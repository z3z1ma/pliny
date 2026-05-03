---
id: ticket:phvalid16
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

Add saved-record placeholder validation guidance.

# Context

Templates intentionally use `<TBD: ...>` placeholders, but saved `.loom` records
should not retain unresolved template placeholders unless explicitly documenting
observed source text.

# Why Now

Placeholder leakage can make a saved record look valid while carrying fake truth.

# Scope

- Add a placeholder scan recipe to record validation guidance.
- State the saved-record rule and exception for documented observed text.
- Preserve intentional template placeholders.

# Out Of Scope

- Do not add a validator runtime or schema engine.
- Do not rewrite all templates.

# Acceptance Criteria

- ACC-001: Validation guidance includes a saved `.loom` placeholder scan.
- ACC-002: Guidance states saved records must not contain unresolved template
  placeholders, example IDs, or generic TODO/TBD tokens unless explicitly
  documented as observed source text.
- ACC-003: Guidance does not make intentional template placeholders failures.
- ACC-004: Evidence records targeted placeholder validation searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-017`
- `ticket:phvalid16#ACC-001`
- `ticket:phvalid16#ACC-002`
- `ticket:phvalid16#ACC-003`
- `ticket:phvalid16#ACC-004`
- `ticket:phvalid16#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-017` | pending | pending | open |
| `ticket:phvalid16#ACC-001` | pending | pending | open |
| `ticket:phvalid16#ACC-002` | pending | pending | open |
| `ticket:phvalid16#ACC-003` | pending | pending | open |
| `ticket:phvalid16#ACC-004` | pending | pending | open |
| `ticket:phvalid16#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-records/references/validation.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: saved-record placeholder validation rule.
Write boundary: records validation reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, placeholder scan observations, and
critique recommendation.

# Evidence

Expected: targeted searches for placeholder scan, saved record rule, template
exception, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: validation guidance controls closure honesty.

Required critique profiles:

- validation-honesty
- template-safety
- workflow-boundary

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

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 5.
