---
name: loom-constitution
description: "Maintain durable project identity, principles, constraints, strategic direction, decision records, and roadmap records. Use when the work changes what the project is, what it values, what it refuses, or what long-lived direction it is committing to beyond current execution."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: constitution
  protocol_version: "2.0"
---

# loom-constitution

Constitution is Loom's highest project-facing owner layer.

Use it when the project needs to remember what it is and how it should judge future work.

## What This Skill Owns

- `constitution:main`
- constitutional decision records (ADRs)
- roadmap records
- durable principles and constraints

Decision records and roadmap records are first-class constitutional artifacts, not subtypes tucked under the main constitution file. Decision records are Loom's ADR layer: they capture durable architectural and policy choices and their rejected alternatives, so future agents inherit precedent instead of re-deriving it. Roadmap records live in the same subsystem because a roadmap is strategic direction made durable — sequencing at the policy layer, not sequencing at the execution layer.

## Use This Skill When

- a principle should become durable policy
- an architectural constraint should become explicit
- a major choice should outlive the current ticket or plan
- the project's strategic direction changed materially
- a roadmap theme or milestone sequence deserves durable expression
- an architectural or policy choice should be citable later as precedent (write a decision record)

## Do Not Use This Skill When

- you are tracking live progress
- you are describing one bounded implementation step
- the change belongs to a spec, plan, or ticket instead of durable policy
- you only need accepted explanation rather than policy authority

## Constitutional Posture

Good constitutional writing is:

- durable
- explicit
- constraining
- useful as a judgment frame
- not confused with day-to-day execution

A constitutional record should help a future agent decide, not merely admire the prose.

## Read Constitution Before Deciding

Before making a non-trivial architectural or policy choice, grep the constitution subsystem first. Decision records are precedent; the roadmap is strategic sequencing; `constitution:main` is current framing. A choice that re-derives a prior decision without citing it wastes work and risks contradicting accepted policy.

Useful starting queries:

- `rg -n '^id:' .loom/constitution` — list every constitutional record
- `find .loom/constitution/decisions -name '*.md' | sort` — scan precedent by filename
- `rg -n '<topic>' .loom/constitution` — check whether this topic already has policy

## Default Procedure

1. decide whether the work belongs in `constitution:main`, a decision record, or a roadmap record
2. check whether prior constitutional records already cover the topic before creating a new one
3. copy the right template
4. fill in the policy truth, not just abstract philosophy
5. link downstream work where useful, except for `constitution:main`, which usually stays link-light
6. when writing a decision record, state the rejected alternatives and their reasons so the record carries precedent value
7. reconcile any plan/spec/wiki pages that are now out of date because the constitutional frame changed

## Done Means

- the durable principle or direction is explicit
- downstream work can now inherit the judgment
- the record reads as policy, not as a ticket
- a fresh agent would know how this should influence later work
- a decision record names its rejected alternatives and the reason each was rejected

## Read In This Order

1. `references/record-families.md`
2. `references/writing-standard.md`
3. `templates/constitution.md`
4. `templates/decision.md`
5. `templates/roadmap.md`
