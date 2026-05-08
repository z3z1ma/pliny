---
name: loom-simplification
description: "Run behavior-preserving simplification. Use when code works but is harder to read, maintain, review, or extend than needed; when AI artifacts, speculative helpers, dead code, unclear names, or excessive abstraction accumulate; route behavior preservation to evidence and tickets."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-simplification

Simplification removes unnecessary complexity without changing behavior.

This playbook coordinates scoped cleanup, behavior preservation, evidence, and
review so cleanup does not become hidden feature work or architecture migration.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- behavior-preserving cleanup scope
- Chesterton's Fence checks before deletion or reshaping
- dead-code, naming, duplication, and abstraction cleanup
- test/evidence selection for unchanged behavior
- escalation to architecture, migration, spec, or tickets when cleanup is not simple

## What This Workflow Does Not Own

- intended behavior changes; use specs and tickets
- broad seam, API, or module-boundary redesign; use `loom-architecture`
- old-path replacement and removal lifecycle; use `loom-migration`
- live execution, acceptance, or closure; use tickets
- behavior-preservation evidence; use evidence
- final review verdicts; use critique

## Use This Skill When

- code works but is harder to understand or maintain than it needs to be
- review feedback asks for clarity, smaller scope, fewer helpers, or less cleverness
- AI-generated scaffolding, speculative abstraction, duplication, or dead code remains
- names, branches, or control flow obscure existing behavior
- cleanup should be behavior-preserving and independently reviewable

## Do Not Use This Skill When

- the desired outcome changes runtime behavior or product behavior
- the cleanup requires a new architecture seam, adapter, or API contract
- the old path has consumers that need migration or deprecation
- behavior preservation cannot be checked and the risk is material
- the ticket bundles simplification with feature work without explicit scope

## Default Procedure

1. Read the owning ticket, relevant specs, current code, tests, and recent context
   that explain why the code exists.
2. State the behavior that must not change and the simplification target: dead
   code, duplication, naming, control flow, abstraction, test clarity, or dependency
   pruning.
3. Apply Chesterton's Fence: identify responsibilities, callers, edge cases,
   tests, data dependencies, and historical or compatibility reasons before
   deleting or reshaping code.
4. Declare a narrow write boundary and simplify one concept at a time. Keep feature
   work and broad refactors out unless the ticket explicitly scopes them.
5. Prefer deleting unused code, inlining needless indirection, clarifying names,
   reducing branches, and matching project conventions over inventing new helpers.
6. Run behavior-preservation checks after each meaningful simplification when
   practical. Preserve evidence when acceptance or future critique needs it.
7. Escalate to `loom-architecture`, `loom-migration`, specs, or plans when the
   simplification reveals a seam, consumer movement, behavior ambiguity, or ordered
   rollout.
8. Run critique when the cleanup is non-trivial, broad, or likely to hide behavior
   changes.

## Simplification Checks

Good simplification usually makes at least one of these better:

- fewer concepts needed to understand the same behavior
- clearer names aligned with domain language
- less indirection without losing a real seam
- smaller public surface or helper set
- fewer branches, states, or special cases
- easier tests at the same or deeper behavior seam
- deleted dead code with reconciled references

## Common Rationalizations

- Rationalization: "This is just cleanup, so tests are optional."
  Reality: Behavior-preserving work still needs evidence that behavior stayed the
  same or an explicit evidence limit.
- Rationalization: "I do not understand this code, so it is overcomplicated."
  Reality: First understand callers, responsibilities, and edge cases; confusion
  is not proof of needless complexity.
- Rationalization: "A new helper will make it cleaner."
  Reality: Helpers add concepts. Prefer deletion, inlining, and local clarity
  unless reuse or a seam is real.
- Rationalization: "I might as well fix this nearby behavior."
  Reality: Feature work belongs in a separate spec/ticket or explicit scope
  expansion.

## Red Flags

- simplification changes behavior without spec or ticket ownership
- deleted code had uninspected callers or compatibility obligations
- several unrelated cleanups are batched into one hard-to-review diff
- evidence is only a diff that looks cleaner
- new abstractions outnumber deleted concepts
- review cannot tell whether behavior changed

## Verification

- [ ] Behavior that must remain unchanged is explicit.
- [ ] Callers, responsibilities, tests, and edge cases were inspected or marked unknown.
- [ ] Write scope stayed narrow and did not absorb feature work.
- [ ] Behavior-preservation evidence supports the ticket claim or limits are explicit.
- [ ] Escalations to architecture, migration, spec, plan, or critique are recorded when needed.

## Done Means

- the code is simpler by a named criterion without hidden behavior change
- the ticket owns scope, evidence disposition, and acceptance
- evidence supports behavior preservation or names remaining risk
- critique disposition matches the size and risk of the cleanup

## Read In This Order

Read immediately for simplification work:

1. `references/simplification-playbook.md` for the full simplification process,
   opportunity tables, language notes, evidence expectations, and review questions.
2. the core `loom-tickets` skill to confirm scope, acceptance, evidence, and review disposition.
3. the core `loom-evidence` skill for behavior-preservation checks and diff review evidence.
4. the core `loom-critique` skill when cleanup is non-trivial or behavior risk is plausible.

Then read conditionally:

5. `skills/loom-architecture/SKILL.md` when cleanup reveals seam, API, or module-boundary work.
6. `skills/loom-migration/SKILL.md` when old paths have consumers or removal lifecycle risk.
7. the core `loom-specs` or `loom-plans` skills when behavior or sequencing becomes unclear.
