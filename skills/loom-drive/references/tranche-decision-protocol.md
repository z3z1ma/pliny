# Tranche Decision Protocol

This reference supports the `loom-drive` skill.

The drive loop needs a bridge between objective state and execution. Most drives
only need a clear checkpoint and next route. Use this fuller protocol when
objective gaps, review state, or sequencing ambiguity make the next bounded
tranche unsafe to choose from the current ticket chain alone.

## Optional Objective Gap Summary

When objective gaps are not already obvious from the initiative, plan, or ticket
chain, write or update a compact gap summary in the owner layer that owns the
fact being stated.

```text
claim: <OBJ-001 | ACC-001 | ticket-local criterion>
state: open | partial | supported | challenged | blocked | accepted_risk | satisfied
current support: <evidence / critique / ticket links>
gap type: evidence | behavior | implementation | review | explanation | sequencing | decision
next owner: research | spec | plan | ticket | evidence | critique | wiki | user
candidate route: <route>
notes: <why this gap matters now>
```

The summary does not create a new layer. It is a reasoning shape inside the owner
records that already own objective status, plan strategy, and ticket coverage.
If `accepted_risk` appears in a gap summary, cite the ticket-owned acceptance
decision or critique disposition that accepted the risk; the summary itself does
not accept risk.

## Optional Tranche Detail

Use this fuller tranche detail only when dependencies, write-scope conflicts,
claim coverage, or critique/evidence gates need more than a single ready ticket
or next-route sentence. When needed, the parent should state:

- objective or acceptance claims included in this tranche
- claims explicitly excluded until a later tranche
- ticket count and why each ticket is independently legible
- dependency order and whether any tickets can run in parallel
- likely child write scopes and conflict check
- evidence expected from each ticket or child route
- critique policy and required profiles
- reassessment point after the tranche
- stop or ask-user conditions for the tranche

Prefer one to three tickets for a normal tranche. More is allowed only when the
plan proves the tickets are independent and the parent can still reconcile the
combined result honestly. If there is already one bounded ready ticket and no
sequencing ambiguity, do not manufacture a gap summary or tranche detail.

## Route Decision Priority

Choose the next route in this order. The first true condition wins unless the
ticket or operator explicitly records a different rationale.

| Condition | Next route |
| --- | --- |
| Product direction, autonomy, risk, budget, or success meaning is materially unclear | ask user |
| The workspace or owner chain is untrustworthy | workspace/records repair |
| Evidence is missing for a decision or option | research |
| Intended behavior or acceptance is ambiguous | spec |
| Sequencing, dependency order, or tranche boundary is ambiguous | plan |
| No bounded live execution owner exists for the next mutation | ticket |
| A ticket is ready and work is tiny, local, and safe | local edit |
| A ticket is Ralph-ready or needs fresh bounded context | Ralph |
| Observed support or challenge needs durable preservation | evidence |
| Risk, protocol authority, code behavior, or acceptance sufficiency needs review | critique |
| Accepted explanation should persist for future agents | wiki or retrospective |
| Objective criteria are satisfied and required evidence/critique/wiki disposition is complete | acceptance / stop |

This table prevents implementation from becoming the default answer. Shaping and
review routes are first-class continuation outcomes.

## Route Entry And Result Criteria

- Research enters with a question and exits with evidence-backed conclusions or
  explicit uncertainty.
- Spec enters with ambiguous intended behavior and exits with acceptance criteria.
- Plan enters with sequencing ambiguity and exits with tranche/ticket strategy.
- Ticket enters with bounded live work and exits only through ticket-owned state.
- Ralph enters with one Ralph-ready ticket and exits with parent reconciliation.
- Evidence enters with an observation and exits with support/challenge links.
- Critique enters with a review target and exits with findings, verdict, and
  required follow-up.
- Wiki or retrospective enters with accepted learning and exits with durable
  explanation or promotion decisions.

Every route result must name the owner records that changed and the next route or
stop condition.

## Reconciliation Targets

After each route, reconcile before continuing:

- research result -> research record, then spec/plan/ticket if it changes next
  work
- spec change -> spec record and ticket coverage
- plan change -> plan strategy/execution waves and ticket queue
- ticket work -> ticket journal, coverage, evidence/critique disposition, next
  route
- Ralph child output -> packet status, ticket truth, evidence/critique as needed
- evidence -> evidence record and ticket claim matrix
- critique -> critique record and ticket critique disposition
- wiki/retrospective -> wiki/research/spec/plan/initiative/constitution/memory as
  appropriate, plus ticket disposition

If the parent cannot name reconciliation targets, the route is not ready.
