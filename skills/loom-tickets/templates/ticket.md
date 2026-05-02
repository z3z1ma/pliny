---
id: ticket:<token>
kind: ticket
status: proposed
change_class: <record-hygiene|documentation-explanation|behavior-contract|code-behavior|protocol-authority|data-migration|security-sensitive|release-packaging>
risk_class: <low|medium|high>
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
external_refs: {}
depends_on: []
---

# Summary

What this bounded work item is.

# Context

Relevant upstream context and why this exists.

# Why Now

Why this deserves attention in the current phase.

# Scope

What belongs inside this ticket.

# Out Of Scope

What should not happen inside this ticket.

# Acceptance Criteria

What must be true for this ticket to be accepted.

If a spec owns the acceptance contract, summarize only the ticket-scoped work
here and cite the spec-owned acceptance IDs under `# Coverage`.

If no spec owns the acceptance contract, this ticket may own ticket-local
acceptance criteria. Write stable local IDs so evidence and critique can cite
them, for example:

- ACC-001: The bounded change produces the intended observable result.
- ACC-002: Required evidence is linked before acceptance review.

# Coverage

Covers:

List qualified claim or acceptance IDs. If none apply, write `None - reason`.

- Use `spec:<slug>#ACC-001` for spec-owned acceptance.
- Use `ticket:<token>#ACC-001` for ticket-local acceptance criteria owned in
  this ticket.
- Use `initiative:<slug>#OBJ-001` for initiative objectives this ticket advances.

# Claim Matrix

Use only real claim, evidence, and critique references. Remove this table or
write `None - reason` when no claim matrix applies yet.

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |

# Execution Notes

Useful implementation notes, but not a transcript dump.

# Blockers

Named blockers only. If none exist, write `None`.

# Next Move / Next Route

The next governed route token, using `skills/loom-records/references/route-vocabulary.md`:
`ask_user`, `workspace_status`, `records_repair`, `research`, `spec`, `plan`,
`ticket`, `local_edit`, `ralph`, `evidence`, `critique`, `wiki`,
`retrospective`, `acceptance_review`, `continue`, or `stop`.

# Route Readiness

Name the next governed route and the information needed for that route. Use only
the route sections that apply; remove or mark unrelated sections `N/A`.

Route: ask_user | workspace_status | records_repair | research | spec | plan |
ticket | local_edit | ralph | evidence | critique | wiki | retrospective |
acceptance_review | continue | stop

Local edit readiness:
Bounded edit:
Write boundary:

Ralph readiness, required only when the next route is `ralph`:

Bounded iteration:
Write boundary:
Likely verification posture:
Expected output contract:

Critique readiness:
Review target:
Required profiles:
Evidence to review:

Wiki / retrospective / promotion readiness:
Explanation or lesson to promote:
Owner records to source:

Evidence readiness:
Claims to support or challenge:
Observation procedure:

Acceptance review readiness:
Evidence and critique disposition:
Residual risks:

# Evidence

What evidence exists or is expected.

# Critique Disposition

Risk class: low | medium | high

Must match frontmatter `risk_class`. The frontmatter field is the ticket's
canonical risk classification; this section restates that risk only to explain
the critique policy and acceptance disposition. If the two differ, reconcile the
ticket before readiness, critique routing, or closure.

Critique policy: optional | recommended | mandatory

Policy rationale:

Required critique profiles:

List profile names, or write `None - reason`.

Findings:

List real finding references and ticket-owned finding dispositions, or write
`None - no critique yet`.

Example:

- `critique:example-review#FIND-001` — `resolved` by <evidence or change ref>
- `critique:example-review#FIND-002` — `accepted_risk`; rationale and acceptance
  provenance recorded in `# Acceptance Decision`
- `critique:example-review#FIND-003` — `superseded` by <evidence ref>
- `critique:example-review#FIND-004` — `converted_to_follow_up` as
  `ticket:<token>`

Open medium/high findings must have ticket-owned dispositions of `resolved`,
`accepted_risk`, `superseded`, or `converted_to_follow_up` before closure, with
evidence, acceptance provenance, or linked follow-up tickets as appropriate.
Withdrawn findings require critique rationale and may be cited for audit history
without ticket-owned finding disposition.

Disposition status: pending | blocking | completed | deferred | not_required

Use `blocking` only when unresolved required critique currently blocks acceptance
or dependent continuation. This status is a ticket-owned gate summary, not a
critique verdict.

Deferral / not-required rationale:

# Retrospective / Promotion Disposition

Ticket-owned closure summary for durable learning and follow-through across all
promotion routes. This section does not create a retrospective record kind or
make retrospective replace acceptance; it tells acceptance review whether
compounding work is resolved for this ticket.

Disposition status: pending | blocking | completed | deferred | not_required

- Use `pending` while implementation, critique, or acceptance review has not yet
  determined the retrospective need.
- Use `blocking` when closure would be unsafe because required promotion or
  prevention follow-through is incomplete.
- Use `completed` when durable lessons were promoted into their existing owner
  layers, or the retrospective pass completed and found no open follow-through.
- Use `deferred` when promotion or prevention is intentionally moved to linked
  follow-up work before closure.
- Use `not_required` when the ticket has no durable lesson to promote.

Promoted:

List owner-record updates, or write `None - reason`.

Deferred / not-required rationale:

# Wiki Disposition

Route-specific wiki outcome when accepted explanation is one of the promotion
routes. Write `N/A - no wiki promotion route` when the broader retrospective /
promotion disposition routes learning elsewhere or finds no durable wiki-worthy
explanation.

# Acceptance Decision

Required when the workspace, team, accepted risk, or operator asks for explicit
acceptance provenance.

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

Human-readable notes for important dependencies beyond `depends_on`.

# Journal

Chronological updates that matter later.
