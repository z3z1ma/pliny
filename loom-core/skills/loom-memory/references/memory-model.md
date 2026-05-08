# Memory Model

Memory is a support layer for continuity, not a canonical owner layer.

It stores lightweight recall that is useful to an agent but too local,
subjective, provisional, or decaying to belong in constitution, initiatives,
research, specs, plans, tickets, evidence, critique, or wiki.

## Optionality

Optional does not mean worthless.

Optional means Loom must remain correct if memory is missing, stale, or deleted.
The canonical graph owns project truth. Memory reduces rediscovery cost and helps
operators find the right owner record faster.

## The Memory Fit Test

Use memory only when all of these are true:

- the fact helps future orientation, retrieval, or collaboration
- the fact does not define intended behavior, strategy, live work, evidence,
  accepted explanation, or policy
- the fact can safely decay, be pruned, or be replaced by a pointer
- if the fact becomes important, there is an obvious owner layer to promote it to

If deleting the item would make the durable project story false, incomplete, or
unsafe, it is not memory.

## Useful Memory Content

- retrieval cues: which records, directories, aliases, or recurring terms help a
  future operator start in the right place
- hot context: small current pointers or cautions that should age quickly
- preferences: user or operator collaboration preferences that influence how to
  communicate but do not define project policy
- entities: compact descriptions of people, systems, packages, services, or
  recurring topics that help search and orientation
- support observations: dated notes that may be useful later but are not evidence
  for acceptance, critique, or claims
- support reminders: small reminders that are not yet scoped Loom work

## What Belongs Elsewhere

- Fact type: durable identity, principles, hard constraints, accepted decisions
  - Owner: constitution
- Fact type: strategic outcome, success metric, delegated objective
  - Owner: initiative
- Fact type: investigation result, tradeoff, rejected option, evidence synthesis
  - Owner: research
- Fact type: intended behavior, requirement, acceptance criterion
  - Owner: spec
- Fact type: sequencing, rollout strategy, dependency order
  - Owner: plan
- Fact type: live state, blocker, next move, acceptance disposition, closure
  - Owner: ticket
- Fact type: observed artifact, validation output, reproduction, screenshot, log
  - Owner: evidence
- Fact type: adversarial finding, verdict, severity, required follow-up
  - Owner: critique
- Fact type: accepted explanation, workflow knowledge, troubleshooting pattern
  - Owner: wiki
- Fact type: bounded child read/write/stop/output contract
  - Owner: packet

Memory may link to any of these, but the owner record wins when there is a
disagreement.

## Common Files

- `hot-memory.md` — small, current, high-signal context and pointers
- `observations.md` — dated support observations, not evidence
- `entities.md` — compact registry of people, systems, aliases, or recurring topics
- `action-items.md` — support reminders, not canonical ticket work

Projects may add a small domain-specific file when it has a real retrieval job,
but avoid creating a taxonomy that future agents must maintain before memory is
useful.

## Domains

The default domains are:

- `system/` for project or agent-operation context that is not canonical truth
- `user/` for collaborator preferences or recurring user-specific context that is
  appropriate to store in the repository

Do not put private, sensitive, or credential-like data in memory. It is a normal
workspace file surface.

## Promotion And Demotion

Promote memory when it stops being support-only:

- repeated explanation -> wiki
- scoped work, blocker, acceptance state, or live execution progress -> ticket
- observed output supporting or challenging a claim -> evidence
- intended behavior or acceptance rule -> spec
- investigation conclusion or rejected path -> research
- sequencing or dependency strategy -> plan
- strategic objective or success metric -> initiative
- durable principle, hard constraint, or accepted decision -> constitution

Link, stale-mark, demote, or prune when memory has stopped being the best shape:

- canonical truth now exists and memory only duplicates it
- hot context is no longer hot
- an observation is too stale to help retrieval
- an action-item reminder became ticket work or no longer matters

Use this order of preference:

1. leave the item alone if it is still current, support-only, and useful
2. replace detail with a short pointer when an owner record now carries the truth
3. mark the item stale if it is historically useful but no longer current
4. promote it before relying on it for project truth, acceptance, evidence,
   intended behavior, or accepted explanation
5. prune it when it is low-signal, unverifiable, obsolete, or redundant

Pruning is safe only because memory is optional in the correctness sense. If
removing the item would make the canonical graph false, incomplete, or unsafe,
do not prune it as memory; move or restate the claim in the owning layer first.

## Examples

Good memory:

- "When touching install docs, start with `initiative:loom-install-experience`."
- "The maintainer prefers concise final summaries unless the work is complex."
- "`Ralph` is often discussed as the bounded implementation handoff loop; see
  using-Loom references for authority."

Not memory:

- "Ticket X is blocked" -> ticket
- "Memory must be canonical" -> constitution or spec, and probably a policy debate
- "Test output proves ACC-001" -> evidence
- "The workflow now means X" -> spec or wiki, depending on whether it is behavior
  or accepted explanation

## Size Rule

Keep hot memory small.

If it grows large, it stops being hot memory and should be split, promoted, or
pruned.
