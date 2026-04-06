---
name: loom-workspace
description: Parent-side Loom control-plane skill for workspace discovery, status, diagnostics, repository and worktree scope resolution, record discovery, validation routing, and subsystem selection. Use when entering the repo fresh, diagnosing workspace health, resolving path or repository ownership, discovering records, or deciding which skill should own the next durable action. Not for cases where the owning subsystem is already clear and no control-plane step is needed.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: control-plane
---

# loom-workspace

Use this skill as the parent-side Loom control plane for workspace discovery, readiness checks, routing, and structural diagnosis.

## Use This Skill When

- you entered the repository fresh and need orientation
- you need to bootstrap a new Loom workspace (`.loom/` does not exist or is incomplete)
- you do not yet know which Loom layer owns the next durable action
- you need to diagnose workspace health before trusting records or packet work
- scope ownership of a path or repository is unclear

## Do Not Use This Skill When

- you already know the exact owning subsystem and only need that artifact-layer workflow
- the task is purely local and has no durable Loom consequences

## What This Skill Governs

- workspace initialization and directory bootstrapping
- workspace-level health checks
- repository and worktree scope discovery
- parent-side readiness decisions
- status and diagnosis behavior

## Default Workspace Posture

- fail closed when repository or worktree ownership is ambiguous
- prefer explicit diagnosis over silent assumptions
- prefer reading canonical state before packet launch
- route into the owning subsystem instead of letting one skill absorb unrelated responsibilities
- treat health and validation as decision inputs, not decorative reports

## Execution Playbook

1. if `.loom/` does not exist or is missing canonical subtrees, run `scripts/workspace.py diagnose --fix` to create missing structure before doing anything else
2. start with `scripts/workspace.py status` to summarize the current workspace state and locate likely owning surfaces
3. run `scripts/workspace.py diagnose` before trusting downstream records, packets, or operator guidance
4. check for `.loom/harness.md` — if present, the operator has defined harness profiles for child invocation; note which profiles exist so downstream skills can use them
5. use `scripts/workspace.py list` when you need canonical refs before linking, reviewing, or compiling packets
6. run `scripts/workspace.py scope` for any path or repository ownership question and fail closed if it cannot assign scope cleanly
7. use `scripts/workspace.py diagnose` and `scripts/workspace.py check-links` before depending on a record graph that may have drifted
8. route into the owning subsystem only after the workspace is structurally trustworthy enough to proceed
9. if the workspace is not trustworthy, fix that first instead of pushing uncertainty into the next skill

## Decision Rules

If `scripts/workspace.py diagnose` or validation reports structural issues, fix those before trusting downstream packet work.

If `scripts/workspace.py scope` cannot assign ownership, escalate immediately rather than guessing.

If subsystem ownership is unclear, read the relevant canonical record and choose the skill that owns the next durable mutation or review step.

## Failure Conditions

Do not proceed as if the workspace is trustworthy when:

- repository ownership is ambiguous
- validation is failing
- links are broken
- required rule or skill surfaces are missing
- packet-consuming work is being attempted without adequate structural trust

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/workspace.py diagnose`: use before depending on the workspace for packet work, review, or durable edits; use `--fix` to create missing directories
- `scripts/workspace.py create`: use for kind-specific validation when structural trust matters around one record family
- `scripts/workspace.py check-links`: use to validate the record graph; treat this as a workspace-level integrity check rather than a one-file command
- `scripts/workspace.py link`: use when you need to add or remove typed links between records
- `scripts/workspace.py verify`: use when a verification artifact should become durable
- `scripts/workspace.py scope`: use when you need a deterministic repository owner for one path

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

1. `references/scripts.md`
2. `references/doctor.md`
3. `references/status.md`
4. `references/examples.md`

## References

- `references/scripts.md`
- `references/status.md`
- `references/doctor.md`
- `references/examples.md`
