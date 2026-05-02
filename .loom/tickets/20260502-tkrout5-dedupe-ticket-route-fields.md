---
id: ticket:tkrout5
kind: ticket
status: closed
change_class: record-hygiene
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T22:55:23Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  packet:
    - packet:ralph-ticket-tkrout5-20260502T224954Z
  evidence:
    - evidence:ticket-route-field-validation
  critique:
    - critique:ticket-route-field-ownership-review
external_refs: {}
depends_on: []
---

# Summary

Make one ticket section own the next-route token and keep route readiness focused
on readiness details.

# Context

Council finding `NC-005` found that the ticket template repeats route-token
selection in both `Next Move / Next Route` and `Route Readiness`.

# Why Now

Duplicate route fields can drift and confuse fresh agents about which value owns
the next governed move.

# Scope

- Update ticket template/readiness guidance so one section owns the route token.
- Make the readiness section describe route-specific readiness, not duplicate
  route truth.
- Preserve ticket ownership of live execution state.

# Out Of Scope

- Do not remove route readiness guidance.
- Do not add route automation or validators.

# Acceptance Criteria

- ACC-001: Ticket template has one route-token owner.
- ACC-002: Route readiness describes readiness details without duplicating route
  truth.
- ACC-003: Ticket live-state ownership remains clear.
- ACC-004: Evidence records route-field searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-005` | `evidence:ticket-route-field-validation` | `critique:ticket-route-field-ownership-review` | supported |
| `ticket:tkrout5#ACC-001` | `evidence:ticket-route-field-validation` | `critique:ticket-route-field-ownership-review` | supported |
| `ticket:tkrout5#ACC-002` | `evidence:ticket-route-field-validation` | `critique:ticket-route-field-ownership-review` | supported |
| `ticket:tkrout5#ACC-003` | `evidence:ticket-route-field-validation` | `critique:ticket-route-field-ownership-review` | supported |
| `ticket:tkrout5#ACC-004` | `evidence:ticket-route-field-validation` | `critique:ticket-route-field-ownership-review` | supported |
| `ticket:tkrout5#ACC-005` | `critique:ticket-route-field-ownership-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-tickets/templates/ticket.md` and
`skills/loom-tickets/references/readiness.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:accspec6`.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:ticket-route-field-validation` and oracle critique
`critique:ticket-route-field-ownership-review` support closure with no findings.

# Evidence

Recorded: `evidence:ticket-route-field-validation` covers before/after searches
for `Next Move / Next Route`, `Route Readiness`, `Route:`, route-token lists,
`next route`, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: route-field drift can mislead recovery and acceptance routing.

Required critique profiles:

- routing-safety
- records-grammar
- operator-clarity

Findings:

`critique:ticket-route-field-ownership-review` - no findings; mandatory oracle
critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Ticket route-token ownership was promoted directly into
  `skills/loom-tickets/templates/ticket.md` and
  `skills/loom-tickets/references/readiness.md`.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the ticket grammar product wording itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched ticket guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T22:55:23Z
Basis: Ralph packet `packet:ralph-ticket-tkrout5-20260502T224954Z`; evidence
`evidence:ticket-route-field-validation`; oracle critique
`critique:ticket-route-field-ownership-review` with no findings.
Residual risks: validation is structural/manual. Evidence summarizes route-field
search results rather than preserving full raw `rg` output; exact replay would
require rerunning the recorded search.

# Dependencies

Plan sequence follows `ticket:pktprov4`.

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-005`.
- 2026-05-02T22:49:54Z: Compiled Ralph packet
  `packet:ralph-ticket-tkrout5-20260502T224954Z` and moved ticket to `active`.
- 2026-05-02T22:50:50Z: Ralph iteration updated ticket route-field guidance,
  recorded `evidence:ticket-route-field-validation`, and moved ticket to
  `review_required` for mandatory oracle critique.
- 2026-05-02T22:53:18Z: Parent reconciled Ralph output, normalized claim matrix
  statuses to canonical claim-coverage vocabulary, expanded evidence notes, and
  marked the Ralph packet consumed.
- 2026-05-02T22:55:23Z: Mandatory oracle critique
  `critique:ticket-route-field-ownership-review` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
