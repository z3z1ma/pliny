# Delegating To Workers

Use strict boundaries when the operator is temporarily out of the loop.

When ticket work is executed or delegated, use a Ralph packet. A packet is a
bounded contract for one run. It does not outrank the source records it cites.

The packet exists to make one bounded worker run recoverable, reviewable, and safe
to continue after the worker returns.

## Packet Before Launch

A Loom worker run is the packet file plus the launch that points to it. Compile the
Ralph packet under `.loom/packets/ralph/` before invoking a harness-native
subagent, headless harness command, or manual worker handoff.

Keep the launch wrapper thin: identify the packet path, tell the worker to read it
first, and request the packet's output contract. The packet carries the mission,
context, scope, stop conditions, evidence expectations, and allowed updates.

When a worker result will support ticket state, audit, evidence, research,
knowledge, or closure, keep the packet inspectable on disk so the parent and future
agents can review the handoff without replaying tool logs.

## When To Use A Packet

Use a packet when the next worker run can be bounded.

Good worker tasks have a clear mission, limited scope, known source records,
defined read and write areas, expected evidence or review output, and recognizable
stop conditions.

Do not delegate work that still needs operator shaping, high-authority judgment,
ambiguous product intent, unresolved policy, broad architectural direction,
unsettled data-model or state-modeling choices, or design-coherence decisions.
Shape that work first.

## Packet Contract

A useful packet tells the worker:

- the mission for this run
- the source records, refs, inlined context, or artifacts to trust
- the intended read area
- the intended write area
- the task boundary and non-goals
- relevant assumptions and constraints
- stop conditions
- expected evidence, review output, or validation result
- output expectations
- which records or artifacts should be updated while working

The worker should not have to infer scope from chat history.

The packet should be narrow enough that the worker can finish, stop, or report
blockage without inventing a plan of its own.

## Worker Authority

The worker operates inside the packet.

The worker may update source or work files within scope, the records or evidence
artifacts named by the packet, and the packet's worker output. If new evidence is
needed but not authorized by write scope, the worker should stop or report the
needed evidence instead of widening scope.

The worker should not directly change high-authority direction while executing.
Escalate before changing constitution, specs, plans, or research synthesis.

Knowledge updates should be proposed, not applied, unless the packet explicitly
authorizes that promotion.

Audit is a separate adversarial pass. A worker implementation report is not audit,
and a worker should not certify its own work as accepted.

## Worker Discipline

The worker should stop and report when:

- the packet no longer matches reality
- the requested change is broader than the declared scope
- required context is missing
- evidence or review output cannot be gathered
- implementation reveals a product, architecture, policy, or sequencing decision
- the safe next step belongs to another Loom surface

A worker should not silently widen scope to stay busy.

## Worker Output

The worker reports:

- what changed
- what evidence, review output, or validation result was gathered
- what was not verified or reviewed
- what remains blocked or risky
- what records were updated
- what it recommends next

## After Worker Return

The parent reads the updated records, evidence, packet, and worker report instead
of reconstructing work from tool logs.

The parent decides whether to stop, run another bounded worker run, gather more
evidence, route to audit, return to outer-loop shaping, update another surface, or
promote learning into knowledge.

When the result will support closure, acceptance, or durable reuse, route the claim
through audit backed by a Ralph review packet before treating the work as
trustworthy unless the consuming surface explicitly records why audit would not add
useful trust. The audit may be a narrow pass over the target records, evidence, and
diff.

## Packet Currency

Use a packet only while its target, context, scope, and assumptions still match
reality.

If the work has materially changed, write a new packet instead of asking the worker
to guess.
