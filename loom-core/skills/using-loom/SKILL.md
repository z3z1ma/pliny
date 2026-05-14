---
name: using-loom
description: "Always activate at session start in Loom workspaces before any response or action, unless an adapter has already preloaded this doctrine and references."
---

# using-loom

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply, you ABSOLUTELY MUST
invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not optional. This is not a style preference. This is how Loom prevents
silent scope invention, retroactive tickets, unbounded worker prompts, unsupported
closure claims, and lost recovery context.
</EXTREMELY-IMPORTANT>

Loom is a human-agent control plane for AI-driven software engineering.

Loom works through two connected loops.

The outer loop keeps the agent and operator shaping the work until the next move is
understood, bounded, and routed into the right durable surface. Those surfaces are
Markdown records written for humans and agents, with directory names for `find` and
stable words, headings, labels, IDs, and refs for `grep`.

The inner loop uses Ralph packets to execute bounded ticket slices, run workers,
and perform substantive audit review before records rely on claims.
Packets carry enough source-linked context, scope, constraints, stop conditions,
and evidence expectations for the worker to act without relying on chat history,
while keeping the relevant records truthful as it works.

Use the Loom surfaces to preserve the shaped work, bounded execution, evidence,
audit, and reusable knowledge that future agents need.

## Loop Order

Loom routing comes first. Use workflow-specific skills only after this doctrine
has established whether the work is still outer-loop shaping or ready for bounded
execution.

Activation is part of routing. If there is any material chance a Loom skill or
surface applies to the operator's message, invoke the relevant skill before
responding, asking clarifying questions, code exploration, quick checks, editing,
creating tickets, or launching Ralph. The skill may confirm that a lighter path is
enough; skipping the check because the work feels obvious is not allowed.

The default sequence is:

```text
shape with the operator -> route durable truth -> slice executable work -> execute
ticket slices through Ralph packets -> preserve evidence -> audit claims ->
reconcile records
```

When product intent, success criteria, quality bar, scope, evidence posture, or
ticket boundary is unclear, stay in the outer loop. A workflow-specific skill can
add pressure, but it still moves through Loom surfaces and the same loop order.
When it routes to another Loom skill, follow that skill's procedure and guidance
completely.

Ambiguity defaults to shaping, not implementation. Treat an ask as ready for
execution only when the operator's desired outcome, scope boundary, relevant
constraints, success criteria, evidence posture, and material non-goals are clear
enough that an agent can act without silently choosing product direction. Anything
less stays in the outer loop.

The outer loop is where Loom does front-loaded engineering judgment: selecting a
direction, drawing boundaries, identifying system seams, data models, and state
relationships, and deciding what would make the result coherent rather than merely
functional. These are not implementation details to discover after coding starts.
If those choices are missing, unexamined, or silently inferred, execution is not
ready.

Do not turn a fuzzy request into a ticket, Ralph packet, or patch just to make
progress. First inspect what the repository and Loom records can answer, pinpoint
the material direction, boundary, system-shape, state, or proof ambiguity with the
operator, and route the resolved truth into the owning Loom surface before
execution.

## Session Start

At the start of a Loom session, read this skill and all references below unless an
adapter has already preloaded the same doctrine with clear source markers. Do not
spend context twice when the doctrine is already present.

Read in this order:

1. `references/how-loom-thinks.md`
2. `references/activation-discipline.md`
3. `references/directory-structure.md`
4. `references/shaping-with-humans.md`
5. `references/delegating-to-workers.md`
6. `references/proving-the-work.md`
7. `references/staying-safe.md`

After that, load active `Type: Knowledge Preference` records from
`.loom/knowledge/` when that directory exists. Retrieve other knowledge only when
the task, path, tool, error, ticket, or domain makes it relevant.

Then use the relevant Loom skill for the surface you are touching. If multiple
skills may apply, prefer the owning record skill first, then any workflow playbook
that adds task-shaped pressure.

## Loom Surfaces

Loom records are Markdown files designed to be found, read, and connected with
ordinary `find` and `grep` workflows.

The Loom surfaces are:

- constitution: durable project judgment, policy, principles, constraints, ADRs,
  and roadmap direction
- tickets: the fundamental work unit where executable change is scoped, driven,
  and tracked
- research: investigations, tradeoffs, synthesis, rejected paths, and conclusions
- specs: intended behavior, requirements, scenarios, and interfaces
- plans: operator-shaped strategy for complex changes that exceed one bounded
  ticket, including decomposition, dependencies, validation, and recovery
- evidence: observed facts, outputs, reproductions, screenshots, logs, and
  validation
- audit: adversarial review findings and verdicts from Ralph review runs
- knowledge: preferences, procedures, accepted explanation, reusable
  understanding, and retrieval cues
- packets: bounded contracts for worker handoff

Retrospective is a promotion pass after significant work: decide what learning
should move into the right surface instead of leaving it in chat. Use
`loom-retrospective` for that pass when the work is non-trivial or prevention
follow-up may matter.

## Working Posture

Ask:

- What must be shaped with the operator before execution is honest?
- Is the operator's ask concrete enough, or am I inferring scope, system-shape,
  data-model, state-model, or coherence choices?
- What ambiguity would make a different implementation correct?
- What surface owns the truth I am about to depend on or change?
- Is this still a human-shaped outer-loop problem, or is it safe to execute?
- What is the next smallest ticket-ready slice, and what makes it complete?
- What Ralph packet bounds this worker handoff?
- What evidence or audit would make the claim honest?
- What knowledge should future agents load, retrieve, or not have to rediscover?

Tiny, obvious, low-risk work can stay light. Create or update records when they
materially improve future recovery, judgment, execution, review, or reuse.

Red flags that mean stop and route through the relevant skill instead of acting
from habit:

| Rationalization | Loom reality |
| --- | --- |
| "this is simple" | Simple work still needs the right skill check when a Loom surface might own the next move. |
| "this is just a small change" | Small work can stay light only after the right surface is obvious and risk is low. |
| "I need more context first" | Skill invocation comes before clarifying questions, code exploration, or quick checks. |
| "I need to inspect first" | If inspection is part of a likely Loom workflow, invoke that workflow skill first. |
| "I'll create the ticket after" | Ticket-worthy work needs the ticket before execution, not as a retroactive wrapper. |
| "I'll ask the worker directly" | Worker handoff needs a Ralph packet before launch. |
| "evidence can wait" | Evidence posture is part of honest execution, not cleanup. |
| "audit is overkill" | Risk decides audit posture; convenience does not. |
| "I remember the skill" | Skill text evolves. Load the current relevant skill. |
| "I'll just do this one thing first" | One un-routed action is enough to lose the graph. Check the skill first. |

## Done Means

This skill is complete when the doctrine is loaded and the next move is routed to
the right surface or skill.
