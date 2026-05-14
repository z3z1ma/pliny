# Activation Discipline

Activation is the first behavior Loom needs from an agent.

If you think there is even a 1% chance a skill might apply, you ABSOLUTELY MUST
invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

## First-Action Loop

Before the first response or action for a user message, run this loop:

1. Confirm this doctrine is loaded. If it is already loaded with clear source
   markers, do not spend context reloading it.
2. Ask which Loom surface or skill could materially own the next move.
3. If any material chance exists, invoke the relevant Loom skill before responding,
   before asking clarifying questions, before code exploration, before quick checks,
   before editing files, before creating tickets, and before launching Ralph.
4. If the skill proves it is not the right route, return to Loom routing and choose
   the next surface or proceed lightly when no durable Loom work is needed.
5. Follow the active skill completely when it routes to another Loom skill. A
   workflow-specific skill does not shorten record-skill procedure.

## Priority

Use this priority when more than one skill may apply:

1. `using-loom` doctrine and safety.
2. The owning record skill: constitution, specs, plans, tickets, research,
   evidence, audit, knowledge, or Ralph packets.
3. A workflow playbook, such as debugging, TDD, UI work, review, migration,
   security, performance, release, or branch finish.

Record skills own durable truth. Playbooks add pressure to reach the right record,
evidence, packet, or audit route.

## Red Flags

These thoughts mean the agent is rationalizing around Loom:

| Thought | Reality |
| --- | --- |
| "This is simple." | Simple work still needs the right skill check when a Loom surface might own the next move. |
| "This is just a small change." | Tiny, obvious, low-risk work can stay light only after routing shows no durable surface is needed. |
| "I need more context first." | Skill invocation comes before clarifying questions, code exploration, or quick checks. |
| "I need to inspect first." | If inspection is part of a likely Loom workflow, load that skill before inspection. |
| "I can ask one quick clarifying question first." | If a shaping or record skill might apply, invoke it before the question. |
| "I'll create the ticket after I understand the fix." | Ticket-worthy work needs scoped acceptance before implementation. |
| "I'll just send the worker the instructions directly." | A worker run that affects Loom state needs a Ralph packet on disk first. |
| "Evidence can wait until the end." | Evidence posture is part of execution readiness and closure honesty. |
| "Audit is overkill." | Audit posture follows claim risk, not convenience. |
| "I know this skill already." | Skill text changes; load the current version. |
| "I'll just do this one thing first." | One un-routed action is enough to lose the graph. Check the skill first. |
| "This feels faster." | Fast unbounded work is how Loom loses the recovery graph. |
