# Plan Shape

## Core sections

- Purpose
- Strategy
- Strategy Snapshot
- Workstreams
- Milestones
- Sequencing
- Execution Waves
- Risks
- Evidence Strategy
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

- spec or ticket-local acceptance coverage: each intended behavior has an owner
- no placeholders: no `TBD`, `TODO`, vague "handle edge cases", or
  "write tests later" steps that would make a worker guess
- clear decomposition: each downstream slice can become one ticket or one short
  staged sequence of tickets
- likely write scopes: expected record or source boundaries are narrow enough to
  check for overlap
- likely verification posture: behavior slices normally imply `test-first` or
  `observation-first`, not `none`
- evidence and critique route: the plan says what kind of proof and review the
  downstream tickets should expect
- stop and loopback conditions: ambiguity routes back to research, spec, plan, or
  ticket refinement instead of being forced through execution

This review can be inline for low-risk plans. Use critique when a plan is broad,
high risk, or likely to mislead downstream workers.

## Good linking

Plans usually link to:

- initiative
- research
- spec
- tickets
- critique when review changes the route

## Execution Waves

Use `# Execution Waves` when a plan contains tickets that may be run in
parallel or must be staged.

Group possible parallel work by independent problem domain before launching
children. Independent means the tickets can be understood, mutated, verified, and
reconciled without relying on another child result in the same wave.

Parallel work is allowed only when:

- ticket `depends_on` relationships do not conflict
- expected packet `child_write_scope` values do not overlap
- there is no shared generated file, migration, lockfile, or stateful resource
  contention

The plan names the wave. Each ticket and packet still owns its own execution
truth.

After a parallel wave returns, integration validation belongs in the parent route
before acceptance. Child success reports do not prove the combined result.
