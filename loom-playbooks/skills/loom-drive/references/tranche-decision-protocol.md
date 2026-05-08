# Tranche Decision Protocol

This reference supports the `loom-drive` skill.

The drive loop needs a bridge between objective state and execution. Most drives
only need a clear owner chain and one bounded ticket. Use this fuller protocol
only when objective gaps, review state, dependency order, or write-scope conflict
make the next bounded tranche unsafe to infer from the existing records.

## Optional Objective Gap Summary

When objective gaps are not already obvious from the initiative, plan, or ticket
chain, write or update a compact gap summary in the owner layer that owns the fact
being stated.

```text
claim: <OBJ-001 | ACC-001 | ticket-local criterion>
state: open | partially_satisfied | satisfied | blocked | out_of_scope
current support: <evidence / critique / ticket links>
gap type: evidence | behavior | implementation | review | explanation | planning | decision
owner that can resolve the gap: <constitution | initiative | research | spec | plan | ticket | evidence | critique | wiki>
operator decision: <decision needed, unsafe-inference reason, and owner record to update; only when human input is required>
notes: <why this gap matters now>
```

The summary does not create a new layer. It is a reasoning shape inside the owner
records that already own objective status, plan strategy, and ticket coverage. If
`accepted_risk` appears in a gap summary, cite the ticket-owned acceptance
decision or ticket-owned finding disposition that accepted the risk; the summary
itself does not accept risk.

## Optional Tranche Detail

Use this fuller tranche detail only when dependencies, write-scope conflicts,
claim coverage, or critique/evidence gates need more than a single ready ticket.
When needed, the parent should state:

- objective or acceptance claims included in this tranche
- claims explicitly excluded until a later tranche
- ticket count and why each ticket is independently legible
- dependency order and whether any tickets can run in parallel
- likely child write scopes and conflict check
- evidence expected from each ticket or child packet
- critique policy and required profiles
- reassessment point after the tranche
- stop conditions or human-decision triggers for the tranche

Prefer one to three tickets for a normal tranche. More is allowed only when the
plan proves the tickets are independent and the parent can still reconcile the
combined result honestly. If there is already one bounded ready ticket and no
sequencing ambiguity, do not manufacture a gap summary or tranche detail.

## Decision Priority

Choose the next action by the first missing truth or safety constraint that
matters:

| If this is true... | Then... |
| --- | --- |
| Product direction, autonomy, risk, budget, or success meaning is materially unclear | ask the user and record the decision needed in the owner record that will change |
| Workspace structure or owner-chain trust is unclear | inspect or repair workspace support before downstream work |
| Owner records are broken, stale, contradictory, or placeholder-contaminated | repair the graph before dependent work |
| Project identity, principle, hard constraint, roadmap, or citable decision must change | update constitution truth |
| Strategic outcome framing, success metrics, or delegated autonomy boundaries must change | update initiative truth |
| Evidence is missing for a decision or option | update research or evidence, depending on whether synthesis or observation is missing |
| Intended behavior or acceptance is ambiguous | update spec truth before implementation |
| High-level execution shape, sequencing, dependency order, or tranche boundary is ambiguous | update plan truth |
| No bounded live execution owner exists for the next mutation | create or refine a ticket |
| A failing behavior or incident needs reproduce-first diagnosis | use debugging before a normal fix |
| A bounded experiment, prototype, or sketch should inform commitment | run a spike and preserve evidence/research output |
| Repository or module structure must be mapped before downstream work can proceed safely | run codemap and preserve evidence/research/wiki output |
| A ticket is ready and work is tiny, local, and safe | use local execution and reconcile the ticket |
| A ticket needs fresh-context implementation with explicit write scope | compile a Ralph packet |
| Observed support or challenge needs durable preservation | create evidence |
| Risk, protocol authority, code behavior, or acceptance sufficiency needs review | run critique |
| Accepted reusable explanation should persist | update wiki |
| Accepted learning should compound before closure | run retrospective over the relevant owner layers |
| Ticket closure readiness needs evaluation | update the ticket acceptance decision |
| Already-truthful work needs merge, release, PR, or handoff packaging | use ship without treating packaging as closure |
| Objective criteria are satisfied and no owner work remains | close or complete the owning tickets/initiative truthfully |

This table is a reasoning aid, not a token list to copy into records. Do not add a
saved workflow field to record the result.

## Reconciliation Targets

After each action, reconcile before continuing:

- constitution change -> constitution record, then initiative/plan/ticket if it
  changes downstream work
- initiative change -> initiative record, then plan/ticket if it changes objective
  execution
- research result -> research record, then spec/plan/ticket if it changes work
- spec change -> spec record and ticket coverage
- plan change -> plan strategy/execution waves and ticket queue
- ticket work -> ticket journal, coverage, evidence/critique disposition,
  blockers, status, and acceptance dossier
- user answer -> the owner record that needed the decision
- workspace repair -> `.loom/workspace.md`, `.loom/harness.md`, or workspace
  support notes when useful, then read the owner chain again
- graph repair -> repaired owner records, links, statuses, IDs, placeholders, or
  blocker notes
- local execution -> ticket journal, changed paths, evidence if the ticket relies on
  observed behavior, and critique when risk warrants
- Ralph child output -> packet status, ticket truth, evidence/critique as needed
- debugging result -> evidence/research/spec/ticket/local execution/Ralph/retrospective
  owners as appropriate
- spike result -> research conclusions/null results, evidence artifacts, and any
  downstream spec/plan/ticket/wiki owner updates
- codemap result -> evidence scans, research uncertainty when needed, and accepted
  wiki atlas/page updates
- evidence -> evidence record and ticket coverage or acceptance view; use a claim
  matrix only when coverage is complex enough to need one
- critique -> critique record and ticket critique disposition
- wiki/retrospective -> wiki/research/spec/plan/initiative/constitution/evidence
  as owner truth requires, plus support-only memory cleanup or owner-record
  pointers when useful, and ticket disposition
- acceptance review -> ticket acceptance decision, evidence disposition, critique
  disposition, residual risk, and status
- ship -> external handoff package plus any ticket-owned acceptance or follow-up
  update; shipping does not close the ticket

If the parent cannot name reconciliation targets, the work is not ready.
