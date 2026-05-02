---
id: ticket:critrec9
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T23:38:57Z
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
    - packet:ralph-ticket-critrec9-20260502T232902Z
  evidence:
    - evidence:critique-recommendation-vocabulary-validation
  critique:
    - critique:critique-recommendation-vocabulary-review
external_refs: {}
depends_on:
  - ticket:critgate2
---

# Summary

Normalize critique recommendation vocabulary so it cannot be mistaken for ticket
states or route tokens.

# Context

Council finding `NC-009` found critique recommendation prose such as
`close-ready` that can blur critique recommendations with canonical ticket state.

# Why Now

Critique should recommend acceptance posture without mutating ticket truth or
teaching non-canonical status values.

# Scope

- Update critique template/references to separate recommendation prose from ticket
  lifecycle states and route tokens.
- Preserve critique ownership of findings/verdicts and ticket ownership of closure.
- Align with route vocabulary where route values are named.

# Out Of Scope

- Do not remove acceptance recommendations from critique.
- Do not give critique records closure authority.

# Acceptance Criteria

- ACC-001: Critique recommendation vocabulary is clearly non-canonical unless it
  names an existing ticket state or route token explicitly.
- ACC-002: Critique guidance says recommendations do not mutate ticket state.
- ACC-003: Ticket and critique ownership boundaries remain clear.
- ACC-004: Evidence records recommendation/status vocabulary searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-009`
- `ticket:critrec9#ACC-001`
- `ticket:critrec9#ACC-002`
- `ticket:critrec9#ACC-003`
- `ticket:critrec9#ACC-004`
- `ticket:critrec9#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-009` | `evidence:critique-recommendation-vocabulary-validation` | `critique:critique-recommendation-vocabulary-review` | supported |
| `ticket:critrec9#ACC-001` | `evidence:critique-recommendation-vocabulary-validation` | `critique:critique-recommendation-vocabulary-review` | supported |
| `ticket:critrec9#ACC-002` | `evidence:critique-recommendation-vocabulary-validation` | `critique:critique-recommendation-vocabulary-review` | supported |
| `ticket:critrec9#ACC-003` | `evidence:critique-recommendation-vocabulary-validation` | `critique:critique-recommendation-vocabulary-review` | supported |
| `ticket:critrec9#ACC-004` | `evidence:critique-recommendation-vocabulary-validation` | `critique:critique-recommendation-vocabulary-review` | supported |
| `ticket:critrec9#ACC-005` | `critique:critique-recommendation-vocabulary-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-critique/templates/critique.md` and
related critique finding/recommendation references.

# Blockers

None - dependency `ticket:critgate2` is closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:routewf10`.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:critique-recommendation-vocabulary-validation` and oracle
critique `critique:critique-recommendation-vocabulary-review` support closure
with no findings.

# Evidence

Expected: before/after searches for `close-ready`, recommendation/status wording,
route tokens in critique guidance, and `git diff --check`.

Recorded: `evidence:critique-recommendation-vocabulary-validation` captures the
before/after vocabulary searches and `git diff --check` for this Ralph
iteration.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: critique/ticket boundary ambiguity can corrupt acceptance state.

Required critique profiles:

- owner-boundary
- records-grammar
- closure-honesty

Findings:

`critique:critique-recommendation-vocabulary-review` - no findings; mandatory
oracle critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Critique recommendation vocabulary and ownership boundaries were promoted
  directly into `skills/loom-critique/templates/critique.md` and
  `skills/loom-critique/references/finding-format.md`.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched critique template/reference guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T23:38:57Z
Basis: Ralph packet `packet:ralph-ticket-critrec9-20260502T232902Z`; evidence
`evidence:critique-recommendation-vocabulary-validation`; oracle critique
`critique:critique-recommendation-vocabulary-review` with no findings.
Residual risks: validation is structural/manual. Historical `.loom/critique`
records may still contain old recommendation prose, but they are outside this
ticket's product-surface target.

# Dependencies

- `ticket:critgate2`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-009`.
- 2026-05-02T23:29:02Z: Confirmed dependency `ticket:critgate2` is closed,
  compiled Ralph packet `packet:ralph-ticket-critrec9-20260502T232902Z`, and
  moved ticket to `active`.
- 2026-05-02T23:30:27Z: Ralph iteration normalized critique acceptance
  recommendation labels, recorded validation evidence, and moved ticket to
  `review_required` for mandatory oracle critique.
- 2026-05-02T23:34:35Z: Parent reconciled Ralph packet
  `packet:ralph-ticket-critrec9-20260502T232902Z`, normalized claim matrix
  statuses to canonical claim-coverage vocabulary, and kept next route as
  mandatory critique.
- 2026-05-02T23:35:41Z: Parent expanded `# Coverage` with ticket-local
  acceptance IDs for traceability before oracle critique.
- 2026-05-02T23:38:57Z: Mandatory oracle critique
  `critique:critique-recommendation-vocabulary-review` passed with no findings.
  Parent recorded retrospective / promotion disposition and accepted closure.
