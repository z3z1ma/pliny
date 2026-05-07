# Plan Shape

## Core sections

- Purpose
- Context And Orientation
- Strategy
- Planning Decisions
- Workstreams
- Execution Units / Ticket Slices
- Milestones
- Sequencing
- Claim / Acceptance Coverage
- Validation And Acceptance Strategy
- Interfaces And Dependencies
- Idempotence And Recovery
- Execution Waves
- Risks
- Supporting Artifacts And Notes
- Plan Readiness Review
- Exit Criteria
- Completion Basis when `status: completed`

## Center Of Gravity

A plan's center of gravity is decomposition: turning high-level work, specs,
research conclusions, initiatives, migrations, or refactors into units of
execution that can become tickets. Sequencing, rollout, milestones, and waves are
strategy around those units; they are not a substitute for the units.

If the plan cannot name ticket-ready units yet, keep applying the planning
procedure or route back to spec/research/initiative before creating broad execution
tickets.

## Self-Orienting Plan Discipline

Some planning styles optimize for a single self-contained document a stateless
agent can execute from start to finish. Loom keeps the useful orientation and
observable-proof bar, but routes live truth through owner layers instead of making
the plan a second ledger.

Map the durable concepts this way:

- purpose / big picture -> plan `# Purpose`
- context and orientation -> plan `# Context And Orientation`, with links to
  owner records instead of duplicating their full contents
- plan of work / concrete steps -> plan `# Execution Units / Ticket Slices`, then
  downstream tickets and packets for live execution contracts
- milestones -> plan `# Milestones`, as narrative checkpoints with expected proof,
  not status checklists
- validation and acceptance -> plan `# Validation And Acceptance Strategy`, while
  tickets own live evidence sufficiency and acceptance decisions
- interfaces and dependencies -> plan `# Interfaces And Dependencies`
- idempotence and recovery -> plan `# Idempotence And Recovery`
- artifacts and notes -> plan `# Supporting Artifacts And Notes`, with raw
  observations preserved in evidence and reusable synthesis in research or wiki
- progress -> tickets, not plans
- surprises and discoveries -> evidence, research, ticket journal, or
  retrospective depending on the truth being changed
- decision log -> plan `# Planning Decisions` only for execution-strategy
  decisions; behavior, policy, and live acceptance decisions route to their owners
- outcomes and retrospective -> ticket closure, retrospective, wiki/research/spec
  promotion, and plan `# Completion Basis` when the plan itself completes

A good Loom plan is therefore self-orienting but not hermetic. It should tell a
fresh agent enough to navigate the owner graph and draft or refine the next ticket
without transcript context. It should not copy every source record or become a live
progress log.

If plan prose starts looking like a checkbox workflow, translate executable
detail into ticket acceptance or packet task text before a worker starts. The plan
may name proof targets for tickets and packets to validate; it does not become the
execution contract, evidence owner, or acceptance dossier.

## Execution Units / Ticket Slices

Each execution unit is a proposed ticket or tight sequence of tickets. It should
be detailed enough that a fresh agent can draft or refine the ticket without
reconstructing the plan from chat.

For each unit, name:

- source claim, spec acceptance ID, research conclusion, or initiative objective
- observable outcome or deliverable
- likely write boundary, including records and source paths when known
- explicit non-goals and scope exclusions
- dependency or ordering reason
- verification posture and evidence target
- critique expectation when risk warrants it
- stop or loopback condition if execution discovers missing behavior, evidence,
  architecture, source, or sequencing truth

Vertical slices are preferred for behavior work: a narrow path through the real
user, API, data, or operator surface that produces observable value. Horizontal
slices are acceptable only when the layer itself is the product of the ticket or a
bounded prerequisite.

## Context And Orientation

Context should make the plan usable by a fresh agent. Include only what shapes the
execution route:

- governing initiative, spec, research, decision, wiki, or ticket links
- terms of art that matter for this plan
- relevant source areas, records, interfaces, or systems
- current constraints or assumptions that affect decomposition

Do not duplicate entire owner records. Link them, summarize the part that matters,
and route changes back to the owner.

## Milestones

Milestones are narrative proof checkpoints across execution units. They should say:

- what scope the milestone covers
- what exists or works at the end that did not exist before
- which units or tickets it contains
- what validation, evidence, or critique should be available
- what acceptance checkpoint or loopback follows

Milestones do not own live progress. If execution state changes, update the ticket.

## Strategy And Planning Decisions

Planning decisions capture why the execution route is shaped this way. Record only
decisions the plan owns: decomposition, ordering, risk sequencing, parallelization,
or recovery strategy. Route behavior decisions to specs, durable policy decisions
to constitution, evidence conclusions to research/evidence, and live acceptance
decisions to tickets.

Do not let planning decisions become a transcript log or progress journal.

Plan milestones are execution-sequencing checkpoints. They are not roadmap
commitments, initiative outcome metrics, or ticket progress state.

## Validation, Acceptance, Recovery, And Interfaces

Plans should name the proof shape for downstream work without claiming acceptance.
Use `# Validation And Acceptance Strategy` to describe expected tests, manual
observations, red/green evidence, screenshots, traces, or critique profiles. The
ticket still owns whether the evidence is sufficient.

Use `# Interfaces And Dependencies` for modules, APIs, services, schemas,
migrations, feature flags, datasets, libraries, or environment assumptions that
shape execution. This section should make hidden coupling visible before tickets are
created.

Use `# Idempotence And Recovery` when steps may be repeated, resumed, partially
rolled back, or affected by stateful resources. A fresh agent should know where to
look for current live state and what cleanup or rollback route is expected.

## Plan Readiness Review

Before a plan drives tickets or packets, review it for:

- claim coverage: each initiative objective, spec claim, or ticket-local
  acceptance criterion that constrains the plan is mapped to at least one
  downstream ticket, or marked `None - reason` when no claim-bearing source
  applies
- spec or ticket-local acceptance coverage: each intended behavior has an owner
  and the plan does not become the live acceptance ledger
- no placeholders: no `TBD`, `TODO`, vague "handle edge cases", or
  "write tests later" steps that would make a worker guess
- clear decomposition: each downstream slice can become one ticket or one short
  staged sequence of tickets
- context and orientation: enough repository and owner-record context exists for a
  fresh agent to navigate without transcript history
- narrative milestones: checkpoints name scope, expected result, and proof
- execution-unit detail: each proposed ticket has an outcome, source claim, likely
  write scope, non-goal, verification target, and loopback condition
- validation and acceptance strategy: downstream proof expectations are concrete
  enough for tickets to inherit
- interfaces and dependencies: important APIs, services, records, migrations,
  data, flags, or environmental assumptions are visible
- idempotence and recovery: retries, rollback, cleanup, and live-state recovery are
  named when relevant
- zero-context handoff quality: a fresh worker can infer the relevant files or
  records, owner constraints, verification target, stop conditions, and non-goals
  from the plan and linked records without transcript archaeology
- likely write scopes: expected record or source boundaries are narrow enough to
  compare against packet `child_write_scope` values and check for overlap
- execution-wave independence: any proposed parallel wave has no same-wave
  dependency conflict, no write scope overlap, and no shared generated file,
  lockfile, migration, or stateful-resource contention; otherwise write
  `None - reason` and run sequentially or loop back to planning
- likely verification posture: behavior slices normally imply `test-first` or
  `observation-first`, not `none`
- evidence and critique route: the plan says what kind of proof and review the
  downstream tickets should expect
- stop and loopback conditions: ambiguity routes back to research, spec, plan, or
  ticket refinement instead of being forced through execution
- supporting artifacts and notes: important source material is linked or excerpted
  concisely, with raw observations routed to evidence or research
- critical pre-execution review: broad or high-risk plans are read once as if by
  the downstream worker, and gaps that would make that worker guess are fixed or
  routed before execution starts

## Claim / Acceptance Coverage

Use claim coverage mapping when a plan translates initiative outcomes, research
conclusions, specs, or ticket-local acceptance criteria into executable tickets.

The plan should name:

- the source claim or acceptance ID, such as `initiative:<slug>#OBJ-001`,
  `spec:<slug>#ACC-001`, or `ticket:<token>#ACC-001`
- the downstream ticket expected to cover it
- the evidence or critique route the ticket should prepare for
- any explicit gap, written as `None - reason`, rather than leaving coverage
  implicit

This mapping is a routing aid. The downstream ticket owns live coverage state,
evidence disposition, critique disposition, and acceptance decisions. If the
acceptance contract itself changes, update the owning spec or ticket rather than
letting plan prose redefine it.

## Good linking

Plans usually link to:

- initiative
- research
- spec
- tickets
- critique when review changes the route

## Execution Waves

Use `# Execution Waves` when a plan contains tickets that may be run in
parallel or must be staged. Plans may identify a possible wave, but they do not
make parallel execution the default.

Group possible parallel work by independent problem domain before launching
children. Independent means the tickets can be understood, mutated, verified, and
reconciled without relying on another child result in the same wave.

Parallel work is allowed only when:

- ticket `depends_on` relationships do not conflict
- expected packet `child_write_scope` values do not overlap
- legacy packet `write_scope` values, when reviewing older records, do not
  overlap
- there is no shared generated file, migration, lockfile, or stateful resource
  contention

If no parallel or staged wave applies, write `None - reason` rather than leaving
the independence check implicit.

Before any sibling Ralph execution, record a compact wave check in the plan,
ticket journal, or packet working notes; scratch notes are temporary before
launch only:

| Wave | Tickets | Independence basis | `child_write_scope` / write scope overlap check | Shared-state check | Parent reconciliation |
| --- | --- | --- | --- | --- | --- |

For Git-backed parallel Ralph, cross-check
`skills/loom-ralph/references/parent-child-handshake.md` and
`skills/loom-git/references/parallel-ralph-with-git.md`. Ralph packet
independence and Git worktree/branch independence are separate requirements; one
does not satisfy the other.

The plan names the wave. Each ticket and packet still owns its own execution
truth.

After a parallel wave returns, integration validation belongs in the parent route
before acceptance. Child success reports do not prove the combined result.
