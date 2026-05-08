---
name: loom-workspace
description: "Orient and route Loom work. Use when starting or resuming a session, the request is fuzzy, repository scope or owner chain is unclear, or you need to decide which skill handles a coding task."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: control-plane
---

# loom-workspace

Use this skill first when you are entering a Loom repository cold, resuming after
context compaction, preparing for compaction, or when the next owner layer is not
yet obvious.

This skill replaces the old "doctor", "status", and "scope helper" mindset with a more agent-native posture:
inspect the workspace directly, make structural trust explicit, then route to the owning layer.

## What This Skill Owns

- workspace bootstrap
- workspace diagnosis
- repository / scope discovery
- fuzzy-request problem shaping before owner commitment
- first-read order
- subsystem routing
- status snapshot synthesis
- cold-start and post-compaction recovery routing
- pre-compaction owner update checks

## First Read Order

When Loom is present and the repo looks structurally plausible:

1. load `using-loom` doctrine, or confirm the harness preloaded the ordered
   using-Loom references
2. inspect `.loom/`
3. read `constitution:main`
4. for cold-start or post-compaction recovery, discover active tickets and other
   live status queues with `references/status-snapshot.md`
5. read the obvious owner chain for the current task
6. choose the next skill

Do not start deep work before the workspace is structurally trustworthy enough to trust its records.
Do not treat chat history, transcript memory, generated context files, or memory
records as canonical resume truth; continue from the owner records that own the
current fact.

## Use This Skill When

- `.loom/` is missing, partial, or suspicious
- the target path may belong to one of several repositories
- you do not yet know whether the task belongs to constitution, initiative,
  research, spec, plan, ticket, evidence, Ralph, critique, wiki,
  retrospective, or a workflow coordinator
- the user asked to set up Loom in a repository
- the workspace needs a health pass before packet work
- you are recovering after a cold start or context compaction and need to find
  the current active ticket or live queue from files
- you are about to stop or compact and need owner records to make continuation
  recoverable without transcript context

## Do Not Use This Skill When

- the owner layer is already obvious and structurally sound
- you are already inside a bounded ticket iteration and only need the owning execution skill

## Default Workspace Procedure

1. confirm the workspace root
2. inspect the `.loom/` tree and read order
3. verify `constitution:main` exists, or route to `loom-constitution` if the
   user is bootstrapping Loom and the constitution must be created
4. verify the canonical subdirectories exist
5. resolve repository ownership of the target path
6. if resuming, list active, blocked, review, and acceptance queues from tickets
7. read the governing artifact chain
8. choose the next owner layer, skill, or workflow coordinator from the record
   truth

## Signals That You Should Halt Or Escalate

Halt or escalate when:

- the workspace root is ambiguous
- multiple repository owners look plausible for the same target path
- `.loom/` exists but the canonical tree is malformed enough that you cannot trust it
- the task would require widening scope without a ticket/plan update

## Native Tool Posture

Prefer direct inspection before inventing a helper abstraction:

- `find` / `fd` for tree discovery
- `rg` for IDs, statuses, and refs
- `git rev-parse --show-toplevel` for repository ownership
- `git status --short` and `git diff --stat` for current mutation awareness

## Common Rationalizations

- **"The current directory is obviously the workspace root."**
  - Reality: Nested repos, examples, and fixtures can contain their own Loom trees. Verify scope.
- **"Chat history is enough to resume."**
  - Reality: Recovery must come from owner records, not transcript memory.
- **"`.loom/` exists, so the workspace is trustworthy."**
  - Reality: The tree can be partial, stale, or scoped to a fixture. Inspect structure and constitution.
- **"I know the next skill without reading records."**
  - Reality: Route from owner truth when the workspace is not freshly known.

## Red Flags

- active work appears under a nested example or wrong repository root
- no `constitution:main` or equivalent workspace identity is inspectable
- ticket queues, blockers, or review debt are inferred from memory instead of files
- path-local instructions or generated context disagree with Loom owner records
- scope would cross repositories without a registry or explicit operator direction

## Verification

- [ ] Workspace root and repository ownership are explicit.
- [ ] Canonical `.loom/` tree and constitution are structurally trustworthy enough for the task.
- [ ] Active tickets, blockers, and review/acceptance queues were discovered from records when resuming.
- [ ] The next skill is chosen from owner-layer truth, not habit or transcript context.

## Done Means

- the workspace root is explicit
- structural trust is explicit
- the owner layer, skill, or workflow coordinator needed for the user's task is
  clear from the records
- you are not guessing about scope or routing

## Read In This Order

Read immediately for normal workspace entry:

1. `references/workspace-tree.md` when checking or bootstrapping the `.loom`
   directory shape.
2. `references/routing.md` when deciding which owner layer or workflow
   coordinator should handle the request.
3. `references/task-routing-catalog.md` when the user asks in ordinary coding
   language such as bug, feature, refactor, tests, dependency, performance,
   security, UI, API, docs, PR, release, or done/acceptance terms.

Then read conditionally:

4. `references/status-snapshot.md` when recovering after cold start or context
   compaction, preparing for compaction, or summarizing current queues, blockers,
   review debt, or acceptance debt.
5. `references/problem-shaping.md` when the operator request is too fuzzy to
   route directly into an owner record.
6. `references/doctor.md` when structural trust is questionable.
7. `references/scope-registry.md` when repository aliases or multi-worktree
   scope need to be made explicit.
8. `templates/workspace.md` only when creating `.loom/workspace.md`.
9. `templates/harness.md` only when documenting fresh-context invocation
   mechanics.
