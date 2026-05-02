# Acceptance Gate

Acceptance is the fail-closed decision for ticket closure.

`closed` means the durable story is coherent. It is not a synonym for finished
implementation.

## Inputs

- ticket
- change class and risk class
- linked spec acceptance IDs and ticket-local acceptance IDs in scope
- ticket claim matrix when present
- evidence
- critique records and ticket-owned finding dispositions
- critique policy: `optional`, `recommended`, or `mandatory`, plus rationale and
  ticket-owned disposition status `pending`, `blocking`, `completed`, `deferred`,
  or `not_required`
- retrospective / promotion disposition: ticket-owned status `pending`,
  `blocking`, `completed`, `deferred`, or `not_required`, plus promoted owner
  records or rationale
- wiki disposition when wiki is one of the promotion routes
- recent Ralph packet outcomes
- relevant plan or initiative context

Ticket frontmatter `risk_class` is the canonical ticket risk. The risk class in
`# Critique Disposition` restates that same value for critique routing and must
not become a second, contradictory risk claim.

New tickets and tickets being materially updated for readiness, Ralph, critique,
acceptance, reopening, or closure must declare `change_class` and `risk_class`.
Legacy tickets without those fields are normalized when touched or before they
are used for governed execution or acceptance; they are not declared broken
merely by existing.

## Acceptance Dossier

The acceptance dossier is the composed ticket-owned view used for closure.
It is not a new record kind.

```text
Acceptance Dossier =
  Acceptance Criteria
  + Coverage
  + Claim Matrix
  + Evidence
  + Critique Policy
  + Critique Disposition
  + Retrospective / Promotion Disposition
  + Wiki Disposition when applicable
  + Journal
  + Acceptance Decision when required
```

## Closure Questions

- Are acceptance criteria met?
- Does implementation reality match intended behavior, or is the gap explicitly
  recorded?
- Does evidence support each covered claim reference?
- If acceptance is ticket-local, are `ACC-*` references qualified outside the
  ticket as `ticket:<token>#ACC-001`?
- Is the evidence fresh enough for the current source, record, dependency, and
  environment state, or are its limits explicit?
- Does the claim matrix accurately summarize support, challenge, and open
  claims?
- Is critique policy explicit enough for this change class and risk class?
- When critique policy requires profiles, are those profiles complete?
- If critique is mandatory, does required critique exist and do all open
  medium/high findings have ticket-owned dispositions of `resolved`,
  `accepted_risk`, `superseded`, or `converted_to_follow_up`?
- If critique is recommended but not performed, does the ticket record why it
  was deferred or intentionally not needed before closure?
- For any existing critique, do open medium and high severity findings have
  ticket-owned dispositions of `resolved`, `accepted_risk`, `superseded`, or
  `converted_to_follow_up`?
- For withdrawn findings, does the critique record provide withdrawal rationale,
  with any ticket citation limited to audit history rather than closure blocking?
- Are finding references qualified, for example `critique:example-review#FIND-001`?
- Is retrospective / promotion disposition resolved for closure as `completed`,
  `deferred`, or `not_required`, or does it remain `blocking` because required
  promotion or prevention follow-through is incomplete?
- If wiki is one promotion route, does `# Wiki Disposition` record the
  route-specific outcome without replacing the broader promotion decision?
- If human signoff or accepted-risk provenance is required, does
  `# Acceptance Decision` name who accepted, when, on what basis, and with what
  residual risks?
- Are links and status fields coherent?

## Ticket-Owned Finding Disposition

Tickets consume critique findings; critique records do not close tickets. For
each finding reference, use a qualified reference such as
`critique:example-review#FIND-001` and record one ticket-owned disposition:

- `resolved` — the finding was addressed by a specific change or evidence ref.
- `accepted_risk` — the risk remains but is intentionally accepted; record the
  rationale and acceptance provenance in `# Acceptance Decision`.
- `superseded` — newer evidence invalidates or replaces the finding; cite that
  evidence.
- `converted_to_follow_up` — the finding is real but outside this ticket's
  closure scope; link the follow-up ticket that now owns the remaining work.

Open medium/high findings are not closure-compatible while missing ticket-owned
disposition, evidence, acceptance provenance, or linked follow-up tickets as
appropriate.

Withdrawn findings are closure-compatible when the critique record retracts them
with rationale. They do not require a ticket-owned finding disposition, though the
ticket may cite them for audit history.

Do not put these values in a critique record as if critique accepted its own
findings. Critique owns finding state and verdict; the ticket owns how each
finding affects closure. See `skills/loom-records/references/status-lifecycle.md`
for the shared boundary vocabulary.

## Outcomes

- `closed`: durable story is complete and coherent
- `complete_pending_acceptance`: work is substantially done but an acceptance
  step remains
- `review_required`: critique is still the next governed move
- `active`: implementation is still underway
- `blocked`: a named blocker prevents progress

## Guardrails

- Fail closed.
- Do not close because the code feels done.
- Do not close over unresolved required critique.
- Do not close over missing mandatory critique.
- Do not close over missing evidence for covered claims or acceptance criteria.
- Do not close over `pending` or `blocking` retrospective / promotion
  disposition.
- Do not close over open medium/high critique findings unless the ticket records
  `resolved`, `accepted_risk`, `superseded`, or `converted_to_follow_up` with the
  needed evidence, acceptance provenance, or linked follow-up ticket.
- Do not close over recommended critique without a ticket-owned disposition.
- Do not let acceptance live only in chat.
- Create follow-up tickets for substantial residual work.

## Acceptance Provenance

For regulated work, accepted risk, or explicit human gates, record:

```md
# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:
```

Leave fields blank only while the ticket is not yet accepted.

## Native Queries

```bash
rg -n '^(id|status|depends_on):' .loom/tickets --glob '*.md'
rg -n '<ticket-id>|<target>' .loom/{critique,wiki,evidence,specs,research,plans,packets} --glob '*.md'
git status --short
git diff --stat
```
