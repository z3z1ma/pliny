---
name: loom-ralph
description: Managed Loom orchestration skill for Ralph packetized execution: bounded ticket execution through persisted packets, fresh child runs, verification, and ticket-ledger reconciliation. Use when one exact ticket should advance through one bounded fresh-context execution step with explicit scope and write boundaries. Not for local-only edits, critique-first work, or vague multi-ticket execution.
compatibility: Designed for this Markdown-first Loom repository. Assumes repository-local scripts, canonical Markdown records, and harness-agnostic child launches resolved through `.loom/harness.md` profiles, harness self-discovery, or operator guidance.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: orchestration
---

# loom-ralph

Ralph is the first-class Loom orchestration skill for bounded execution.

Use Ralph when long-horizon work should advance through one durable, packetized, fresh-context execution step without collapsing execution, review, and explanation into one transcript.

Tickets remain the durable source of live execution truth before, during, and after the child run.

## Use This Skill When

- one exact ticket should advance through one bounded fresh-context execution step
- the parent needs a packetized contract rather than a long transcript handoff
- write boundaries and scope need to be explicit before execution

## Do Not Use This Skill When

- the work is only local reading, diagnosis, or record maintenance
- the next step is primarily critique or docs rather than execution
- the ticket is too vague to bind one bounded execution step safely

## What This Skill Governs

- Ralph packet artifacts
- execution packets that target tickets
- the parent-side orchestration steps around a Ralph child run
- reconciliation of Ralph outcomes back into ticket truth

## Ralph Is Distinct From Neighboring Loom Layers

- plans remain the execution-strategy layer
- tickets remain the live execution ledger
- critique remains the durable review layer
- docs remain the authoritative explanatory layer after accepted reality is known
- Ralph orchestrates bounded execution over those artifacts without replacing them

## Default Ralph Posture

- prefer fresh-context iterations over transcript accumulation
- run one bounded iteration at a time
- make the durable packet detailed enough to stand on its own between launches
- treat the bound ticket as the authoritative execution ledger
- require explicit continue, stop, blocked, or escalate behavior
- ground continuation decisions in ticket truth, verification evidence, critique, and acceptance context rather than model confidence alone

## Before You Launch

1. read the current ticket and governing context first
2. make sure the ticket is strong enough to support one bounded iteration
3. resolve scope whenever ownership is not already explicit
4. choose packet mode, style, and write boundary deliberately

## Execution Playbook

1. compile and persist the packet before child execution
2. inspect the packet contract enough to confirm target, scope, and write set are correct
3. resolve the harness invocation: check `.loom/harness.md` for a matching profile, then try harness self-discovery, then ask the operator (see `references/harness-invocation.md`)
4. launch the child in a fresh context using the resolved command
4. capture durable run evidence after the child returns
5. validate affected records and graph integrity
6. reconcile the result back into ticket truth immediately so the packet does not become shadow state
7. decide continue, stop, blocked, or escalate based on durable evidence rather than optimism

## Child Expectations

The child should:

1. read the packet as the local execution contract
2. treat records as context and follow the already-active authority hierarchy plus the local skill and packet contract
3. mutate only the allowed write set if execution authority is granted
4. report verification performed
5. return a continue, stop, blocked, or escalate recommendation

If a child run returns without durable ticket activity, the run is incomplete from a Loom point of view even if local file changes exist.

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/ralph.py packet`: use before launch to scaffold the Ralph contract under `.loom/runs/ralph/`
- `scripts/ralph.py verify`: use after the run when the outcome or supporting checks should become durable evidence

## What Good Looks Like

- one ticket clearly owns the execution step
- the packet is bounded, explicit, and reusable as a durable artifact
- the child stayed inside scope and produced verification evidence
- the ticket absorbed the result truthfully after the run

## Failure Conditions

Treat the Ralph run as failed or incomplete when:

- the child wrote outside the allowed boundary
- the child left no durable ticket change despite claiming meaningful progress
- the child omitted verification or outcome classification
- the packet is stale enough that the parent cannot trust the run contract anymore
- the child tried to treat Ralph artifacts as the ledger instead of the ticket

## Done Means

- one bounded execution step completed or blocked truthfully
- the packet, evidence, and ticket reconciliation all tell the same story
- verification and outcome classification are explicit
- frontmatter and downstream links are explicit enough for later workspace validation

## Read In This Order

1. `references/packets.md`
2. `references/scripts.md`
3. `references/harness-invocation.md`
4. `references/schema-ralph.md`
5. `references/examples.md`

## References

- `references/schema-ralph.md`
- `references/packets.md`
- `references/scripts.md`
- `references/harness-invocation.md`
- `references/examples.md`
