---
id: ticket:rtvocab1
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
depends_on: []
---

# Summary

Create one canonical, grep-friendly route vocabulary and align drive, ticket,
workspace, and template route wording to it.

# Context

Council finding `CR-001` found route tokens drifting across drive/checkpoint,
ticket readiness, workspace status, and examples: `ask_user`, `ask-user`, `ask
user`, `Ralph`, `acceptance`, `acceptance_review`, `continue`, and related prose.

# Why Now

Route vocabulary is foundational. Later tickets should inherit one safe route
grammar instead of normalizing around drift.

# Scope

- Define a canonical route vocabulary in an owner-appropriate shared reference.
- Update downstream route examples in `loom-drive`, `loom-tickets`,
  `loom-workspace`, and affected templates.
- Preserve route readability without turning every normal sentence into an enum.
- Keep workflow routes separate from command or adapter invocation names.

# Out Of Scope

- Do not add a runtime validator or command router.
- Do not change ticket state-machine statuses unless required by route grammar.
- Do not rename existing record kinds or workflow skills.

# Acceptance Criteria

- ACC-001: A single shared route-vocabulary reference or section owns the route
  tokens used for next-route/checkpoint/resume guidance.
- ACC-002: Drive, ticket, and workspace route examples align with the shared
  vocabulary.
- ACC-003: Route vocabulary stays distinct from ticket lifecycle statuses,
  command names, and adapter invocation surfaces.
- ACC-004: Evidence records before/after token searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-001`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-001` | pending | pending | open |
| `ticket:rtvocab1#ACC-001` through `ticket:rtvocab1#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-records`, `skills/loom-drive`,
`skills/loom-tickets`, `skills/loom-workspace`, and route-bearing templates.

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet.

# Route Readiness

Route: Ralph implementation packet

Ralph readiness, required only when the next route is Ralph:

Bounded iteration: normalize shared route vocabulary and update direct downstream
uses.
Write boundary: `skills/loom-records/**`, `skills/loom-drive/**`,
`skills/loom-tickets/**`, `skills/loom-workspace/**`, this ticket, one evidence
record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, before/after route-token searches,
evidence, ticket update, and critique recommendation.

# Evidence

Expected: targeted route-token searches, manual comparison of shared route grammar
against downstream examples, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: route vocabulary affects checkpoint recovery and workflow
routing safety.

Required critique profiles:

- protocol-change
- operator-clarity
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

None.

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-001`.
