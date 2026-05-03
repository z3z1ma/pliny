---
name: loom-debugging
description: "Run a reproduce-first debug or incident workflow through existing Loom layers. Use when behavior fails, root cause is unknown, or a fix needs reproduction evidence, root-cause preservation, and regression evidence."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-debugging

Debugging routes reproduction, root-cause work, fixes, evidence, and prevention
follow-through into the Loom records that own those facts.

## What This Workflow Coordinates

- reproduce-first bug workflow
- root-cause routing
- fix evidence expectations
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

`reproduce -> localize -> explain -> fix -> evidence -> prevent`

1. capture reproduction steps or current failing behavior as evidence
2. investigate root cause before proposing a fix; create or update research if
   the root cause is not known
3. update or create a spec if intended behavior is ambiguous
4. create or tighten a ticket for the bounded fix
5. choose `local_edit` for a tiny, local, safe fix, or compile a Ralph packet when
   the fix needs fresh context, explicit child write scope, or packetized
   isolation; Ralph packets normally use `verification_posture: test-first`
6. preserve red and green evidence
7. route to critique when risk warrants
8. run retrospective if the lesson should prevent repeated mistakes

## Artifact Routing

| Debug output | Owner |
| --- | --- |
| reproduction steps | evidence |
| root cause investigation | research |
| intended behavior clarification | spec |
| fix execution | ticket plus `local_edit` or Ralph, according to route readiness |
| regression evidence | evidence |
| recurring evidence gap | ticket follow-up or test expectation via retrospective |
| recurring lesson | wiki, research, spec, plan, initiative, constitution, or evidence via retrospective; memory may keep support-only recall or owner-record pointers |

## Done Means

- the failure was reproduced or the inability to reproduce is explicit
- root cause is evidence-backed or still marked unknown
- intended behavior is owned by a spec when needed
- the fix is owned by a ticket and either a reconciled local edit or packetized
  child result, as appropriate
- evidence exists for before and after behavior
- prevention follow-through is explicit

## Read In This Order

Read immediately for debugging work:

1. `references/systematic-debugging.md` when root cause is unknown, time pressure
   makes guessing tempting, or previous fixes failed.
2. `skills/loom-evidence/SKILL.md` when preserving reproduction, red/green
   output, logs, screenshots, or other evidence.

Then read conditionally:

3. `skills/loom-research/SKILL.md` when root cause is unknown or rejected
   hypotheses should remain citable.
4. `skills/loom-specs/SKILL.md` when intended behavior is ambiguous.
5. `skills/loom-tickets/SKILL.md` when creating or tightening the bounded fix
   ticket.
6. `skills/loom-ralph/SKILL.md` when the fix is ready for a packetized
   implementation iteration.
7. `skills/loom-critique/SKILL.md` when the fix or incident carries review
   risk.
