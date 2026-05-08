---
name: loom-agent-orchestration
description: "Coordinate fresh workers, subagents, and parallel execution safely. Use when executing a plan with independent tasks, dispatching multiple agents, reviewing child outputs, partitioning work, or deciding whether tasks can run concurrently without overlapping Loom or Git scope."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow-coordinator
---

# loom-agent-orchestration

Agent orchestration is parent-side coordination over disposable workers.

This playbook adapts subagent-driven development, plan execution, and parallel
dispatch into Loom's owner graph. Ralph remains the canonical bounded
implementation handoff loop; this playbook helps decide when and how multiple
fresh contexts should be used safely.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- worker partitioning from plans and tickets
- fresh-context prompts or Ralph packet selection
- parallelization safety checks
- child status handling and parent reconciliation
- staged review: spec compliance, code quality, evidence, critique
- conflict integration across workers

## What This Workflow Does Not Own

- Ralph packet semantics; use core Ralph
- live ticket state; use tickets
- plan sequencing; use plans
- Git isolation; use `loom-git`
- critique verdicts; use critique
- external harness worker lifecycle or hidden state

## Use This Skill When

- a plan has multiple implementation tasks and fresh workers are available
- independent bugs, test failures, or feature slices can be investigated separately
- a parent wants one worker per ticket, packet, or problem domain
- parallel execution might save time but write-scope conflicts are possible
- child outputs need spec compliance and quality review before integration

## Do Not Use This Skill When

- tasks are tightly coupled or share unresolved contracts
- write scopes overlap or generated artifacts/lockfiles would conflict
- one local edit is simpler and safer
- the plan is not ready enough to give a worker full context
- the goal is to avoid parent reconciliation work

## Default Procedure

1. Start from owner records: plan, tickets, specs, evidence, and current blockers.
2. Partition by independent problem domain or ticket, not by arbitrary file count.
3. Check non-overlap: acceptance, write scope, tests, generated files, locks,
   migrations, shared state, and Git branches/worktrees.
4. Choose transport: Ralph packet for implementation mutations that need durable
   contract; harness subagent prompt for bounded research/review/support work when
   appropriate; local execution for tiny safe steps.
5. Give each worker self-contained context: mission, owner chain, read scope, write
   scope, verification, stop conditions, and output contract.
6. Do not make workers read a broad plan and infer their task. Extract the specific
   task and relevant context for them.
7. Handle child statuses deliberately: done, done with concerns, needs context,
   blocked, or escalates.
8. Review child output for spec compliance before code quality. Then verify evidence
   and diff/write-scope compliance.
9. Integrate sequentially when outputs return. Run combined verification before
   claiming the parent tranche advanced.
10. Reconcile ticket truth, evidence, critique, and follow-ups after every accepted
    child result.

## Parallel Safety

Parallel execution is allowed only when:

- tasks have no dependency conflict
- child write scopes do not overlap
- shared contracts are already stable
- generated artifacts, migrations, lockfiles, and config are not contested
- each worker has a distinct Git worktree or equivalent isolation when files mutate
- parent can integrate and verify all results afterward

If any condition fails, run sequentially or return to planning.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "More agents means faster." | More agents without independent scopes create merge conflicts and inconsistent truth. |
| "The worker can read the plan." | Workers need a bounded task with curated context and stop conditions. |
| "The child said done, so move on." | Parent must verify output, evidence, scope, and ticket reconciliation. |
| "Spec review and code review are the same." | First check whether the right thing was built, then whether it was built well. |

## Red Flags

- parallel workers edit the same files, lockfiles, migrations, or generated outputs
- child prompt inherits transcript context instead of explicit owner records
- parent skips review loops or combined verification
- blocked child is retried with the same context and model without changing anything
- child concerns are ignored because output appears complete
- ticket state is updated from child report without parent inspection

## Verification

- [ ] Tasks are independent and write scopes do not overlap.
- [ ] Each worker has owner context, read/write scope, verification, stop conditions, and output contract.
- [ ] Git/worktree isolation matches parallel risk.
- [ ] Parent reviewed spec compliance, quality, evidence, and diff scope.
- [ ] Combined verification ran before parent-level success claims.
- [ ] Ticket/evidence/critique reconciliation is current.

## Done Means

- parallel or delegated work stayed inside bounded scopes
- child outputs were verified and reconciled by the parent
- integration state is evidence-backed and ticket-owned
- no external worker report became shadow truth

## Read In This Order

Read immediately for worker orchestration:

1. `references/worker-partition-and-review.md` for partitioning, worker prompts,
   status handling, parallel safety, and staged review.
2. the core `loom-ralph` skill when implementation work needs durable packets.
3. the core `loom-plans` and `loom-tickets` skills when tasks must be decomposed
   before dispatch.
4. `skills/loom-git/SKILL.md` when file mutations need branch/worktree isolation.

Then read conditionally:

5. `skills/loom-code-review/SKILL.md` for review loops and feedback disposition.
6. the core `loom-tickets`, `loom-evidence`, and `loom-critique` skills before
   parent success claims and for reconciliation.
