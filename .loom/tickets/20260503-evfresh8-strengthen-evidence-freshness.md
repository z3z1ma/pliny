---
id: ticket:evfresh8
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

Strengthen evidence freshness metadata and negative-evidence examples.

# Context

Older audit action 7 found that evidence freshness doctrine exists but the
template could make source state, command/procedure, exit code/verdict, raw
artifacts, and challenging evidence more visible.

# Why Now

Evidence supports acceptance, critique, and wiki/research claims. If freshness and
challenge paths are under-specified, agents can overclaim green evidence or miss
observations that falsify a claim.

# Scope

- Add observation metadata or equivalent fields to the evidence template.
- Make freshness fields harder to skip.
- Add a negative/challenging evidence example in claim coverage or evidence
  guidance.
- Preserve evidence as observed artifact truth, not acceptance or critique truth.

# Out Of Scope

- Do not require every evidence record to store full raw logs inline.
- Do not make evidence own intended behavior, critique verdicts, or ticket closure.

# Acceptance Criteria

- ACC-001: Evidence template asks for observed-at/source-state/procedure/verdict
  or equivalent metadata.
- ACC-002: Evidence template makes freshness, invalidation, and recheck triggers
  explicit.
- ACC-003: Claim coverage or evidence guidance includes a concrete challenge
  example for negative evidence.
- ACC-004: Evidence records before/after evidence freshness/challenge searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-010`
- `ticket:evfresh8#ACC-001`
- `ticket:evfresh8#ACC-002`
- `ticket:evfresh8#ACC-003`
- `ticket:evfresh8#ACC-004`
- `ticket:evfresh8#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-010` | pending | pending | open |
| `ticket:evfresh8#ACC-001` through `ticket:evfresh8#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-evidence/templates/evidence.md`,
`skills/loom-evidence/SKILL.md`, and
`skills/loom-records/references/claim-coverage.md`.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: evidence freshness and challenge example cleanup.
Write boundary: evidence/claim coverage guidance, this ticket, one evidence
record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `Fresh enough for`, `Invalidated by`,
`Challenges Claims`, `exit code`, `verdict`, `source state`, and
`git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: evidence freshness and negative evidence directly affect
acceptance honesty.

Required critique profiles:

- evidence-quality
- closure-honesty
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

- 2026-05-03T00:56:36Z: Created from older audit action 7.
