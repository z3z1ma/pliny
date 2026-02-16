---
id: check-working-tree-with-git-status
title: Check working tree state with git status
trigger: Before resuming edits or after tool activity that may change repository state
confidence: 0.8500
status: active
domain: workflow
source: local
created_at: 2026-02-15T21:06:52.548579Z
updated_at: 2026-02-16T06:24:33.846388Z
tags: workflow, git, state-awareness, safety
notes: This pattern appears around coordination and validation transitions, reducing state drift risk before next actions.
---

## Action
Run `git status --porcelain` (or `git status --short`) at key checkpoints to confirm current working tree state before proceeding with additional edits or coordination commands.

## Evidence
- ts=2026-02-15T23:42:50.144244Z source_id=obs-git-status-234250 source_hash=git-status-porcelain
- ts=2026-02-15T23:48:41.974840Z source_id=obs-git-status-234841 source_hash=git-status-short
- ts=2026-02-15T23:50:04.029376Z source_id=obs-git-status-235004 source_hash=git-status-porcelain
- ts=2026-02-15T23:50:38.678586Z source_id=obs-git-status-235038 source_hash=git-status-porcelain
- ts=2026-02-15T23:50:44.063915Z source_id=obs-git-status-235044 source_hash=git-status-short-clean-checkpoint
- ts=2026-02-15T23:51:27.453273Z source_id=obs-git-status-235127 source_hash=git-status-short-branch-merge-queue
- ts=2026-02-15T23:52:00.101203Z source_id=obs-git-status-235200 source_hash=git-status-short-ticket-checkpoint
- ts=2026-02-15T23:52:38.978527Z source_id=obs-git-status-235238 source_hash=git-status-short-clean-after-commit
- ts=2026-02-15T23:53:50.200319Z source_id=obs-git-status-235350 source_hash=git-status-porcelain
- ts=2026-02-15T23:54:36.194631Z source_id=obs-git-status-235436 source_hash=git-status-porcelain
- ts=2026-02-15T23:54:55.362053Z source_id=obs-git-status-235455 source_hash=git-status-porcelain
- ts=2026-02-16T00:01:29.233006Z source_id=obs-git-status-000129 source_hash=git-status-short-checkpoint
- ts=2026-02-16T00:06:54.400484Z source_id=obs-git-status-000654 source_hash=git-status-short-branch-pre-merge
- ts=2026-02-16T00:22:56.553761Z source_id=obs-git-status-002256 source_hash=git-status-porcelain-pre-validation
- ts=2026-02-16T00:23:40.331963Z source_id=obs-git-status-002340 source_hash=git-status-short-post-pytest
- ts=2026-02-16T00:23:53.036305Z source_id=obs-git-status-002353 source_hash=git-status-short-clean-after-commit
- ts=2026-02-16T00:24:26.769134Z source_id=obs-git-status-002426 source_hash=git-status-short-branch-post-merge-queue
- ts=2026-02-16T00:24:47.342356Z source_id=obs-git-status-002447 source_hash=git-status-porcelain-post-validation
- ts=2026-02-16T00:39:58.344549Z source_id=obs-git-status-003958 source_hash=git-status-short-manager-checkpoint
- ts=2026-02-16T00:40:52.670889Z source_id=obs-git-status-004052 source_hash=git-status-short-clean-before-loop
- ts=2026-02-16T00:41:22.272712Z source_id=obs-git-status-004122 source_hash=git-status-short-branch-after-merge-queue
- ts=2026-02-16T00:42:20.193799Z source_id=obs-git-status-004220 source_hash=git-status-porcelain-pre-validation-loop
- ts=2026-02-16T00:42:34.324817Z source_id=obs-git-status-004234 source_hash=git-status-porcelain-recheck
- ts=2026-02-16T00:43:08.037280Z source_id=obs-git-status-004308 source_hash=git-status-short-post-pytest-failure
- ts=2026-02-16T00:43:41.240248Z source_id=obs-git-status-004341 source_hash=git-status-porcelain-post-ship-check
- ts=2026-02-16T00:45:30.426908Z source_id=obs-git-status-004530 source_hash=git-status-short-clean-checkpoint
- ts=2026-02-16T00:46:06.749373Z source_id=obs-git-status-004606 source_hash=git-status-short-branch-post-merge-queue
- ts=2026-02-16T00:46:30.832828Z source_id=obs-git-status-004630 source_hash=git-status-porcelain-post-validation
- ts=2026-02-16T05:30:45.516621Z source_id=obs-git-status-053045 source_hash=git-status-short-branch-sprint-prep
- ts=2026-02-16T06:22:48.029620Z source_id=obs-git-status-062248 source_hash=git-status-porcelain-checkpoint
- ts=2026-02-16T06:23:23.644571Z source_id=obs-git-status-062323 source_hash=git-status-porcelain
- ts=2026-02-16T06:24:33.632915Z source_id=obs-git-status-062433 source_hash=git-status-porcelain

## Notes
This pattern appears around coordination and validation transitions, reducing state drift risk before next actions.
