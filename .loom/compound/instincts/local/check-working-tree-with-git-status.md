---
id: check-working-tree-with-git-status
title: Check working tree state with git status
trigger: Before resuming edits or after tool activity that may change repository state
confidence: 0.6200
status: active
domain: workflow
source: local
created_at: 2026-02-15T21:06:52.548579Z
updated_at: 2026-02-15T21:06:52.548579Z
tags: workflow, git, state-awareness, safety
notes: Two separate invocations in one run suggest deliberate state verification rather than incidental use.
---

## Action
Run `git status --porcelain` at key checkpoints to confirm current working tree state before proceeding with additional edits or commands.

## Evidence
- ts=2026-02-15T21:06:02.449035Z source_id=obs-git-status-210602 source_hash=git-status-porcelain
- ts=2026-02-15T21:06:52.292706Z source_id=obs-git-status-210652 source_hash=git-status-porcelain

## Notes
Two separate invocations in one run suggest deliberate state verification rather than incidental use.
