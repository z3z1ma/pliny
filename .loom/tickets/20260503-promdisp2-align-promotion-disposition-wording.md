---
id: ticket:promdisp2
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

Align closure and handoff wording so retrospective / promotion disposition is
broader than wiki disposition.

# Context

Council finding `NC2-001` found residual shorthand that still says or implies
wiki disposition where the correct closure gate is broader retrospective /
promotion disposition.

# Why Now

Fresh agents can miss research, spec, plan, initiative, constitution, evidence,
or memory promotions when closure guidance names only wiki follow-through.

# Scope

- Replace stale wiki-only closure shorthand with retrospective / promotion
  disposition language in affected bootstrap/workflow/public surfaces.
- Keep wiki disposition as route-specific when wiki promotion is selected.
- Preserve `completed`, `deferred`, `not_required`, and `blocking` outcomes where
  ticket closure needs them.

# Out Of Scope

- Do not create a new retrospective record kind.
- Do not require wiki promotion for every ticket.
- Do not rewrite unrelated README or workflow prose for style.

# Acceptance Criteria

- ACC-001: Closure/handoff guidance names retrospective / promotion disposition
  rather than treating wiki disposition as the only follow-through gate.
- ACC-002: Wiki disposition remains route-specific and does not replace broader
  promotion disposition.
- ACC-003: Ticket closure guidance still allows honest `not_required` and
  `deferred` dispositions when justified.
- ACC-004: Evidence records before/after promotion/wiki disposition searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-004`
- `ticket:promdisp2#ACC-001`
- `ticket:promdisp2#ACC-002`
- `ticket:promdisp2#ACC-003`
- `ticket:promdisp2#ACC-004`
- `ticket:promdisp2#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-004` | pending | pending | open |
| `ticket:promdisp2#ACC-001` through `ticket:promdisp2#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include bootstrap validation/critique references, Ralph
work driver, ship/git guidance, and README workflow wording if still stale.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: promotion disposition wording cleanup.
Write boundary: affected promotion/wiki closure wording surfaces, this ticket,
one evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `wiki disposition`, `retrospective`,
`promotion disposition`, closure wording, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: promotion gate ambiguity can make closure skip required durable
learning follow-through.

Required critique profiles:

- closure-honesty
- workflow-boundary
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

- 2026-05-03T00:56:36Z: Created from council finding `NC2-001`.
