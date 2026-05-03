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
next owner: constitution | initiative | research | spec | plan | ticket | evidence | critique | wiki
operator decision: <decision needed, unsafe-inference reason, and owner record to update; only when candidate route is ask_user>
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
- `stop` or `ask_user` conditions for the tranche

Prefer one to three tickets for a normal tranche. More is allowed only when the
plan proves the tickets are independent and the parent can still reconcile the
combined result honestly. If there is already one bounded ready ticket and no
sequencing ambiguity, do not manufacture a gap summary or tranche detail.

## Route Decision Priority

Choose the next route in this order. The first true condition wins unless the
ticket or operator explicitly records a different rationale.

| Condition | Next route |
| --- | --- |
| Product direction, autonomy, risk, budget, or success meaning is materially unclear | `ask_user` |
| The workspace is untrustworthy | `workspace_status` |
| The owner chain has broken, stale, or contradictory records | `records_repair` |
| Project identity, principles, hard constraints, roadmap direction, or citable decisions must change | `constitution` |
| Strategic outcome framing, objective criteria, success metrics, or delegated autonomy boundaries must change | `initiative` |
| Evidence is missing for a decision or option | `research` |
| Intended behavior or acceptance is ambiguous | `spec` |
| Sequencing, dependency order, or tranche boundary is ambiguous | `plan` |
| No bounded live execution owner exists for the next mutation | `ticket` |
| A failing behavior or incident needs reproduce-first diagnosis before a normal fix route is safe | `debugging` |
| A bounded experiment, prototype, or sketch should inform commitment | `spike` |
| Repository or module structure must be mapped before downstream work can proceed safely | `codemap` |
| A ticket is ready and work is tiny, local, and safe | `local_edit` |
| A ticket is Ralph-ready for one bounded implementation iteration that needs a fresh child packet or explicit write boundary | `ralph` |
| Observed support or challenge needs durable preservation | `evidence` |
| Risk, protocol authority, code behavior, or acceptance sufficiency needs review | `critique` |
| Accepted reusable explanation, architecture explanation, or workflow concept should persist for future agents | `wiki` |
| Accepted learning should compound or promote across owner layers before closure | `retrospective` |
| Ticket-owned closure readiness needs evaluation | `acceptance_review` |
| Already-truthful work needs merge, release, PR, or handoff packaging | `ship` |
| A route result has been reconciled into owner records, and those records already name the next governed tranche or route | `continue`, as a route token only; not a Ralph child outcome |
| Objective criteria are satisfied and no owner work remains | `stop`, with a recorded stop reason or condition |

This table prevents implementation from becoming the default answer. Shaping and
review routes are first-class continuation outcomes. Do not use `continue` as a
fallback when owner truth is missing; reconcile owner records first, then follow
the route they already name.

## Route Entry And Result Criteria

- `ask_user` enters when a material decision cannot be safely inferred from owner
  records, delegated authority, or a low-risk reversible assumption. It exits with
  either an operator answer plus the owner record to update, or a recorded blocker,
  stop condition, or unsafe-inference reason.
- `workspace_status` enters when workspace trust, structure, harness posture,
  support metadata, or entry state is uncertain. It exits with repaired workspace
  support metadata, a narrower downstream route, or a named blocker.
- `records_repair` enters when the graph has broken links, stale owners,
  contradictory status, placeholder leakage, invalid record shape, or other graph
  drift. It exits with repaired owner records or a blocker that prevents dependent
  work.
- `constitution` enters with missing or changed project identity, principle,
  constraint, roadmap, or decision truth and exits with constitutional truth
  updated or explicitly deferred.
- `initiative` enters with strategic outcome, objective, success-metric, or
  delegated-autonomy truth to create or refine and exits with the initiative
  updated or explicitly deferred.
- `research` enters with a question and exits with evidence-backed conclusions or
  explicit uncertainty.
- `spec` enters with ambiguous intended behavior and exits with acceptance criteria.
- `plan` enters with sequencing ambiguity and exits with tranche/ticket strategy.
- `ticket` enters with bounded live work and exits only through ticket-owned state.
- `local_edit` enters with a ready ticket whose mutation is tiny, local, and safe
  without a fresh child packet. It exits with source or record changes, evidence
  as needed, and ticket reconciliation.
- `ralph` enters with one Ralph-ready bounded implementation ticket and exits with
  parent reconciliation.
- `debugging` enters with failing behavior or incident evidence needs and exits with
  reproduction/root-cause/fix/prevention routing through existing owner layers.
- `spike` enters with a bounded experiment, prototype, or sketch question and exits
  with evidence, research conclusions or null results, and a downstream route.
- `codemap` enters with repository/module orientation need and exits with scan
  evidence, research when uncertain, or accepted wiki atlas updates.
- `evidence` enters with an observation and exits with support/challenge links.
- `critique` enters with a review target and exits with findings, verdict, and
  required follow-up.
- `wiki` or `retrospective` enters with accepted learning and exits with durable
  explanation or promotion decisions.
- `acceptance_review` enters with a ticket-owned acceptance dossier and exits with
  accepted, blocked, follow-up, stop, or ship routing recorded on the ticket.
- `ship` enters with truthful ticket/evidence/critique/retrospective or promotion
  disposition and exits with external handoff packaging plus the next
  ticket-owned route.
- `continue` enters only when existing owner records already authorize the next
  narrower route or tranche. It exits by following that owner-named route without
  inventing new truth.
- `stop` enters when objective work should pause or end. It exits with a stop
  reason, owner record, remaining blockers or external triggers, and no closure
  claim unless ticket-owned acceptance already supports closure.

Every route result must name the owner records that changed and the next route.
If the next route is `stop`, record the stop reason or condition.

Use `skills/loom-records/references/route-vocabulary.md` for route-token grammar.

## Reconciliation Targets

After each route, reconcile before continuing:

- constitution result -> constitution record, then initiative/plan/ticket if it
  changes downstream work
- initiative result -> initiative record, then plan/ticket if it changes objective
  execution
- research result -> research record, then spec/plan/ticket if it changes next
  work
- spec change -> spec record and ticket coverage
- plan change -> plan strategy/execution waves and ticket queue
- ticket work -> ticket journal, coverage, evidence/critique disposition, next
  route
- ask_user -> operator answer or blocker recorded in the owner record that needed
  the decision
- workspace_status -> `.loom/workspace.md`, `.loom/harness.md`, or workspace
  support repair notes, then downstream route
- records_repair -> repaired owner records, links, statuses, IDs, placeholders, or
  blocker
- local_edit -> ticket journal, changed paths, evidence if the ticket relies on
  observed behavior, and critique when risk warrants
- Ralph child output -> packet status, ticket truth, evidence/critique as needed
- debugging result -> evidence/research/spec/ticket/local_edit/Ralph/retrospective
  owners as appropriate, plus ticket next route when live work is involved
- spike result -> research conclusions/null results, evidence artifacts, and any
  downstream spec/plan/ticket/wiki route
- codemap result -> evidence scans, research uncertainty when needed, and accepted
  wiki atlas/page updates
- evidence -> evidence record and ticket claim matrix
- critique -> critique record and ticket critique disposition
- wiki/retrospective -> wiki/research/spec/plan/initiative/constitution/evidence
  as owner truth requires, plus support-only memory cleanup or owner-record
  pointers when useful, and ticket disposition
- acceptance_review -> ticket acceptance decision, evidence disposition, critique
  disposition, residual risk, and next route
- ship result -> external handoff package plus ticket-owned acceptance or
  follow-up route; shipping does not close the ticket
- continue -> no new owner truth by itself; follow the owner-named route or
  tranche
- stop -> ticket, initiative, or drive anchor stop reason, resume condition, and
  any unresolved blocker or external action

If the parent cannot name reconciliation targets, the route is not ready.
