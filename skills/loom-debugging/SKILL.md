---
name: loom-debugging
description: "Run a reproduce-first debug or incident workflow through existing Loom layers. Use when behavior fails, root cause is unknown, or a fix needs reproduction evidence, root-cause preservation, and regression proof."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: workflow
  protocol_version: "2.0"
---

# loom-debugging

Debugging is a workflow over existing Loom layers.

It does not create a new canonical layer.

## What This Skill Owns

- reproduce-first bug workflow
- root-cause routing
- fix proof expectations
- prevention handoff into retrospective

## Use This Skill When

- there is a failing behavior or incident
- the root cause is unknown
- intended behavior is ambiguous
- a fix needs regression evidence before acceptance

## Do Not Use This Skill When

- the work is a normal feature with clear acceptance
- the failure cannot be reproduced or observed yet and the only need is intake
- the next step is already a narrow ready ticket with evidence

## Default Procedure

Follow:

`reproduce -> localize -> explain -> fix -> prove -> prevent`

1. capture reproduction steps or current failing behavior as evidence
2. create or update research if the root cause is not known
3. update or create a spec if intended behavior is ambiguous
4. create or tighten a ticket for the bounded fix
5. compile a Ralph packet, normally with `verification_posture: test-first`
6. preserve red and green evidence
7. route to critique when risk warrants
8. run retrospective if the lesson should prevent repeated mistakes

## Artifact Routing

| Debug output | Owner |
| --- | --- |
| reproduction steps | evidence |
| root cause investigation | research |
| intended behavior clarification | spec |
| fix execution | ticket and Ralph |
| regression proof | evidence |
| recurring lesson | wiki, research, spec, or constitution via retrospective |

## Done Means

- the failure was reproduced or the inability to reproduce is explicit
- root cause is evidence-backed or still marked unknown
- intended behavior is owned by a spec when needed
- the fix is owned by a ticket and packet
- proof exists for before and after behavior
- prevention follow-through is explicit

## Read In This Order

1. `skills/loom-records/templates/evidence.md`
2. `skills/loom-research/SKILL.md`
3. `skills/loom-specs/SKILL.md`
4. `skills/loom-tickets/SKILL.md`
5. `skills/loom-ralph/SKILL.md`
6. `skills/loom-critique/SKILL.md`
