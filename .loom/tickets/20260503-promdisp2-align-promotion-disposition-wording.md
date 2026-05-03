---
id: ticket:promdisp2
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T01:31:03Z
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
    - packet:ralph-ticket-promdisp2-20260503T011837Z
    - packet:ralph-ticket-promdisp2-20260503T012242Z
  evidence:
    - evidence:promotion-disposition-wording-validation
  critique:
    - critique:promotion-disposition-wording-review
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
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-004` | `evidence:promotion-disposition-wording-validation` | `critique:promotion-disposition-wording-review` | supported |
| `ticket:promdisp2#ACC-001` | `evidence:promotion-disposition-wording-validation` | `critique:promotion-disposition-wording-review` | supported |
| `ticket:promdisp2#ACC-002` | `evidence:promotion-disposition-wording-validation` | `critique:promotion-disposition-wording-review` | supported |
| `ticket:promdisp2#ACC-003` | `evidence:promotion-disposition-wording-validation` | `critique:promotion-disposition-wording-review` | supported |
| `ticket:promdisp2#ACC-004` | `evidence:promotion-disposition-wording-validation` | `critique:promotion-disposition-wording-review` | supported |
| `ticket:promdisp2#ACC-005` | `critique:promotion-disposition-wording-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include bootstrap validation/critique references, Ralph
work driver, ship/git guidance, and README workflow wording if still stale.

# Blockers

None. The iteration 1 scope blocker is resolved by replacement packet
`packet:ralph-ticket-promdisp2-20260503T012242Z`, which includes
`skills/loom-records/references/implementation-reality.md` in scope.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:critfail3`.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:promotion-disposition-wording-validation` and oracle critique
`critique:promotion-disposition-wording-review` support closure with no findings.

# Evidence

Recorded: `evidence:promotion-disposition-wording-validation` captures
before/after wording searches, route-specific wiki-disposition observations,
preserved disposition outcomes, and `git diff --check` for this implementation
iteration.

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

`critique:promotion-disposition-wording-review` - no findings; mandatory oracle
critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Retrospective / promotion disposition wording was promoted directly into the
  touched product/public guidance surfaces.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched closure and handoff guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T01:31:03Z
Basis: Ralph packets `packet:ralph-ticket-promdisp2-20260503T011837Z` and
`packet:ralph-ticket-promdisp2-20260503T012242Z`; evidence
`evidence:promotion-disposition-wording-validation`; oracle critique
`critique:promotion-disposition-wording-review` with no findings.
Residual risks: validation is pattern/search based and historical `.loom` records
may preserve older wording as audit history.

# Dependencies

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-001`.
- 2026-05-03T01:18:38Z: Moved to `active` and compiled
  `packet:ralph-ticket-promdisp2-20260503T011837Z` for promotion disposition
  wording cleanup.
- 2026-05-03T01:21:05Z: Ralph child stopped before product edits because
  before-state search found stale `wiki follow-through` wording in
  `skills/loom-records/references/implementation-reality.md` outside the packet
  child write scope; recorded
  `evidence:promotion-disposition-wording-validation` and moved the ticket to
  `blocked` for parent scope reconciliation.
- 2026-05-03T01:22:42Z: Parent consumed the blocked first packet as valid scope
  discovery and compiled replacement packet
  `packet:ralph-ticket-promdisp2-20260503T012242Z` with
  `skills/loom-records/references/implementation-reality.md` added to the write
  scope.
- 2026-05-03T01:24:53Z: Replacement Ralph iteration updated product wording,
  refreshed evidence, and moved the ticket to `review_required` for mandatory
  oracle critique with profiles `closure-honesty`, `workflow-boundary`, and
  `operator-clarity`.
- 2026-05-03T01:27:38Z: Parent reconciled replacement Ralph output, marked
  `packet:ralph-ticket-promdisp2-20260503T012242Z` consumed, and confirmed
  `git diff --check` passed before oracle critique.
- 2026-05-03T01:31:03Z: Mandatory oracle critique
  `critique:promotion-disposition-wording-review` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
