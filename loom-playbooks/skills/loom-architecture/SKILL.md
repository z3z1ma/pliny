---
name: loom-architecture
description: "Improve architecture and interface seams. Use when refactoring module boundaries, reducing coupling, designing APIs or adapters, making code more testable, or turning codemap friction into planned structure changes; route durable truth to Loom owner records."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-architecture

Architecture work changes how future implementation should be shaped.

This playbook coordinates interface, seam, module-boundary, and coupling work
without creating an architecture ledger outside `loom-core` records.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- architecture-friction diagnosis after codemap or implementation discovery
- interface and seam option framing
- module-boundary refactor strategy
- API contract and adapter design routing
- testability and locality improvement planning
- evidence and critique expectations for architecture mutations

## What This Workflow Does Not Own

- durable policy or architectural precedent; use constitution decisions
- accepted repository or module atlas explanation; use wiki through `loom-codemap`
- intended behavior and reusable API contracts; use specs
- sequencing across multiple tickets; use plans
- live execution, blockers, acceptance, or closure; use tickets
- review verdicts; use critique

## Use This Skill When

- a change should reduce coupling, clarify module boundaries, or deepen an interface
- current code makes one concept spread across many files without a clear seam
- a public, shared, or internal API needs alternatives before implementation
- a codemap pass found shallow wrappers, unclear adapters, or missing test surfaces
- behavior-preserving refactor work is too structural for ordinary cleanup

## Do Not Use This Skill When

- the next step is only mapping current structure; use `loom-codemap`
- the work is simple behavior-preserving cleanup; use `loom-simplification`
- intended behavior is still fuzzy; use core specs before architecture execution
- a durable principle or hard constraint is changing; use constitution
- the implementation slice is already ticket-ready and needs no architecture choice

## Default Procedure

1. Orient from the current code, related tests, existing specs, wiki atlas pages,
   decisions, tickets, and relevant codemap output.
2. Name the architecture friction precisely: coupling, locality, shallow wrapper,
   missing adapter, unclear ownership, test seam, API compatibility, or repeated
   path rediscovery.
3. Identify current callers, data flow, side effects, error semantics, and test
   surfaces before proposing a new shape.
4. Produce two or three materially different options when the interface or seam is
   not obvious. Compare depth, locality, compatibility, testing leverage,
   migration cost, and deletion path.
5. Route tradeoffs, rejected options, and uncertainty to research. Route intended
   API, module, or behavior contracts to specs.
6. Use a plan when the architecture change needs sequencing, migration, rollout,
   or multiple tickets. Use one ticket when the mutation is bounded.
7. Execute locally only for a narrow, safe slice. Use Ralph when the write scope is
   broad, risky, or benefits from a fresh bounded worker.
8. Preserve before/after evidence: tests, structural checks, dependency/caller
   scans, or focused observations that prove behavior and contract preservation.
9. Run critique for seam/API risk, behavior-preservation risk, and operator
   clarity before acceptance when risk warrants it.
10. Promote accepted architecture explanation to wiki only after owner truth and
    critique are settled.

## Seam Checks

Ask these before choosing a design:

- Can one caller use the new interface without knowing internal storage,
  framework, transport, or side-effect details?
- Does the interface make the important behavior easier to test at a deeper seam,
  not only through many shallow units?
- Can old code be deleted or isolated after migration, or does the design create a
  permanent adapter layer by accident?
- Does Hyrum's Law matter because external or many internal consumers may depend
  on undocumented behavior?
- Is the proposed boundary close to the concept it names, or does it force future
  agents to bounce through unrelated files?

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "I can refactor first and document the architecture later." | Architecture mutations need intended seams, evidence, and ticket scope before downstream code depends on them. |
| "The new abstraction looks cleaner." | Clean is not enough; prove locality, test leverage, compatibility, and deletion path. |
| "A codemap already found the problem, so implementation is obvious." | Codemap explains current structure. Architecture work chooses a mutation path and must compare options when the seam is not obvious. |
| "All callers are internal, so compatibility does not matter." | Internal consumers can still rely on undocumented behavior; inspect callers before narrowing contracts. |

## Red Flags

- architecture choice lacks current caller or test-surface inspection
- option comparison is cosmetic rather than structurally different
- a wiki page is treated as the behavior contract
- refactor expands into feature work without ticket or spec ownership
- old and new paths remain indefinitely with no migration or deletion trigger
- critique is skipped for a broad seam or API change because tests passed

## Verification

- [ ] Architecture friction and desired seam are explicit.
- [ ] Current callers, tests, contracts, and side effects were inspected or marked unknown.
- [ ] Tradeoffs and rejected options are in research when the choice was non-obvious.
- [ ] Intended behavior or interface contract is in a spec when downstream work needs it.
- [ ] Plan, ticket, evidence, and critique disposition match the risk and scope.
- [ ] Accepted architecture explanation is promoted to wiki only after owner truth settles.

## Done Means

- the architecture choice is routed to the proper owner records
- the implementation slice is ticket-owned and evidence-backed
- behavior preservation and interface compatibility are validated or explicitly limited
- critique disposition is closure-compatible when risk warrants review
- future agents can recover the chosen seam without reading chat history

## Read In This Order

Read immediately for architecture work:

1. `references/interface-and-seam-design.md` for vocabulary, dependency
   categories, seam discipline, contract-first design, Hyrum's Law, validation
   boundaries, and interface alternative design.
2. `skills/loom-codemap/SKILL.md` when current structure, call paths, or module
   ownership are not already clear.
3. the core `loom-research` skill when comparing options, rejected designs, or
   tradeoffs.
4. the core `loom-specs` skill when interface behavior, API contracts, or
   compatibility promises need a stable owner.

Then read conditionally:

5. the core `loom-plans` skill when sequencing, rollout, or migration matters.
6. the core `loom-tickets` and `loom-ralph` skills when implementation is ready.
7. the core `loom-evidence` and `loom-critique` skills for before/after proof and
   seam/API review.
8. the core `loom-wiki` skill when accepted architecture explanation should persist.
