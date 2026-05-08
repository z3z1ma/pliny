---
name: loom-docs-sync
description: "Keep README, API docs, changelogs, inline comments, and operator-facing documentation synchronized with Loom owner truth. Use when documentation must mirror accepted decisions, behavior, releases, migrations, or recurring explanations without becoming the owner."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-docs-sync

Documentation sync keeps presentation surfaces aligned with the Loom graph.

This playbook is for documentation that mirrors, explains, or packages accepted
truth. It does not own decisions, intended behavior, acceptance, or release state.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- README, setup, API, changelog, release-note, and inline-comment sync
- documentation freshness checks after accepted implementation or migration work
- mapping docs changes to the owner records they mirror
- stale path, command, and link reconciliation
- docs follow-through during ship, migration, source-grounding, and architecture work

## What This Workflow Does Not Own

- durable decisions, ADR-like precedent, principles, or policy; use constitution
- intended behavior or API contracts; use specs
- accepted explanation; use wiki
- live docs tasks, blockers, closure, or accepted risk; use tickets
- release packaging or PR summaries; use `loom-ship`

## Use This Skill When

- public APIs, commands, setup, or developer workflow changed
- README, API docs, changelog, release notes, or inline gotchas need updating
- migration, deprecation, ship, architecture, or source-grounding work changes what future users or agents need to know
- docs may be stale relative to accepted owner records
- a path-local instruction file should point at Loom records without defining competing truth

## Do Not Use This Skill When

- the real change is a project decision or policy; use `loom-constitution`
- the real change is intended behavior; use core specs
- the real change is accepted explanation; use core wiki
- documentation would restate obvious code
- docs are being used to carry live execution state instead of tickets

## Default Procedure

1. Identify the documentation surface: README, setup, API docs, changelog, release
   note, inline comment, path-local instruction, or operator guide.
2. Identify the owner truth being mirrored: constitution decision, spec, wiki,
   ticket, evidence, research, ship package, or memory support pointer.
3. If the owner truth is missing or stale, update the owner layer first instead of
   letting docs become the source of truth.
4. Update docs to present the current owner truth with links when useful.
5. For inline comments, explain why or a non-obvious constraint, not what the code
   already says.
6. For public APIs, mirror the spec-owned contract for inputs, outputs, errors,
   compatibility, examples, and deprecation / migration status.
7. For README/setup docs, check current commands, environment notes, quick start,
   architecture overview, and troubleshooting links.
8. For changelogs or release notes, mirror accepted ticket/evidence/critique truth
   through `loom-ship` rather than inventing status.
9. Verify links, paths, commands, and stale references proportional to the docs
   claim.

## Documentation Quality

Good synchronized documentation:

- points at owner records when the claim is durable or non-obvious
- names freshness or version limits when relevant
- avoids TODOs that should be tickets
- includes setup or API examples only when they are current or marked unverified
- does not become a shadow ledger, shadow ADR store, or hidden support memory

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "The code is self-documenting." | Code shows what. Docs often need to explain setup, public contracts, examples, and why accepted constraints matter. |
| "We can write docs after release." | Docs, migration notes, and setup changes are part of acceptance when future use depends on them. |
| "This ADR can live in docs." | In Loom, durable decisions belong to constitution. Docs may mirror or link them. |
| "A TODO comment is enough." | Future work needs ticket disposition or an explicit accepted risk. |

## Red Flags

- docs define a decision, behavior, or live state that owner records do not own
- README commands are stale or unverified
- public API changed without spec or docs reconciliation
- comments restate code or preserve commented-out old code
- docs claim completion while ticket/evidence/critique do not
- old docs still point at removed paths after migration

## Verification

- [ ] Documentation surface and owner truth are both identified.
- [ ] Missing owner truth was routed to the owner layer before docs were updated.
- [ ] README/API/changelog/release docs mirror current owner truth.
- [ ] Inline comments explain non-obvious why or gotchas.
- [ ] Stale paths, commands, TODOs, and commented-out code are reconciled.

## Done Means

- future users and agents can use the docs without contradicting owner records
- docs mirror owner truth without becoming the owner
- stale or missing docs are ticket-owned or explicitly out of scope
- release and handoff wording can rely on current records

## Read In This Order

Read immediately for docs sync work:

1. `references/documentation-sync.md` for owner routing, README/API/changelog,
   comments, path-local instructions, and freshness checks.
2. the core `loom-tickets` skill when docs follow-through, accepted risk, or
   closure state changes.
3. the core `loom-wiki` skill when accepted explanation should persist.

Then read conditionally:

4. the core `loom-constitution` skill when durable decisions or constraints change.
5. the core `loom-specs` skill when documentation affects intended behavior.
6. `skills/loom-ship/SKILL.md` when release notes or handoff summaries are needed.
7. `skills/loom-migration/SKILL.md` when docs must track old/new paths.
8. `skills/loom-source-grounding/SKILL.md` when external docs or version citations matter.
