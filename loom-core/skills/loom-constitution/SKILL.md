---
name: loom-constitution
description: "Maintain durable project identity and constraints. Use when architecture policy, principles, ADRs/decision records, roadmap direction or roadmap records, hard constraints, citable decisions, or long-lived project rules must change."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: owner-layer
  owns_layer: constitution
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

## Roadmap Boundary

Roadmaps express durable strategic direction and policy-level milestones.

They do not replace initiative success metrics, plan strategy milestones, or
ticket execution state. If a roadmap starts tracking day-to-day progress, route
that detail down into initiatives, plans, or tickets.

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

## Common Rationalizations

- Rationalization: "This feels important, so it belongs in the constitution."
  - Reality: Constitution owns durable policy and constraints, not every important fact.
- Rationalization: "The decision is obvious, so rejected options are unnecessary."
  - Reality: Rejected options are what make decision records useful precedent.
- Rationalization: "A roadmap can track project progress."
  - Reality: Roadmaps express durable direction; initiatives, plans, and tickets own execution detail.
- Rationalization: "A wiki page can serve as policy."
  - Reality: Wiki explains accepted understanding. Constitution owns policy authority.

## Red Flags

- constitutional prose is aspirational but not constraining
- decision record lacks alternatives, consequences, or downstream reconciliation
- roadmap lists ticket tasks instead of policy-level direction
- policy change silently contradicts existing constitution records
- specs, plans, or wiki pages remain stale after a constitutional change

## Verification

- [ ] Existing constitutional records were checked for precedent.
- [ ] The change belongs to policy, durable direction, or citable decision truth.
- [ ] Decision records name accepted choice, rejected alternatives, and consequences.
- [ ] Downstream records that conflict with the new frame were reconciled or marked pending.

## Done Means

- the durable principle or direction is explicit
- downstream work can now inherit the judgment
- the record reads as policy, not as a ticket
- a fresh agent would know how this should influence later work
- a decision record names its rejected alternatives and the reason each was rejected

## Read In This Order

Read immediately for constitutional changes:

1. `references/record-families.md` when deciding whether the change belongs in
   `constitution:main`, a decision record, or a roadmap.
2. `references/writing-standard.md` before accepting durable policy language or
   when the prose risks becoming vague philosophy.

Then read conditionally:

3. `templates/constitution.md` only when creating or reshaping
   `constitution:main`.
4. `templates/decision.md` only when recording a citable architectural or
   policy choice with rejected alternatives.
5. `templates/roadmap.md` only when durable strategic sequencing belongs above
   plans.
