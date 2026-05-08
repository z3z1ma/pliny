---
name: loom-incremental-implementation
description: "Implement changes in small verified slices. Use when a feature, refactor, migration, or bug fix touches multiple files, feels too large to land at once, needs feature flags, or should remain working after each increment."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-incremental-implementation

Incremental implementation keeps every step understandable, testable, and reversible.

This playbook coordinates thin execution slices inside the ticket/Ralph loop. It
does not replace ticket truth, packet scope, evidence, or Git provenance.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- one-logical-change-at-a-time execution
- vertical, contract-first, and risk-first implementation slices
- scope discipline during multi-file edits
- safe defaults, feature flags, and rollback-friendly increments
- per-slice verification and evidence handoff

## What This Workflow Does Not Own

- intended behavior or acceptance; use specs and tickets
- live execution status or closure; use tickets
- child authority; use Ralph packets
- commit, branch, merge, or worktree policy; use `loom-git`
- release packaging; use `loom-ship`

## Use This Skill When

- implementing a feature or change across more than one file
- tempted to write a large batch of code before testing
- refactoring or cleanup needs several independent steps
- incomplete work needs to be merged safely behind flags or disabled paths
- a ticket can be advanced by one complete, verifiable slice

## Do Not Use This Skill When

- the task is a single obvious local edit
- the work lacks a ready ticket or clear behavior owner
- the next step is planning, discovery, spike, codemap, or debugging
- slicing would hide a needed migration, architecture, or spec decision

## Default Procedure

1. Read the owning ticket, acceptance IDs, write boundary, relevant source files,
   tests, and any plan sequence.
2. Pick one slice: vertical when possible, contract-first when parallel work needs a
   seam, risk-first when uncertainty could invalidate later work.
3. State what is in scope and explicitly what nearby cleanup, refactor, or feature
   work is not in scope.
4. Implement the smallest complete behavior or structural step that leaves the
   system coherent.
5. Use `loom-tdd` for behavior changes when a failing check is practical; otherwise
   use observation-first or structural verification.
6. Run the relevant verification after the slice, read output, and preserve evidence
   when ticket acceptance or later critique depends on it.
7. Reassess before the next slice: if behavior, architecture, migration, security,
   or performance scope changed, route outward instead of continuing blindly.
8. Use `loom-git` for atomic commit/provenance work when commits are requested or
   branch/worktree state matters.
9. Keep a feature flag, adapter, or disabled path only with owner, expiry or cleanup
   trigger, and ticket disposition.

## Slice Rules

- One slice changes one logical concern.
- The project should build or be explicitly marked in a known intermediate state
  after the slice.
- The slice should be independently reviewable and revertable.
- Refactors and features should be separate unless the ticket explicitly scopes the
  refactor as part of the behavior change.
- Adjacent issues become notes or follow-up tickets, not drive-by edits.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "It is faster to build everything first and test at the end." | Bugs compound across slices and become harder to localize. |
| "This nearby cleanup is small." | Nearby cleanup widens review and evidence scope. Record it or create a separate ticket. |
| "A flag means incomplete work is harmless." | Flags need owner, expiry/cleanup trigger, and verification of relevant states. |
| "I'll split commits later." | Split before review and evidence, not after a tangled diff exists. |

## Red Flags

- more than one feature, refactor, config, or migration concern in the same slice
- tests/build broken between slices without explicit ticket rationale
- large uncommitted or unreviewable diff accumulates
- feature flag has no owner or cleanup trigger
- implementation continues after discovering spec or architecture ambiguity
- verification output is stale or repeated without source changes

## Verification

- [ ] Slice scope and out-of-scope nearby work are explicit.
- [ ] Verification ran after the slice or limitation is recorded.
- [ ] Behavior changes have TDD or observation-first proof proportional to risk.
- [ ] Feature flags/adapters have owner, expiry/cleanup trigger, and evidence plan.
- [ ] Next slice is still justified by current owner records.

## Done Means

- the ticket advanced by one coherent, evidence-backed step
- the system is working or any intermediate state is explicitly owned by the ticket
- no unrelated cleanup or feature work is hidden in the slice
- continuation can resume from ticket, evidence, and Git/packet provenance

## Read In This Order

Read immediately for multi-file execution:

1. `references/thin-slice-execution.md` for slicing strategies, scope discipline,
   safe defaults, feature flags, rollback, and per-slice checks.
2. the core `loom-tickets` skill to confirm live execution state and acceptance.
3. the core `loom-evidence` and `loom-tickets` skills before making success,
   acceptance, or closure claims.

Then read conditionally:

4. `skills/loom-tdd/SKILL.md` for behavior changes.
5. `skills/loom-git/SKILL.md` for branch, commit, worktree, and diff hygiene.
6. `skills/loom-agent-orchestration/SKILL.md` when multiple independent slices may use fresh workers.
