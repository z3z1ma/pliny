---
name: loom-drive
description: "Drive a high-level user objective across multiple Loom phases. Use when the user delegates an outcome that needs objective shaping, owner-record updates, bounded tickets, Ralph/local execution, evidence, critique, reassessment, and continuation without prompting every downstream step."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow-coordinator
---

# loom-drive

`loom-drive` is the objective-driven parent-loop coordinator.

It gives the current agent a procedure for turning a broad user objective into
owner records, bounded ticket tranches, Ralph or local execution, reconciliation,
and continuation decisions.

## Essence

The essence of `loom-drive` is sustained parent judgment.

The user should be able to say what outcome they want, not manually operate every
Loom phase. The parent agent then keeps asking the same governing question:

> What is the next owner-truth mutation or bounded execution step that most
> directly advances the objective without inventing authority?

`loom-drive` is successful when the agent can keep moving between shaping and
execution while the filesystem graph remains the recoverable source of truth. It
is a failure if the real plan lives in chat, if the agent keeps asking for
approval on every obvious next ticket, or if autonomy becomes an excuse to widen
scope without owner records.

## Drive Contract

When this skill activates, the parent accepts a drive contract:

- make the objective measurable enough to judge continuation
- preserve all durable truth in the correct Loom owner layer
- decompose only the next useful tranche, not the whole imagined future
- execute only bounded work through local edits, Ralph, or domain workflows
- reconcile every child result before depending on it
- continue without waiting for unnecessary user prompts while work remains within
  delegated authority
- stop and ask when the next choice would invent product direction, accept
  material risk, or exceed scope, safety, time, or budget limits

The contract is suspended when the objective can no longer be advanced safely
from the recorded truth.

## Drive Continuity

The loop remains recoverable across sessions only when the current drive state is
recorded in owner artifacts. Before executing downstream work, establish a drive
checkpoint from existing layers:

- initiative owns the objective, measurable success criteria, delegated autonomy,
  budget/time limits, and objective-level stop conditions
- initiative success criteria should use stable objective criterion IDs such as
  `OBJ-001` when downstream tickets, evidence, or critique need to cite them
- research owns unresolved evidence, options, rejected paths, and conclusions
- spec owns intended behavior and reusable acceptance criteria
- plan owns tranche strategy, sequencing, dependencies, and execution waves
- tickets own live execution state, next route, blockers, scoped coverage,
  evidence disposition, critique disposition, and acceptance decisions
- packets own bounded child contracts; saved drive handoffs are support artifacts
  that may carry child context, source snapshot, proposal-time write scope, stop
  conditions, and output contract without owning canonical truth
- evidence, critique, and wiki own observed support, adversarial verdicts, and
  accepted explanation

If a fresh agent could not resume from those records, stop driving and repair the
checkpoint before launching more work.

Use `references/continuity-contract.md` for the continuity snapshot convention:
objective status, current tranche, and next route are pinned to existing
owner-record sections instead of to a new ledger.

Use `references/checkpoint-resume-protocol.md` before stopping, compacting,
launching child work, or handing control to another route. If the checkpoint
cannot be found or updated in owner records, stop driving. Before any child
launch, the checkpoint must already be current; "can update later" is not enough.

## What This Skill Owns

- activation and routing for high-level objective requests
- focused objective-shaping questions before downstream execution
- the repeated parent loop across existing Loom owner layers
- tranche planning and ticket creation posture
- delegation boundaries for Ralph, local edits, critique, wiki, research, and
  optional subagents
- continuation, human-escalation, and stop-condition decisions

## What This Skill Does Not Own

- project truth that belongs in initiative, research, spec, plan, ticket,
  evidence, critique, wiki, or constitution records
- support recall that belongs in memory records
- live execution state; use tickets for execution status, blockers, and closure
- bounded child contracts; Ralph packets own implementation handoff contracts
- critique verdicts or wiki explanation truth
- external scheduling or persistent agent identity

Workflow coordination is not truth ownership. When this skill creates or changes
durable claims, route them into the layer that owns that kind of truth.

## Use This Skill When

- the user asks for a broad outcome, product change, project improvement, or
  multi-step objective rather than one known bounded edit
- an existing initiative or plan should continue without the user manually
  prompting each next ticket
- the next move requires moving between objective framing, planning, tickets,
  Ralph execution, evidence, critique, wiki, and reassessment
- context pressure suggests a bounded outer-loop synthesis handoff would make the
  parent more reliable

## Do Not Use This Skill When

- the request is already one clear local edit or one Ralph-ready ticket
- the next truth change belongs entirely to one owner-layer skill
- the user is asking a question that should stay in research, spec shaping, or
  ordinary explanation
- the request depends on capabilities outside the recorded Loom workflow
- scope, budget, authority, or risk is too ambiguous to proceed after focused
  questions

## Activation Triggers

Activate `loom-drive` for chat requests shaped like:

- "build/implement/improve X" where X implies multiple owner records or tickets
- "take this objective and keep going until it is done"
- "continue this initiative/plan" when the next ticket tranche is not yet obvious
- "drive this project toward <outcome>" with delegated autonomy

Before activating, route through `loom-workspace` if the workspace, owner chain,
or repository scope is not trustworthy enough to drive.

Do not activate merely because a task is large. Activate when the user is
delegating outcome advancement across phases. A large but already ticket-ready
implementation still belongs directly to `loom-tickets` or `loom-ralph`.

## User Questioning Posture

Ask only enough focused questions to make the first durable objective safe to
record. Prefer a small batch of questions over repeated approval gates.

Clarify these before downstream tickets depend on them:

- measurable objective and success criteria
- hard constraints, non-goals, and risk tolerance
- autonomy limit: what the agent may decide without returning to the user
- budget or time limits, if any
- stop conditions that require human judgment
- first tranche priority when several routes are plausible

Once those are clear enough, proceed through Loom records without asking for
approval before every ticket. Stop and ask again only at explicit escalation
boundaries.

## Default Drive Loop

0. **Accept or refuse the drive contract** — decide whether enough authority,
   objective clarity, and workspace trust exist to drive rather than merely plan
   or ask questions.
1. **Shape the objective** — decide whether the request needs an initiative,
   `research`, `spec`, `plan`, `ticket`, or `local_edit` route.
2. **Record owner truth** — create or refine the initiative for outcome and
   metrics; add research, spec, or plan records only when those layers own missing
   evidence, behavior, or sequencing truth.
3. **Check continuity** — confirm objective, autonomy, current tranche, coverage,
   evidence, critique, and next-route state live in owner records rather than
   unrecorded conversation context.
4. **Plan the next tranche** — decompose only enough work to produce bounded,
   independently legible tickets for the next useful step. Use
   `references/tranche-decision-protocol.md` when objective gaps or sequencing
   ambiguity require an optional gap summary or fuller tranche detail before the
   next-route decision is safe.
5. **Create or refine tickets** — tickets own live execution state, blockers,
   next move, critique disposition, acceptance decisions, evidence disposition,
   and closure.
6. **Run preflight gates** — distinguish repair/shaping routes from execution
   routes. Failed gates route to their owner repair path; they block `local_edit`,
   `ralph`, `acceptance_review`, and dependent continuation until repaired.
7. **Execute bounded work** — use `local_edit` for tiny safe changes, `ralph` for
   fresh-context implementation, and domain skills for `critique`/`wiki`/`research`
   packetization. Declare read/write scope and stop conditions before child work.
8. **Reconcile results** — inspect child output, update ticket truth, route
   observations into evidence, findings into critique, accepted explanation into
   wiki, and changed strategy or behavior into the owner layers.
9. **Reassess objective state** — compare current evidence, critique disposition,
   acceptance coverage, and remaining gaps against the objective's success
   criteria.
10. **Checkpoint** — update the drive anchor and live tickets so a fresh chat can
    resume without prior conversation context.
11. **Continue or stop** — create the next tranche, run required critique/wiki or
    retrospective, ask the user, or stop because the objective is satisfied,
    blocked, unsafe, over budget, or outside delegated authority.

See `references/drive-loop.md` for the fuller parent checklist.

## Optional Outer-Loop Subagent Transport

A dedicated outer-loop subagent may be used for context management when the
parent needs fresh synthesis of an objective chain, option set, tranche plan, or
risk list.

This is transport only:

- the subagent proposes owner-record changes, tickets, risks, and next routes
- the parent reviews the output before applying it
- canonical records retain truth ownership
- tickets retain live execution ownership
- parent reconciliation remains mandatory before dependent work launches
- the outer-loop handoff template is prompt-only by default; save it only when a
  durable support artifact is useful for reviewability, context recovery, or
  handoff audit
- saved outer-loop handoffs live under the optional, lazy-materialized,
  non-canonical support surface
  `.loom/support/drive-handoffs/<UTC compact timestamp>-<slug>.md` with
  `kind: support-artifact`, `support_kind: drive-outer-loop-handoff`, and
  `handoff_kind: outer-loop-synthesis`
- saved handoff status is support-local: `draft`, `reconciled`, `abandoned`, or
  `superseded`; it does not own objective state, live ticket state, acceptance,
  evidence sufficiency, critique verdicts, wiki truth, canonical truth, or packet
  lifecycle
- the outer-loop handoff template is not a packet family and not a truth owner
- any handoff `write_scope` is proposal-time permission for that support
  handoff, not Ralph `child_write_scope`
- do not create `.loom/support/` merely during bootstrap; create it only when a
  saved support artifact is intentionally materialized

Use `templates/outer-loop-handoff.md` only when a bounded handoff would reduce
context pressure or improve reviewability.

## Stop Or Ask The User When

- success criteria, autonomy limits, or non-goals remain materially ambiguous
- the next step would invent product direction the user has not delegated
- scope would widen beyond the current initiative, plan, ticket, or write boundary
- required evidence is missing or contradicted
- open or unresolved medium/high critique findings lack ticket-owned dispositions
  such as resolved, accepted risk, superseded, or linked follow-up work
- a ticket is blocked, write scopes overlap unsafely, or parallel work could
  corrupt shared state
- budget, time, safety, privacy, or risk limits are reached
- continuation would depend on state or capabilities that cannot be expressed in
  Loom owner records and bounded routes

## Done Means

- the objective and success criteria live in the correct owner record
- current execution state lives in tickets, not chat or a plan
- each child or local execution step has been reconciled into ticket truth
- evidence and ticket-owned critique dispositions are explicit enough for the next
  decision
- the parent has either created the next bounded tranche, asked the user a focused
  question, routed to critique/wiki/retrospective, or recorded why the loop stops

## Read In This Order

Read immediately when activating `loom-drive`:

1. `references/drive-loop.md` for the parent-loop checklist and routing rules.
2. `references/continuity-contract.md` for the owner-record fields that must
   carry resumable drive state.
3. `references/tranche-decision-protocol.md` for conditional objective-gap
   summaries, optional tranche detail, route priority, and reconciliation targets.
4. `references/checkpoint-resume-protocol.md` for hard safety gates, route
   federation, checkpoint updates, and deterministic resume.
5. `skills/loom-records/references/route-vocabulary.md` when writing checkpoint,
   resume, handoff, or route-readiness route fields.
6. `skills/loom-workspace/references/routing.md` if the next owner layer or
   workflow coordinator is still unclear.

Then read conditionally:

7. `skills/loom-initiatives/SKILL.md` when creating or refining the objective and
    success metrics.
8. `skills/loom-research/SKILL.md`, `skills/loom-specs/SKILL.md`, or
    `skills/loom-plans/SKILL.md` when evidence, intended behavior, or sequencing
    is missing.
9. `skills/loom-tickets/SKILL.md` before creating, advancing, or accepting
    bounded execution work.
10. `skills/loom-ralph/SKILL.md` before packetized implementation execution.
11. `skills/loom-evidence/SKILL.md`, `skills/loom-critique/SKILL.md`,
    `skills/loom-wiki/SKILL.md`, or `skills/loom-retrospective/SKILL.md` when
    observations, review, accepted explanation, or learning assimilation is next.
12. `templates/outer-loop-handoff.md` only when launching an optional bounded
    outer-loop synthesis subagent.
