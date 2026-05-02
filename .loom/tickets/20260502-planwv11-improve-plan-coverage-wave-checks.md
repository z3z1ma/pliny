---
id: ticket:planwv11
kind: ticket
status: ready
change_class: protocol-authority
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
  - ticket:rtvocab1
  - ticket:retrod3p
  - ticket:pktgram5
---

# Summary

Improve plan acceptance coverage and parallel-wave independence checks.

# Context

Council finding `CR-011` found plan templates do not fully model spec/ticket claim
mapping or execution-wave independence/write-scope overlap checks.

# Why Now

Plans bridge strategy into tickets and may authorize parallel Ralph. Unsafe plan
defaults can create downstream ambiguity or overlap.

# Scope

- Add plan template/reference cues for spec-to-ticket or initiative-to-ticket
  claim coverage.
- Add explicit parallel-wave independence and write-scope overlap checks.
- Cross-link to Ralph/Git parallel guidance where useful.

# Out Of Scope

- Do not make plans own ticket execution progress.
- Do not require parallel execution.
- Do not add a planner runtime.

# Acceptance Criteria

- ACC-001: Plan template/readiness cues claim/acceptance coverage mapping.
- ACC-002: Execution waves require independence and write-scope overlap checks or
  explicit `None - reason`.
- ACC-003: Parallel guidance preserves ticket and packet authority boundaries.
- ACC-004: Evidence records before/after plan-wave searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-011`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-011` | pending | pending | open |
| `ticket:planwv11#ACC-001` through `ticket:planwv11#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-plans/templates/plan.md`,
`skills/loom-plans/references/plan-shape.md`, and relevant Ralph/Git cross-links.

# Blockers

Depends on tickets `rtvocab1`, `retrod3p`, and `pktgram5`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: add plan coverage and parallel-wave readiness checks.
Write boundary: plan/Ralph/Git guidance, this ticket, one evidence record, one
critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: searches for `Execution Waves`, `write scope`, `claim coverage`,
`parallel`, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique; plan guidance can authorize unsafe
parallel work.

Required critique profiles:

- routing-safety
- operator-clarity
- records-grammar

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
- `ticket:retrod3p`
- `ticket:pktgram5`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-011`.
