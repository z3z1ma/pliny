---
id: ticket:critfail3
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T01:39:16Z
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
  packet:
    - packet:ralph-ticket-critfail3-20260503T013234Z
  evidence:
    - evidence:mandatory-critique-template-validation
  critique:
    - critique:mandatory-critique-template-review
external_refs: {}
depends_on: []
---

# Summary

Make the ticket template locally fail closed for mandatory critique disposition.

# Context

Council finding `NC2-002` found that the ticket template lists critique
disposition statuses but does not locally say mandatory critique cannot close as
`deferred` or `not_required`.

# Why Now

Fresh agents often copy templates before reading every reference. The ticket
template should carry the closure-critical mandatory critique rule directly.

# Scope

- Add a fail-closed note to the ticket template critique disposition section.
- Preserve the distinction between mandatory, recommended, and optional critique.
- Keep ticket-owned finding dispositions separate from critique-owned finding
  states and verdicts.

# Out Of Scope

- Do not change the ticket state machine.
- Do not make recommended critique a hard closure blocker unless a ticket or human
  gate requires it.

# Acceptance Criteria

- ACC-001: Ticket template says mandatory critique remains pending/blocking until
  final critique exists.
- ACC-002: Ticket template says open medium/high mandatory critique findings need
  ticket-owned dispositions before closure.
- ACC-003: Template keeps `deferred` / `not_required` closure-compatible only for
  recommended/optional critique with rationale, not mandatory critique.
- ACC-004: Evidence records before/after critique disposition searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-005`
- `ticket:critfail3#ACC-001`
- `ticket:critfail3#ACC-002`
- `ticket:critfail3#ACC-003`
- `ticket:critfail3#ACC-004`
- `ticket:critfail3#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-005` | `evidence:mandatory-critique-template-validation` | `critique:mandatory-critique-template-review` | supported |
| `ticket:critfail3#ACC-001` | `evidence:mandatory-critique-template-validation` | `critique:mandatory-critique-template-review` | supported |
| `ticket:critfail3#ACC-002` | `evidence:mandatory-critique-template-validation` | `critique:mandatory-critique-template-review` | supported |
| `ticket:critfail3#ACC-003` | `evidence:mandatory-critique-template-validation` | `critique:mandatory-critique-template-review` | supported |
| `ticket:critfail3#ACC-004` | `evidence:mandatory-critique-template-validation` | `critique:mandatory-critique-template-review` | supported |
| `ticket:critfail3#ACC-005` | `critique:mandatory-critique-template-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces are `skills/loom-tickets/templates/ticket.md` and, only if
needed, `skills/loom-tickets/references/acceptance-gate.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:wssupp4`.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:mandatory-critique-template-validation` and oracle critique
`critique:mandatory-critique-template-review` support closure with no findings.

# Evidence

`evidence:mandatory-critique-template-validation` supports `ACC-001` through
`ACC-004` with before/after searches for `Critique policy`, `mandatory`,
`deferred`, `not_required`, `Disposition status`, `draft/stub`, open medium/high
findings, ticket-owned dispositions, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: ticket template closure gates directly shape ticket acceptance.

Required critique profiles:

- closure-honesty
- template-safety
- owner-boundary

Findings:

`critique:mandatory-critique-template-review` - no findings; mandatory oracle
critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Mandatory critique fail-closed guidance was promoted directly into the ticket
  template critique disposition section.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
ticket template guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T01:39:16Z
Basis: Ralph packet `packet:ralph-ticket-critfail3-20260503T013234Z`; evidence
`evidence:mandatory-critique-template-validation`; oracle critique
`critique:mandatory-critique-template-review` with no findings.
Residual risks: validation is structural/manual; there is no automated
protocol-template test suite.

# Dependencies

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-002`.
- 2026-05-03T01:32:34Z: Moved to `active` and compiled
  `packet:ralph-ticket-critfail3-20260503T013234Z` for ticket template mandatory
  critique fail-closed guidance.
- 2026-05-03T01:34:06Z: Added the mandatory critique fail-closed template note,
  recorded `evidence:mandatory-critique-template-validation`, and moved to
  `review_required` for mandatory oracle critique.
- 2026-05-03T01:36:39Z: Parent reconciled Ralph output, marked
  `packet:ralph-ticket-critfail3-20260503T013234Z` consumed, and normalized claim
  matrix pending-review statuses to `supported_pending_review` before oracle
  critique.
- 2026-05-03T01:39:16Z: Mandatory oracle critique
  `critique:mandatory-critique-template-review` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
