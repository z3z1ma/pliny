---
name: loom-migration
description: "Plan and execute migrations, deprecations, replacements, and removals. Use when sunsetting APIs, replacing libraries, moving data or consumers, retiring feature flags, consolidating old paths, proving zero usage, or coordinating staged rollout and cleanup through Loom records."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-migration

Migration work is a lifecycle, not one cleanup commit.

This playbook coordinates replacement, deprecation, usage inventory, staged
movement, zero-usage proof, removal, and post-removal cleanup through core records.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- replacement-before-deprecation discipline
- consumer and usage inventory
- staged migration, adapter, strangler, and feature-flag lifecycle planning
- zero-usage evidence before removal
- cleanup of old code, tests, docs, config, and explanation
- rollout, rollback, and ship handoff alignment

## What This Workflow Does Not Own

- durable roadmap or policy direction; use constitution or initiatives
- replacement behavior or compatibility contracts; use specs
- sequencing across tickets; use plans
- live migration progress, blockers, accepted risk, or closure; use tickets
- observed usage and zero-usage proof; use evidence
- release notes or PR packaging; use `loom-ship`

## Use This Skill When

- an old API, feature, library, workflow, storage path, flag, or integration is being replaced
- consumers must move from old behavior to new behavior safely
- deprecation notices, compatibility windows, or removal conditions matter
- zero usage must be proven before deleting code, docs, config, or data paths
- adapters, strangler patterns, feature flags, or staged rollout are likely

## Do Not Use This Skill When

- the change is a one-file behavior-preserving cleanup; use `loom-simplification`
- there is no old path, consumer movement, rollout, or cleanup lifecycle
- intended replacement behavior is unclear; use specs first
- the next task is only packaging already-truthful work; use `loom-ship`

## Default Procedure

1. Identify old path, replacement path, consumers, compatibility promises, data
   ownership, rollout constraints, and removal risks.
2. Require a replacement or explicit no-replacement rationale before deprecating.
3. Preserve usage inventory and baseline observations in evidence when they will
   justify migration, hold, or removal decisions.
4. Route replacement behavior and compatibility boundaries to specs.
5. Use a plan for staged sequencing, consumer order, adapters, feature flags,
   rollout, rollback, and cleanup triggers.
6. Create tickets for bounded consumer moves, adapter changes, data migrations,
   deprecation notices, verification steps, and removals.
7. For flags or adapters, name owner, expiry or cleanup trigger, enabled/disabled
   verification needs, and follow-up disposition.
8. Before removing the old path, gather zero-usage or safe-removal evidence and run
   critique for data migration, dependency, security, or API risk when applicable.
9. Use `loom-ship` to package launch, rollout, rollback, release, or handoff notes
   after owner records are truthful.
10. Run retrospective when repeated migration lessons, cleanup triggers, or
    operator guidance should persist.

## Migration Patterns

- Strangler: route new work through the replacement while old consumers drain.
- Adapter: isolate compatibility while consumers migrate, with a deletion trigger.
- Feature flag: stage exposure and rollback, with owner and expiry.
- Bulk cutover: use only when rollback, evidence, and blast radius are acceptable.
- Zombie-code removal: delete only after usage, references, docs, and tests are reconciled.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "We can deprecate first and build the replacement later." | Consumers need a credible replacement path or an explicit no-replacement decision. |
| "No one probably uses the old path." | Removal needs usage inventory or an explicit evidence limit, not probability. |
| "The feature flag makes this safe indefinitely." | Flags need owner, expiry or cleanup trigger, and verification for relevant states. |
| "Cleanup can be a follow-up note in the PR." | Cleanup that affects closure or future work needs ticket-owned disposition or follow-up tickets. |

## Red Flags

- old and new paths coexist without owner or deletion trigger
- consumer inventory is guessed from memory
- zero usage is claimed without evidence or explicit limits
- compatibility behavior changes without a spec amendment
- rollback or idempotency is absent for data or dependency migration
- docs, tests, config, or wiki still point at the removed path

## Verification

- [ ] Old path, replacement path, consumers, and compatibility boundary are explicit.
- [ ] Usage and zero-usage claims are evidence-backed or explicitly limited.
- [ ] Specs, plans, tickets, evidence, and critique match the migration risk.
- [ ] Flags/adapters have owner, expiry or cleanup trigger, and follow-up disposition.
- [ ] References to removed paths are reconciled before closure.

## Done Means

- consumers have moved or accepted risk is ticket-owned
- old path removal is evidence-backed and reference-reconciled
- rollout, rollback, and cleanup claims mirror owner records
- critique and retrospective disposition are closure-compatible

## Read In This Order

Read immediately for migration work:

1. `references/migration-lifecycle.md` for deprecation decisions, advisory versus
   compulsory migration, consumer inventory, migration patterns, zombie-code
   disposition, and removal verification.
2. the core `loom-specs` skill for replacement behavior and compatibility contracts.
3. the core `loom-plans` skill for staged migration, rollout, dependencies, and cleanup triggers.
4. the core `loom-evidence` skill for usage inventory, zero-usage proof, and before/after output.

Then read conditionally:

5. the core `loom-tickets` and `loom-ralph` skills for bounded migration execution.
6. `skills/loom-ship/SKILL.md` for launch, rollback, PR, release, or handoff packaging.
7. the core `loom-critique` and `loom-retrospective` skills for review and lessons.
8. `skills/loom-security/SKILL.md` when migration touches sensitive data, auth,
   permissions, or external trust boundaries.
