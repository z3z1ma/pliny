---
id: ticket:critgate2
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T22:31:08Z
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
    - packet:ralph-ticket-critgate2-20260502T221504Z
  evidence:
    - evidence:critique-closure-gate-validation
  critique:
    - critique:critique-closure-gate-review
    - critique:critique-closure-gate-rereview
external_refs: {}
depends_on: []
---

# Summary

Tighten bootstrap closure wording so mandatory critique cannot be read as
deferrable before closure.

# Context

Council finding `NC-002` found wording in bootstrap validation/critique doctrine
that says required critique has happened or is explicitly deferred, which can
blur mandatory and recommended critique policies.

# Why Now

Closure discipline should fail closed for mandatory critique while still allowing
ticket-owned rationale for recommended critique disposition.

# Scope

- Update bootstrap validation and critique/wiki references to distinguish
  mandatory critique from recommended critique.
- Preserve ticket-owned acceptance and critique finding disposition boundaries.
- Keep recommended critique disposition flexible where policy allows it.

# Out Of Scope

- Do not make optional critique mandatory.
- Do not move closure authority out of tickets.

# Acceptance Criteria

- ACC-001: Mandatory critique clearly blocks closure until completed and required
  findings are dispositioned.
- ACC-002: Recommended critique can be completed, deferred, or not required only
  with ticket-owned rationale.
- ACC-003: Bootstrap validation and critique/wiki wording are consistent.
- ACC-004: Evidence records critique-gate wording searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-002`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-002` | `evidence:critique-closure-gate-validation` | `critique:critique-closure-gate-review#FIND-001` resolved; `critique:critique-closure-gate-rereview` passed | supported |
| `ticket:critgate2#ACC-001` | `evidence:critique-closure-gate-validation` | `critique:critique-closure-gate-review#FIND-001` resolved; `critique:critique-closure-gate-rereview` passed | supported |
| `ticket:critgate2#ACC-002` | `evidence:critique-closure-gate-validation` | `critique:critique-closure-gate-rereview` passed | supported |
| `ticket:critgate2#ACC-003` | `evidence:critique-closure-gate-validation` | `critique:critique-closure-gate-review#FIND-001` resolved; `critique:critique-closure-gate-rereview` passed | supported |
| `ticket:critgate2#ACC-004` | `evidence:critique-closure-gate-validation` | `critique:critique-closure-gate-rereview` passed | supported |
| `ticket:critgate2#ACC-005` | `critique:critique-closure-gate-rereview` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-bootstrap/references/07-validation-and-honesty.md`
and `skills/loom-bootstrap/references/05-critique-and-wiki.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:drvgram3`.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence `evidence:critique-closure-gate-validation` and oracle critique
`critique:critique-closure-gate-rereview` support closure. Prior finding
`critique:critique-closure-gate-review#FIND-001` is ticket-dispositioned as
resolved by the final-review wording repair.

# Evidence

Observed in `evidence:critique-closure-gate-validation`:

- before/after searches for required, mandatory, recommended, explicitly
  deferred, `not_required`, and closure-blocking wording
- `git diff --check`
- repair validation after `critique:critique-closure-gate-review#FIND-001`

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: closure-gate ambiguity can weaken fail-closed acceptance.

Required critique profiles:

- closure-honesty
- operator-clarity
- routing-safety

Findings:

- `critique:critique-closure-gate-review#FIND-001` (medium, open): resolved by
  replacing draft/stub-permissive `required review exists` wording with a final
  critique review and explicit verdict requirement in bootstrap doctrine.
- `critique:critique-closure-gate-rereview` - no findings; mandatory oracle
  critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Mandatory critique closure-gate precision, including the `final` critique record
  requirement, was promoted directly into
  `skills/loom-bootstrap/references/05-critique-and-wiki.md` and
  `skills/loom-bootstrap/references/07-validation-and-honesty.md`.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the bootstrap doctrine wording itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched bootstrap guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T22:31:08Z
Basis: Ralph packet `packet:ralph-ticket-critgate2-20260502T221504Z`; evidence
`evidence:critique-closure-gate-validation`; oracle critique
`critique:critique-closure-gate-review#FIND-001` resolved by repair; oracle
re-review `critique:critique-closure-gate-rereview` passed with no findings.
Residual risks: validation is structural. A non-target ticket acceptance-gate
reference still has shorter critique-gate wording, but bootstrap doctrine now
owns the clarified closure policy for this ticket's scope.

# Dependencies

Plan sequence follows `ticket:pktsupp1`.

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-002`.
- 2026-05-02T22:15:03Z: Compiled Ralph packet
  `packet:ralph-ticket-critgate2-20260502T221504Z` and moved ticket to `active`.
- 2026-05-02T22:16:05Z: Ralph child updated bootstrap critique closure wording,
  recorded `evidence:critique-closure-gate-validation`, and moved ticket to
  `review_required` for mandatory oracle critique.
- 2026-05-02T22:21:29Z: Parent reconciled Ralph output, normalized claim matrix
  statuses to canonical claim-coverage vocabulary, expanded evidence sections,
  and marked the Ralph packet consumed.
- 2026-05-02T22:26:16Z: Mandatory oracle critique recorded
  `critique:critique-closure-gate-review#FIND-001`; parent repaired bootstrap
  wording to require a final critique review with explicit verdict before closure.
- 2026-05-02T22:31:08Z: Oracle re-review
  `critique:critique-closure-gate-rereview` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
