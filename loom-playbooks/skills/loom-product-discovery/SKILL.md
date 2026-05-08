---
name: loom-product-discovery
description: "Shape raw product ideas into Loom owner records. Use when a user brings a vague feature, workflow concept, product direction, improvement idea, PRD request, brainstorming prompt, or not-yet-ticket-ready outcome; route durable truth to initiative, research, spec, plan, or ticket records."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow-coordinator
---

# loom-product-discovery

Product discovery decides what the work should mean before execution hardens it.

This playbook coordinates divergent and convergent idea shaping, then routes the
settled truth into Loom owner layers instead of creating a separate idea ledger.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- raw idea intake and problem pressure checks
- divergent option generation
- convergent option selection
- assumptions, non-goals, and open-question routing
- handoff into initiatives, research, specs, plans, tickets, spike workflows, or wiki

## What This Workflow Does Not Own

- strategic outcome truth; use initiatives
- tradeoffs, assumptions, rejected paths, or evidence synthesis; use research
- intended behavior and acceptance; use specs
- execution decomposition; use plans
- live execution state; use tickets
- accepted explanation; use wiki after owner truth settles

## Use This Skill When

- the user asks to brainstorm, shape, refine, PRD, scope, or turn an idea into work
- the request names a solution but the problem, beneficiary, or value is unclear
- several product directions could satisfy the same rough outcome
- a feature request needs a not-doing list, assumptions, MVP boundary, or open questions
- `loom-drive` cannot safely continue because the objective itself is still fuzzy

## Do Not Use This Skill When

- the behavior contract is already clear enough for a spec or ticket
- the next move is an implementation ticket, debug pass, critique, or ship package
- the question is only technical feasibility; use `loom-spike` or research
- the user is asking for accepted explanation of settled behavior; use wiki

## Discovery Loop

1. State the rough idea in neutral language without accepting the proposed solution
   as the only path.
2. Pressure-check the problem: target user or operator, current pain or workaround,
   why now, success signal, constraints, non-goals, and durability risk.
3. Ask one focused question or a small batch only when the answer would materially
   change the owner record or first tranche.
4. Generate five to eight candidate directions when the space is still open, then
   collapse them into two or three materially different options.
5. Compare options by value, evidence strength, risk, implementation cost,
   reversibility, maintenance burden, and fit with current Loom records.
6. Choose the smallest valuable shape or record why no option is ready.
7. Route durable output to owner layers: initiative for durable objective,
   research for options and assumptions, spec for intended behavior, plan for
   sequencing, ticket for bounded execution, evidence/research for experiment
   results, and wiki only for accepted explanation. Use `loom-spike` as the
   workflow when the next step is an experiment; do not treat it as an owner layer.
8. Record a not-doing list and open questions in the owner record that downstream
   work will read.

## Output Shapes

Choose the lightest owner output or workflow route that makes downstream work safe:

- initiative when the idea becomes a durable outcome with success metrics
- research when options, rejected paths, or assumptions need citable synthesis
- spec when intended behavior or acceptance is now clear enough to contract
- plan when the chosen direction needs multiple ordered execution units
- ticket when the next step is already bounded and ticket-local acceptance is enough
- spike workflow when the next honest step is a prototype, sketch, or feasibility
  probe, with durable results routed to research, evidence, spec, plan, ticket, or
  wiki as appropriate

Do not create a standalone PRD or idea directory as Loom truth. If a one-page
summary is useful, put its durable claims in the owner record that owns them.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "The user already gave the solution, so skip discovery." | A requested solution can hide an untested problem, wrong beneficiary, or over-wide first slice. |
| "Brainstorming can stay in chat." | Rejected options, assumptions, and non-goals become important once downstream tickets depend on them. |
| "A polished one-pager is the source of truth." | Loom owner records own strategy, evidence, behavior, plans, and execution state. |
| "Ask for approval after every phase." | Ask when a material decision needs user judgment; continue under recorded delegated authority when safe. |

## Red Flags

- no target user, operator, system, or maintenance surface is named
- success criteria are vibes, not observable outcomes
- not-doing and non-goals are absent for a broad idea
- the first ticket encodes a solution before the problem is accepted
- open questions that could change scope are hidden in prose
- discovery output becomes a shadow execution ledger

## Verification

- [ ] Problem, beneficiary, current baseline, and smallest valuable shape are explicit or marked blocking.
- [ ] Options, assumptions, rejected paths, and non-goals are routed to the right owner records.
- [ ] Intended behavior is in a spec before reusable acceptance depends on it.
- [ ] The next ticket or plan tranche does not depend on unresolved discovery questions.
- [ ] Wiki is used only for accepted explanation, not proposed product truth.

## Done Means

- the idea has either become owner-record truth or is explicitly blocked/deferred
- downstream execution can cite the relevant initiative, research, spec, plan, or ticket
- material assumptions and non-goals are visible
- no separate product-discovery ledger is carrying canonical truth

## Read In This Order

Read immediately for discovery work:

1. `references/discovery-loop.md` for divergent/convergent idea shaping,
   codebase-grounded discovery, assumption surfacing, not-doing lists, and owner
   routing.
2. the core `loom-initiatives` skill when a durable objective or success metric may
   be needed.
3. the core `loom-research` skill when options, assumptions, or rejected paths need
   citable synthesis.
4. the core `loom-specs` skill when the idea becomes intended behavior.

Then read conditionally:

5. `skills/loom-spike/SKILL.md` when a prototype, sketch, or experiment should
   answer the next question.
6. the core `loom-plans` and `loom-tickets` skills when execution shape becomes clear.
7. the core `loom-wiki` skill only after accepted explanation should persist.
