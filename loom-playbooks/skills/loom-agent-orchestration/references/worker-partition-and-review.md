# Worker Partition And Review

Use this reference when multiple fresh contexts, subagents, or Ralph packets may
advance work faster or more safely than one long-running parent context.

## Parent Role

The parent owns:

- selecting tasks fit for delegation
- compiling context and packet contracts
- choosing sequential versus parallel execution
- inspecting child outputs
- integrating diffs and evidence
- reconciling owner records
- stopping when scope or truth discipline is violated

The child owns one bounded task. It does not own the whole workflow.

## Partitioning

Partition by independent problem domain:

- one ticket or one Ralph packet
- one failing test file only when failures are independent
- one subsystem with no shared write scope
- one review perspective such as spec compliance or code quality
- one research question or codemap slice

Do not partition by arbitrary line count if the same concept crosses files.

## Worker Context

Give each worker:

- mission
- owner chain and acceptance IDs
- exact task text or packet
- read scope and write scope
- relevant source, tests, patterns, and evidence
- constraints and out-of-scope items
- verification command or observation
- stop conditions
- output contract

Avoid asking workers to infer their part from a whole plan. Extract the task.

## Outcome Handling

For Ralph packets, use core child outcomes:

- `continue`: meaningful progress happened and another bounded iteration is likely next
- `stop`: the bounded task is complete and another iteration may not be needed
- `blocked`: a concrete blocker prevents progress
- `escalate`: the task should return to spec, plan, architecture, security,
  critique, or user decision

For non-Ralph harness workers, labels such as `done`, `done_with_concerns`, or
`needs_context` are transport summaries only. Map them into core owner truth:
ticket status, blockers, evidence, critique findings, or a revised packet/handoff
before depending on them.

Never ignore concerns just because files changed.

## Review Order

After implementation child output:

1. scope review: did it stay inside read/write authority?
2. spec compliance: did it build the right behavior and acceptance?
3. code quality: correctness, readability, architecture, security, performance
4. evidence review: do outputs support claims?
5. integration review: does it conflict with siblings?

Spec compliance comes before code quality. Well-written wrong behavior is still wrong.

## Parallel Dispatch

Parallel dispatch requires:

- independent tasks
- no shared write files
- stable shared contracts
- separate Git isolation for file mutation
- no contested generated artifacts or lockfiles
- parent capacity to review and integrate all results

When in doubt, run sequentially.

## Conflict Integration

When child outputs conflict:

- stop integration
- identify whether conflict is source, spec, plan, or ticket truth
- prefer owner-layer truth over child assertions
- update plan/tickets/packets before relaunching
- do not merge partial results that violate one another's acceptance claims

## Capability Selection

Use lighter workers for mechanical, narrow tasks with complete context. Use more
capable workers for broad integration, architecture judgment, security review,
or ambiguous debugging. If a worker blocks due to reasoning load, revise context,
split the task, or use a more capable reviewer rather than blind retry.

## Final Parent Verification

After all child outputs are integrated:

- inspect combined diff
- run combined verification
- update evidence
- run critique when required
- reconcile ticket status and finding disposition
- decide next tranche or closure gate

The parent-level claim is not valid until this combined verification exists.
