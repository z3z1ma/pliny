---
id: ticket:yk89awl5
kind: ticket
status: closed
change_class: documentation-explanation
risk_class: medium
created_at: 2026-05-02T15:25:50Z
updated_at: 2026-05-02T16:45:19Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-perfection-council-followup
  plan:
    - plan:skills-corpus-perfection-council-followup
  packet:
    - packet:ralph-ticket-yk89awl5-20260502T163744Z
  evidence:
    - evidence:readme-bootstrap-authority-validation
  critique:
    - critique:readme-bootstrap-authority-review
external_refs: {}
depends_on:
  - ticket:3twzep5n
  - ticket:4ilnwsnl
  - ticket:lqiw3hvp
---

# Summary

Align README public framing with bootstrap authority around workflow skills,
packets, ledgers, and bounded implementation routing.

# Context

Council finding `COUNCIL-FIND-003` found README wording looser than bootstrap.
The README should not imply workflow skills can casually create ledgers or that a
packet itself is the route owner for bounded implementation.

# Why Now

README is the public entry point. If it is less strict than bootstrap, fresh
operators can learn the wrong mental model before the mandatory doctrine loads.

# Scope

- Replace README wording that says workflow skills do not create ledgers unless a
  new kind of work needs a durable place.
- Route bounded implementation through `loom-ralph` with a Ralph packet rather
  than `packet` as if packet were a route owner.
- Keep the README readable and compelling while matching bootstrap authority.

# Non-goals

- Do not rewrite README wholesale.
- Do not change bootstrap unless the prior tickets reveal a necessary exact
  wording alignment.
- Do not change product architecture or install guidance.

# Acceptance Criteria

- ACC-001: README states workflow skills coordinate routes through existing owner
  layers and do not create ledgers.
- ACC-002: README route table sends bounded implementation to Ralph with a Ralph
  packet.
- ACC-003: README remains consistent with bootstrap authority and packet sibling
  grammar.
- ACC-004: Evidence records README/bootstrap comparison and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-perfection-council-followup#OBJ-004`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-perfection-council-followup#OBJ-004` | `evidence:readme-bootstrap-authority-validation` | `critique:readme-bootstrap-authority-review` | supported |

# Execution Notes

Council affected README lines were around the route table and workflow section.
Use current line numbers, not stale council line numbers, during implementation.

# Blockers

None. Dependencies `ticket:3twzep5n`, `ticket:4ilnwsnl`, and `ticket:lqiw3hvp`
are closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:u02z7o9j`.

# Ralph Readiness

Bounded iteration: align README public framing with bootstrap authority.

Write boundary: `README.md`, possibly targeted bootstrap references only if
needed for exact alignment, this ticket, one evidence record, one critique
record, and the Ralph packet.

Likely verification posture: observation-first structural validation.

Expected output contract: changed files, evidence, critique, ticket closure
recommendation, and retrospective disposition.

# Evidence

Recorded:

- `evidence:readme-bootstrap-authority-validation` records `git diff --check`,
  targeted README searches, and manual comparison against bootstrap and packet
  sibling doctrine.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique for every ticket; README public
framing shapes operator behavior.

Required critique profiles:

- operator-clarity
- routing-safety
- protocol-change

Findings:

None - oracle critique passed with no findings.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle critique passed with no findings.

# Wiki Disposition

Retrospective disposition complete. Durable lessons were promoted directly into
the public product surface: README route and workflow wording now inherit
bootstrap authority and settled packet sibling grammar. No separate wiki page,
research record, spec, constitution decision, or memory entry is needed for this
ticket.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T16:45:19Z
Basis: Ralph packet `packet:ralph-ticket-yk89awl5-20260502T163744Z`; evidence
`evidence:readme-bootstrap-authority-validation`; oracle critique
`critique:readme-bootstrap-authority-review` with no findings.
Residual risks: validation and critique were structural/textual; future operator
interpretation is not proven beyond README/bootstrap corpus consistency.

# Dependencies

- `ticket:3twzep5n`
- `ticket:4ilnwsnl`
- `ticket:lqiw3hvp`

# Journal

- 2026-05-02T15:25:50Z: Created from council finding `COUNCIL-FIND-003`.
- 2026-05-02T16:37:44Z: Dependencies closed. Moved to active and compiled Ralph
  packet `packet:ralph-ticket-yk89awl5-20260502T163744Z` from commit
  `57f19fbf5eafede98d179978e14b736c0068bb69`.
- 2026-05-02T16:40:06Z: README alignment implemented, structural evidence
  recorded as `evidence:readme-bootstrap-authority-validation`, and ticket moved
  to `review_required` for mandatory oracle critique.
- 2026-05-02T16:45:19Z: Oracle critique passed with no findings. Recorded final
  critique, retrospective disposition, and acceptance; closed ticket.
