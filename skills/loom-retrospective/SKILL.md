---
name: loom-retrospective
description: "Run Loom's compounding pass across existing owner layers. Use when a non-trivial ticket or initiative is closing, critique surfaced stable lessons, the same question has been re-derived, or accepted learning should be promoted into wiki, research, spec, plan, initiative, constitution, evidence, or memory."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-retrospective

Retrospective is Loom's compounding workflow.

It assimilates what was learned during a ticket, initiative, critique, spike,
debugging pass, or recent work slice into the existing owner layers.

It promotes learning into the records that already own that kind of knowledge.
This skill owns retrospective workflow mechanics; shared record grammar only
reminds operators that retrospective is a workflow route, not a new record kind.

## What This Workflow Coordinates

- wiki promotion for accepted explanations and workflows
- research preservation for durable investigation results, rejected options, and
  null results
- spec updates for clarified intended behavior
- plan updates for changed sequencing
- initiative updates for changed strategic framing
- constitution updates for changed principles, constraints, decisions, or roadmap
  direction
- evidence preservation for observed artifacts, challenged observations, or
  validation artifacts
- memory updates for support-only continuity, retrieval cues, preferences, or
  reminders

## Use This Skill When

- a non-trivial ticket is closing or entering acceptance review
- an initiative is closing or materially changing direction
- critique surfaced lessons that should prevent repeated mistakes
- a spike, debugging pass, or code map produced durable learning
- the same question has been answered from transcript context more than once
- accepted learning needs promotion into its owning layer

## Do Not Use This Skill When

- there is no durable learning to promote
- the work is still unsettled and belongs in research, spec, critique, or ticket
  execution first
- you are trying to create a second progress ledger outside tickets
- a small local cleanup has no reusable lesson

## Promotion Routing

- accepted explanations and workflows -> `loom-wiki`
- durable investigation results, rejected options, and null results -> `loom-research`
- clarified intended behavior -> `loom-specs`
- changed sequencing -> `loom-plans`
- changed strategic framing -> `loom-initiatives`
- changed principles, constraints, decisions, or roadmap direction -> `loom-constitution`
- observed artifacts, challenged observations, or validation artifacts -> `loom-evidence`
- missing evidence that still needs work -> ticket follow-up or test expectation
- support-only recall, retrieval cues, preferences, or reminders -> `loom-memory`

## Retrospective Loop

Use the loop `observe -> distill -> promote -> prevent`.

Observe concrete signals from ticket journals, packet outputs, critique findings,
evidence records, changed owner records, and recurring questions that had to be
reconstructed.

Distill durable lessons separately from one-time execution detail, then promote
each accepted lesson to the owner layer that can maintain it.

Prevent repeated mistakes by choosing exactly one prevention artifact when
practical:

- behavior ambiguity -> spec
- missed test case or evidence gap -> evidence when an observed artifact exists,
  or a follow-up ticket/test expectation when the gap is future work
- bad architectural choice -> constitution decision
- recurring operator confusion -> wiki workflow or reference page
- repeated implementation pitfall -> research null result or wiki troubleshooting
- repeated project-local technique -> project-local skill
- support-only reminder -> memory

If there is nothing durable to promote, say so. Do not invent artifacts to look
productive.

## Default Procedure

1. read the ticket, initiative, critique, evidence, packet, or work slice being
   assimilated
2. list durable lessons separately from one-time execution details
3. route each lesson to exactly one owner layer where practical
4. update owner records only when the lesson is accepted enough to preserve
5. update the ticket or initiative disposition to say what was promoted, deferred,
   or intentionally not promoted
6. when memory held support context for the work, leave useful current cues,
   replace promoted detail with owner-record pointers, mark stale historical cues,
   or prune obsolete reminders

## Done Means

- durable learning moved to the owner layer that can maintain it
- no retrospective-only ledger was created
- memory was not left as the only source for promoted truth
- the ticket or initiative truth says what follow-through happened or was deferred
- repeated mistakes now have one prevention artifact, or the absence of durable
  follow-through is explicit

## Read In This Order

Read immediately for retrospective work:

1. `skills/loom-records/references/retrospective.md` when checking the shared
   grammar that retrospective creates no new canonical record layer.
2. `skills/loom-tickets/SKILL.md` when ticket acceptance, closure, or follow-up
   disposition needs updating.

Then read conditionally:

3. `skills/loom-wiki/SKILL.md` when accepted explanation should become reusable.
4. `skills/loom-research/SKILL.md` when findings, rejected options, or null
   results should remain citable.
5. `skills/loom-specs/SKILL.md`, `skills/loom-plans/SKILL.md`,
   `skills/loom-initiatives/SKILL.md`, or `skills/loom-constitution/SKILL.md`
   when the lesson changes the owner truth those layers maintain.
6. `skills/loom-evidence/SKILL.md` when observed artifacts, challenged
   observations, or validation artifacts need preservation.
