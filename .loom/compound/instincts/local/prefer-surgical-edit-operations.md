---
id: prefer-surgical-edit-operations
title: Prefer surgical edit operations over broad rewrites
trigger: When modifying existing files with Edit/Write and the change is logically small-to-medium
confidence: 0.8200
status: active
domain: workflow
source: local
created_at: 2026-02-13T19:10:38.159235Z
updated_at: 2026-02-15T18:42:48.199834Z
tags: workflow, editing, safety, diff-quality
notes: Repeated large-span edit warnings in one change stream indicate elevated unintended-reformatting risk; smaller targeted edits reduce drift and make intent auditable.
---

## Action
Use narrow, hash-anchored edits at the smallest logical locus; avoid whole-file or very large block replacements unless the intent is genuinely full-file replacement.

## Evidence
- ts=2026-02-15T18:33:21.997523Z source_id=obs-edit-183321 source_hash=edit-warning-5162-lines
- ts=2026-02-15T18:33:47.332746Z source_id=obs-edit-183347 source_hash=edit-warning-4896-lines
- ts=2026-02-15T18:33:57.992716Z source_id=obs-edit-183357 source_hash=edit-warning-1710-lines
- ts=2026-02-15T18:34:13.291720Z source_id=obs-edit-183413 source_hash=edit-warning-298-lines

## Notes
Repeated large-span edit warnings in one change stream indicate elevated unintended-reformatting risk; smaller targeted edits reduce drift and make intent auditable.
