---
name: loom-specs
description: "Maintain behavior contracts, requirements, scenarios, constraints, and acceptance criteria. Use when intended behavior is still fuzzy, when downstream implementation needs one canonical contract, or when critique and wiki will need a stable statement of what the system is supposed to do."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: spec
---

# loom-specs

Specs own intended behavior.

They turn ambiguity into a durable contract.

## What This Skill Owns

- behavior contracts
- requirements
- scenarios
- acceptance criteria
- explicit constraints that shape implementation

## Use This Skill When

- several implementations are plausible and the intended behavior matters
- acceptance criteria are vague
- a ticket or critique would otherwise keep redefining what "correct" means
- a workflow or capability needs one stable behavioral source

## Do Not Use This Skill When

- you are still only gathering evidence
- you only need execution sequencing
- you are writing a user-facing explanation page

## Good Spec Questions

A strong spec answers:

- what problem is being solved
- what desired behavior is expected
- what constraints matter
- what scenarios matter
- how acceptance should be judged

## Done Means

- the behavior is explicit enough that implementation and critique can reference one contract
- the spec is precise without becoming implementation trivia

## Read In This Order

Read immediately for normal spec creation or review:

1. `references/spec-shape.md` when deciding what belongs in requirements,
   scenarios, constraints, and acceptance.
2. `templates/spec.md` only when creating or substantially reshaping a spec
   record.
