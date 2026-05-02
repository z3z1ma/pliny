# Checkpoint And Resume Protocol

This reference supports the `loom-drive` skill.

Each new session must be able to recover drive state from Loom records.
Checkpointing is therefore mandatory drive hygiene, not a nice-to-have summary.

## Anchor Rule

Every active drive has one anchor record:

- high-level objective -> initiative anchor
- plan-only continuation -> plan anchor until promoted to initiative or ticket
- single bounded execution -> ticket anchor; use `loom-tickets` or `loom-ralph`,
  not the full drive loop

For true high-level drives, prefer an initiative anchor. The anchor does not own
live execution state; it points to the current plan, active tickets, evidence,
critique, and next route.

## Required Checkpoint Fields

Record these facts in existing owner records before stopping, compacting, or
launching child work:

```text
drive anchor: <initiative id or narrower owner id>
objective criteria: <OBJ-IDs and satisfied | partial | open | blocked>
current tranche: <plan section / wave / ticket IDs>
active tickets: <ticket IDs and live states>
hard gates: <clear | blocked, with blocker links>
last route result: <route, output link, reconciliation target>
last child output: <packet/handoff/evidence/critique link if applicable>
pending operator question: <exact question or none>
next route: <ask_user | research | spec | plan | ticket | Ralph | evidence | critique | wiki | retrospective | acceptance | stop>
next route owner: <which owner skill/layer changes next>
resume instruction: <one sentence a fresh parent can follow>
updated_at: <timestamp>
```

Put each field in the owner record that owns it. The initiative can summarize the
drive anchor and objective status; tickets own active execution state, critique
disposition, and acceptance decisions; plans own tranche sequencing; evidence and
critique own support, findings, and verdicts.

## Deterministic Resume Discovery

When entering a workspace to resume a drive:

1. Load `loom-bootstrap`, inspect workspace, and read `constitution:main`.
2. Search active execution surfaces:

```bash
rg -n 'status: (active|blocked|review_required|complete_pending_acceptance)' .loom/tickets
rg -n 'continuity snapshot|drive anchor:|next route:|resume instruction:' .loom/initiatives .loom/plans .loom/tickets
rg -n 'loom-drive|objective-driven|OBJ-[0-9]{3}' .loom
```

3. Read the anchor initiative or the active ticket chain surfaced by the search.
4. Read linked research/spec/plan/evidence/critique only as needed to recover the
   next route.
5. If no checkpoint or anchor can be found, do not invent one from memory. Ask
   the user or route to workspace/status diagnosis.

## Hard Preflight Gates

These gates run before local execution, Ralph, acceptance, dependent continuation,
or route federation.

There are two outcomes:

- **repair route required**: the failed gate routes to the owner layer that can
  repair it, such as research, spec, plan, ticket refinement, evidence, critique,
  records repair, or a user question
- **execution blocked**: implementation, acceptance, and dependent continuation
  must not proceed until the gate is repaired or the user explicitly accepts the
  risk in the owning ticket

Failed gates do not block their own repair routes. They do block pretending the
repair already happened.

- Authority gate: objective, autonomy, non-goals, and human-decision triggers are
  clear enough; otherwise ask the user or update the initiative.
- Scope gate: next work is inside the initiative, plan, ticket, and write scope;
  otherwise refine plan/ticket scope or stop.
- Behavior gate: intended behavior and acceptance are not ambiguous; otherwise
  route to spec before implementation.
- Evidence gate: required observations exist; otherwise route to evidence or
  research before relying on the claim.
- Critique gate: mandatory critique is complete, pending as next route, blocking,
  or not required with rationale according to ticket-owned disposition status;
  unresolved medium/high findings block acceptance and dependent implementation
  that would rely on the challenged claim.
- Write-boundary gate: child write scopes are explicit and non-overlapping unless
  intentionally sequenced; otherwise route to plan/ticket/Ralph packet repair.
- Budget/safety gate: time, cost, privacy, security, and risk limits are not
  exceeded; otherwise ask the user or stop.
- Resume gate: checkpoint fields are current before child launch, route handoff,
  parent stop, or any step that depends on recoverable continuation.

Route priority applies only after hard gates pass or when the selected route is
the repair route for the failed gate.

## Route Federation Contract

Route federation means the parent may launch or sequence multiple domain routes
under one drive, such as research, spec, plan, Ralph, critique, and wiki. It is
not parallelism by default. Repair routes may be federated only when their inputs
and write scopes are independent.

Each federated route needs:

- route target and owning skill
- source snapshot or read scope
- child write scope or explicit read-only posture
- expected output contract
- failure/blocker vocabulary
- parent merge target
- concurrency posture: sequential, parallel-safe, or forbidden

Parallel route federation is allowed only when tickets and write scopes are
independent, no generated files/lockfiles/shared state conflict, and the parent
can reconcile combined results before dependent continuation.

## Stop Rule

If the checkpoint cannot be found, cannot be updated, or does not make the next
route recoverable, stop driving. The correct next route is to repair the owner
records or ask the user, not to continue from transcript intuition.
