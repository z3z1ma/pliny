# Plan Shape

## Core sections

- Purpose
- Strategy
- Strategy Snapshot
- Workstreams
- Milestones
- Sequencing
- Claim / Acceptance Coverage
- Execution Waves
- Risks
- Evidence Strategy
- Plan Readiness Review
- Exit Criteria
- Completion Basis when `status: completed`

## Notes

`Strategy Snapshot` in a plan is not the same as ticket execution truth.

Use it for the current strategic picture, not line-by-line implementation
journal entries.

Plan milestones are execution-sequencing checkpoints. They are not roadmap
commitments, initiative outcome metrics, or ticket progress state.

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

This review can be inline for low-risk plans. Use critique when a plan is broad,
high risk, or likely to mislead downstream workers.

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
