# Workflow Selection

This reference keeps the old filename for compatibility, but it no longer defines
a saved workflow-choice system.

Loom operators should choose the next skill, owner layer, or workflow by reasoning
over owner records, ticket state, blockers, evidence, critique, acceptance,
plans, specs, and journals. Do not serialize that reasoning into `next route`,
`Route`, `proposed next route`, or route-readiness fields in tickets,
initiatives, plans, workspace snapshots, or support handoffs.

## Core Rule

The filesystem graph should contain enough facts for a fresh agent to decide what
to do next. It should not contain a separate workflow-routing ledger.

Use records this way:

- tickets own live execution state, blockers, scoped acceptance, evidence
  disposition, critique disposition, acceptance decisions, and journal history
- plans own complex-change planning, decomposition, sequencing, and tranche strategy
- specs own intended behavior and reusable acceptance contracts
- research owns investigations, options, conclusions, and null results
- evidence owns observed artifacts and support/challenge links
- critique owns findings, verdicts, risks, and required follow-up
- wiki owns accepted explanation
- packets own bounded child-worker contracts

If those records do not make the next action clear, improve the owner record that
owns the missing fact. Do not patch the ambiguity with a saved workflow value.

## Packet Exception

Packets are the exception because they are bounded contracts for fresh-context
work. A packet may serialize:

- the exact task for this iteration or review/synthesis pass
- read scope and write scope
- source fingerprint and context budget
- stop conditions for the child
- output contract
- child outcome vocabulary when the packet family defines it
- parent merge expectations

That packet grammar does not justify adding saved workflow fields to tickets or
other owner records. After a packet returns, the parent reconciles facts into the
ticket, evidence, critique, wiki, spec, plan, research, initiative, or
constitution records that own them.

## Skill Selection Cues

These are reasoning cues, not values to save in a field:

- If the missing or changing truth is project identity, durable principles, hard
  constraints, roadmap direction, or citable decisions, use or update
  `loom-constitution`.
- If the missing or changing truth is objective framing, success metrics,
  delegated autonomy, or cross-ticket outcome ownership, use or update
  `loom-initiatives`.
- If the missing or changing truth is evidence synthesis, tradeoffs, rejected
  paths, options, or null results, use or update `loom-research`.
- If the missing or changing truth is intended behavior, requirements, scenarios,
  or reusable acceptance criteria, use or update `loom-specs`.
- If the missing or changing truth is complex-change planning, decomposition,
  sequencing, dependency order, tranche strategy, or rollout, use or update
  `loom-plans`.
- If the missing or changing truth is live bounded execution state, blockers,
  scoped acceptance, critique/evidence disposition, or closure, use or update
  `loom-tickets`.
- If the missing or changing truth is one bounded implementation handoff needing
  explicit read/write scope and fresh context, use a `loom-ralph` packet.
- If the missing or changing truth is observed outputs, validation artifacts,
  logs, screenshots, scans, or reproduction evidence, use or update
  `loom-evidence`.
- If the missing or changing truth is adversarial review, findings, verdicts,
  risk, or acceptance sufficiency review, use or update `loom-critique`.
- If the missing or changing truth is accepted explanation, workflow knowledge,
  architecture notes, or troubleshooting knowledge, use or update `loom-wiki`.
- If the missing or changing truth is accepted learning that needs promotion or
  prevention before closure, use `loom-retrospective`.
- If already-truthful work needs PR, release, merge, or handoff packaging, use
  optional `loom-ship` or an equivalent shipping workflow.
- If workspace structure, repository scope, owner-chain trust, or cold-start
  recovery is unclear, use or update `loom-workspace`.
- If the content is support-only retrieval cues, preferences, reminders,
  entities, or hot context, use `loom-memory` support recall.

When the user asks in ordinary coding-task language such as bug, feature,
refactor, tests, dependency, performance, UI, API, release, or done/acceptance
terms, use `skills/loom-workspace/references/task-routing-catalog.md` as a
prompt-language companion to this owner-truth table.

Use ordinary prose when explaining why you chose a skill. Do not create a route
field just to make the choice look deterministic.

## Vocabulary Boundaries

Keep these categories distinct:

- Ticket execution states
  - Examples: `proposed`, `ready`, `active`, `blocked`, `review_required`,
    `complete_pending_acceptance`, `closed`, `cancelled`
  - Boundary rule: Describe live ticket state. They are not workflow
    instructions.
- Record lifecycle statuses
  - Examples: `draft`, `active`, `accepted`, `recorded`, `superseded`,
    `abandoned`
  - Boundary rule: Describe record lifecycle or support-surface state. They are
    not next-action commands.
- Ralph child outcomes
  - Examples: `continue`, `stop`, `blocked`, `escalate`
  - Boundary rule: Child output for parent reconciliation inside the packet loop.
    It becomes ticket truth only after parent reconciliation.
- Critique-owned finding states
  - Examples: `open`, `withdrawn`
  - Boundary rule: Live inside critique records and describe whether critique
    still stands behind a finding.
- Ticket-owned finding dispositions
  - Examples: `resolved`, `accepted_risk`, `superseded`,
    `converted_to_follow_up`
  - Boundary rule: Live in the ticket's review/follow-through section for
    qualified findings. They do not name a next workflow.
- Support-memory surfaces
  - Examples: `memory`, `loom-memory`, retrieval cues, preferences, reminders,
    hot context
  - Boundary rule: Support recall only. If the content becomes project truth,
    move it to the owner layer.
- Git support coordination
  - Examples: branch, worktree, baseline, diff provenance
  - Boundary rule: Support behavior for isolation and provenance. Git does not
    own Loom truth or workflow ownership.
- Commands and adapters
  - Examples: slash commands, harness commands, MCPs, package wrappers
  - Boundary rule: Invocation conveniences. They may transport work, but owner
    records and skills still own truth.

When the same word appears in multiple contexts, the field and owner decide the
meaning. A Ralph child `outcome: continue` is packet output. A ticket
`status: blocked` is live execution state. Neither should be converted into a
saved workflow route.

## Stopping, Asking, And Continuing

Do not encode `stop`, `ask_user`, or `continue` as saved workflow values in owner
records.

Use the existing owner surface:

- If a ticket is done, record the acceptance decision and close it.
- If a ticket should not proceed, use `status: cancelled` with rationale, or
  `blocked` when a real blocker remains.
- If a human decision is needed, record the decision needed, unsafe-inference
  reason, and owner record that will change in the relevant ticket, initiative,
  spec, plan, or constitution record.
- If work continues, the next action should be inferable from open blockers,
  evidence gaps, critique disposition, acceptance gaps, plan strategy, and the
  journal.

The agent's reasoning is part of the protocol. Skills pair with that reasoning;
they do not need every next choice serialized.
