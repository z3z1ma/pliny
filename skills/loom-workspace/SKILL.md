---
name: loom-workspace
description: "Parent-side Loom control-plane skill for workspace discovery, status, repository and worktree scope resolution, record discovery, validation routing, and subsystem selection. Use when entering the repo fresh, when `.loom/` is missing or incomplete where Loom expects it, when the user explicitly asks to set up, initialize, bootstrap, or scaffold Loom, when workspace health or scope ownership is unclear, or when you do not yet know which Loom layer owns the next durable action. Not for cases where the owning subsystem is already clear and no control-plane step is needed."
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: control-plane
---

# loom-workspace

Use this skill as the parent-side Loom control plane for workspace discovery, readiness checks, routing, and scope resolution.

## Use This Skill When

- you entered the repository fresh and need orientation
- you need to bootstrap a new Loom workspace (`.loom/` does not exist or is incomplete)
- you do not yet know which Loom layer owns the next durable action
- you need to inspect workspace health before trusting records or packet work
- scope ownership of a path or repository is unclear

## Do Not Use This Skill When

- you already know the exact owning subsystem and only need that artifact-layer workflow
- the task is purely local and has no durable Loom consequences

## What This Skill Governs

- workspace initialization and directory bootstrapping
- workspace-level health checks
- repository and worktree scope discovery
- parent-side readiness decisions
- status and health-check guidance

## Default Workspace Posture

- fail closed when repository or worktree ownership is ambiguous
- prefer explicit health checks over silent assumptions
- prefer native file inspection for workspace health checks
- prefer reading canonical state before packet launch
- route into the owning subsystem instead of letting one skill absorb unrelated responsibilities
- treat health and validation as decision inputs, not decorative reports

## Execution Playbook

1. if `.loom/` does not exist or is missing canonical subtrees, create the missing directories directly with `mkdir -p` before doing anything else
2. start with direct `find` and `rg` queries to summarize the current workspace state and locate likely owning surfaces
3. inspect `.loom/`, `rules/`, and `skills/` directly before trusting downstream records, packets, or operator guidance
4. check for `.loom/harness.md` — if present, the operator has defined harness profiles for child invocation; note which profiles exist so downstream skills can use them
5. use `find .loom -name '*.md'` and targeted `rg` when you need canonical refs before linking, reviewing, or compiling packets
6. use `git rev-parse --show-toplevel` from the target path or a nearest ancestor to confirm repository ownership and fail closed if the answer is still ambiguous
7. use direct file queries across `.loom/` before depending on a record graph that may have drifted
8. route into the owning subsystem only after the workspace is structurally trustworthy enough to proceed
9. if the workspace is not trustworthy, fix that first instead of pushing uncertainty into the next skill

## Decision Rules

If direct workspace inspection or validation reports structural issues, fix those before trusting downstream packet work.

If native repository inspection still cannot assign ownership cleanly, escalate immediately rather than guessing.

If subsystem ownership is unclear, read the relevant canonical record and choose the skill that owns the next durable mutation or review step.

## Failure Conditions

Do not proceed as if the workspace is trustworthy when:

- repository ownership is ambiguous
- validation is failing
- links are broken
- required rule or skill surfaces are missing
- packet-consuming work is being attempted without adequate structural trust

## How To Use Native Tooling

Read `references/queries.md` for native workspace query patterns and example invocations.

- use `find` to enumerate records, directories, and likely owning surfaces
- use `rg` to inspect statuses, IDs, links, and cross-record references directly
- use `mkdir -p` to bootstrap or repair missing `.loom/` directories
- use `git rev-parse --show-toplevel` from the target path when repository ownership needs confirmation
- switch to the owning skill's script only when you need record-aware scaffolding, validation, or mutation

Prefer native file tools such as `find`, `rg`, `mkdir -p`, and `git` for workspace health checks and bootstrapping. Use record-aware commands only in the owning skill.

## What Good Looks Like

- you know whether the workspace is healthy enough to trust
- you know which repository owns the target path or record
- you know which Loom skill should own the next durable action
- you do not need to guess about structure, scope, or routing

## Done Means

- workspace health is explicit enough to trust or explicitly unsafe enough to halt
- ownership is resolved or the ambiguity is surfaced clearly
- the next owning skill is identified without guesswork
- downstream work starts from structural trust instead of optimism

## Read In This Order

1. `references/queries.md`
2. `references/doctor.md`
3. `references/status.md`
4. `references/examples.md`

## References

- `references/queries.md`
- `references/status.md`
- `references/doctor.md`
- `references/examples.md`
