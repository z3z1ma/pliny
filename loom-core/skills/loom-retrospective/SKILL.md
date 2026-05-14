---
name: loom-retrospective
description: "Use after significant completed or reviewed work when durable lessons, prevention notes, follow-up routing, or reusable knowledge should survive the session."
---

# loom-retrospective

Retrospective is Loom's promotion and prevention pass.

It reviews significant work after implementation, audit, investigation, launch, bug
fixing, or repeated friction and preserves reusable lessons.

Retrospective records follow-through in the existing surface that can carry each
durable lesson.

## Use This Skill When

Use this skill when:

- a meaningful ticket is closing or moving through final review
- an audit, Ralph packet, research pass, bug fix, spike, migration, or launch
  produced reusable learning
- the same explanation, mistake, question, or operator correction has appeared more
  than once
- a prevention note, follow-up ticket, evidence record, or knowledge record may
  stop repeated work
- a significant work thread is ending and the graph should preserve what matters

Skip retrospective when there is no durable lesson, prevention need, or reusable
context to preserve.

## Dispatch

If running a retrospective pass:

- read `references/promotion-and-prevention.md`
- inspect the work being closed or assimilated: ticket, plan, research, audit,
  evidence, packet output, diff, or related records
- separate durable lessons from one-time execution detail
- route each lesson to the surface that can carry it
- use the owning skill before changing specs, plans, constitution, or research
  synthesis; pause for operator authority when the lesson changes intended
  behavior, strategy, durable judgment, or conclusions
- update the originating record when follow-through should be visible there

If only checking whether retrospective is needed:

- inspect the work record and evidence or audit state
- say whether there is durable learning to promote, prevention follow-up to create,
  or no retrospective work needed

## Retrospective Loop

Use this loop:

```text
observe -> distill -> promote -> prevent
```

Observe concrete signals from records, evidence, audit findings, packet output,
changed files, repeated questions, and operator corrections.

Distill durable lessons separately from local execution details.

Promote accepted lessons into existing Loom surfaces through the procedure and
authority gates of the surface that owns the truth.

Prevent repeated mistakes by choosing a useful follow-through artifact or recording
that no durable action is needed.

## Promotion Routes

Common routes:

- accepted explanation, preference, procedure, troubleshooting pattern, codebase
  atlas, entity note, or retrieval cue -> `loom-knowledge`
- durable investigation result, tradeoff, rejected option, or null result ->
  `loom-research`
- clarified intended behavior, interface expectation, requirement, scenario, or
  invariant -> specs
- changed strategy, decomposition, sequencing, or recovery route -> `loom-plans`
- durable project judgment, principle, constraint, decision, or roadmap direction
  -> `loom-constitution`
- observed artifact, validation output, reproduction, screenshot, log, scan, or
  command result -> `loom-evidence`
- executable follow-up work -> `loom-tickets`
- Ralph-backed challenge, risk review, missing-evidence concern, or closure doubt
  -> `loom-audit`

Knowledge is the usual home for reusable explanations and prevention notes. Use
other surfaces when the lesson is not knowledge-shaped.

## Prevention Routes

When work revealed a repeated mistake or likely future trap, choose the smallest
useful prevention route:

- knowledge for reusable procedure, troubleshooting, preference, or retrieval cue
- evidence for an observation future agents should cite
- research for a rejected path, null result, or tradeoff that should not be
  repeated
- specs for clarified intended behavior, requirements, scenarios, or interfaces
- plans for sequencing or migration recovery lessons
- constitution for durable judgment or precedent
- tickets for concrete follow-up work
- audit for unresolved risk or unsupported closure claims

If no prevention artifact is useful, say so in the originating record or final
summary when that improves recovery.

## Originating Record Updates

Retrospective often starts from a ticket, plan, research record, audit, or packet
output.

Update the originating record when future continuation or closure would be worse
without the note. Good updates include:

- what was promoted
- what follow-up was created
- what was intentionally not promoted
- what remains blocked, risky, or unverified
- which records now carry the durable lesson

The graph should show follow-through in the records that already matter.

## Done Means

Retrospective work is done when:

- durable lessons are separated from one-time execution detail
- accepted lessons are promoted into existing Loom surfaces
- high-authority promotions used the owning skill and required operator authority
  when they changed intended behavior, strategy, durable judgment, or conclusions
- prevention follow-up exists where it helps
- the originating record says what happened when that improves recovery or closure
- no reusable lesson remains only in chat, packet output, or a hard-to-find journal
- follow-through is visible in existing surfaces
