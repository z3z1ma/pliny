# Ralph Harness Invocation

## Parent-Side Goal

The parent uses this invocation when it has already compiled a Ralph packet and wants one fresh child context to perform one bounded execution step.

This is a fresh bounded worker session. The worker should not behave as if it owns the entire workflow.

The launch should feel like a handoff to a bounded implementer, not an invitation to improvise the whole protocol again.

## Resolving The Command

Resolve the harness invocation using the standard resolution order before launching:

1. **Check `.loom/harness.md`** — if the workspace has operator-defined harness profiles, select the profile that best matches the current task. Read the profile's prose to understand when it applies, then substitute `{{ packet_path }}` and `{{ prompt }}` into the command template.

2. **Discover the current harness** — if no `.loom/harness.md` exists, discover the harness you are running inside. Check the parent process name (`ps -o comm= -p $PPID`), check for environment markers, then learn the discovered tool's headless invocation syntax via its help output. Construct the command using that tool's file-attachment and prompt arguments.

3. **Ask the operator** — if discovery is ambiguous, ask the operator to create `.loom/harness.md` or provide the invocation command directly. Do not guess.

For the full harness profile convention and resolution details, read the harness-invocation-templates appendix in the core rules.

## Preflight Checklist

Before launching the command, the parent should confirm:

1. the packet exists on disk
2. the target is a ticket
3. the allowed write set is explicit
4. the packet is fresh enough for the current target state
5. the parent is prepared to reconcile the result afterward
6. the next move is genuinely bounded execution rather than review or docs work
7. the harness invocation is resolved (not guessed)

If any of those are false, do not launch yet.

## Prompt Shape

The prompt should be short, positive, and execution-specific.

It should name:

- the subsystem
- the target
- the kind of work to perform
- the output contract to return

Recommended prompt template:

```text
Execute the bounded Ralph packet for the attached ticket target. Perform the implementation or mutation work described by the packet, stay inside the declared write boundary, and return outcome status, files changed, verification summary, blockers, and continue/stop/blocked/escalate recommendation.
```

Strong prompt qualities:

- keeps the target ticket explicit
- repeats the write-boundary obligation
- asks for outcome classification and verification instead of vague completion claims
- stays short enough that the packet remains the real contract

## Child Procedure

Before acting:

- read the packet fully
- confirm the exact bound ticket target
- confirm the allowed write set and scope boundary
- understand the governing plan, spec, or constitution context included in the packet

During the run, the worker should behave like a bounded ticket implementer:

- keep attention on the bound ticket
- keep the packet contract more authoritative than any remembered prior chat state
- prefer explicit blockers and escalation over uncontrolled scope widening

During the run:

- perform one bounded iteration
- keep the bound ticket truthful before exit if the packet grants that write authority
- record or report verification performed

When the worker believes it is done, it should still check whether the ticket and evidence state are truthful enough for the parent to accept.

The child should avoid these failure modes:

- widening scope because a nearby change looks convenient
- treating remembered transcript context as higher authority than the packet
- claiming completion when the ticket, evidence, or blocker state is still unclear

When done:

- return outcome status
- return changed files or records
- return verification summary
- return blockers or residual risks
- return continue, stop, blocked, or escalate recommendation

## Expected Output Shape

The parent should expect the child to return:

- outcome status
- changed files or changed records
- verification performed
- blockers, risks, or unresolved findings
- ticket update recommendation
- continue, stop, blocked, or escalate recommendation

An especially strong return also includes:

- why the chosen outcome classification is correct
- whether the packet looked stale or contradictory at execution time
- whether any claimed change still needs parent-side correction during reconciliation

## Reconciliation After Return

After the child returns, the parent should:

1. inspect the claimed changes
2. confirm they stayed inside the allowed write set
3. validate affected records if needed
4. update the ticket so the execution ledger reflects the result
5. record or link verification evidence

If a Ralph launch returns without durable ticket activity where ticket activity was required, treat the run as incomplete.

Successful process completion is not enough. The durable ticket and evidence graph must also move forward truthfully.

## Retry Guidance

Compile a fresh packet instead of blindly retrying when:

- the target changed materially
- the prior run revealed missing context
- the packet scope needs to expand or narrow
- the prior result was blocked because the packet contract was incomplete

Do not retry by sending a longer or louder prompt if the packet contract itself is the problem. Fix the packet first.

## Anti-Pattern

This is a weak Ralph prompt:

```text
Finish the task from the packet and do whatever else seems necessary.
```

Why this is weak:

- it encourages scope widening
- it undermines the packet boundary
- it makes later reconciliation less trustworthy
