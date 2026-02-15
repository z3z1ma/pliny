---
id: prefer-surgical-edit-operations
title: Prefer surgical edit operations over broad rewrites
trigger: When modifying existing files with Edit/Write and the change is logically small-to-medium
confidence: 0.8600
status: active
domain: workflow
source: local
created_at: 2026-02-13T19:10:38.159235Z
updated_at: 2026-02-15T21:05:27.994617Z
tags: workflow, editing, safety, diff-quality
notes: Large multi-hundred/ thousand-line edit warnings recur in this stream and were followed by lint/type cleanup, indicating safer progress comes from tighter-scoped edits.
---

## Action
Use narrow, hash-anchored edits at the smallest logical locus; avoid whole-file or very large block replacements unless the intent is genuinely full-file replacement.

## Evidence
- ts=2026-02-15T18:33:21.997523Z source_id=obs-edit-183321 source_hash=edit-warning-5162-lines
- ts=2026-02-15T18:33:47.332746Z source_id=obs-edit-183347 source_hash=edit-warning-4896-lines
- ts=2026-02-15T18:33:57.992716Z source_id=obs-edit-183357 source_hash=edit-warning-1710-lines
- ts=2026-02-15T20:57:02.378747Z source_id=obs-edit-205702 source_hash=edit-warning-226-lines-5-ops
- ts=2026-02-15T20:57:02.498578Z source_id=obs-edit-205702b source_hash=edit-warning-162-lines-1-op
- ts=2026-02-15T21:02:07.045559Z source_id=obs-edit-210207 source_hash=edit-warning-1861-lines-2-ops
- ts=2026-02-15T21:02:39.583635Z source_id=obs-edit-210239 source_hash=edit-warning-2477-lines-3-ops
- ts=2026-02-15T21:03:02.862007Z source_id=obs-edit-210302 source_hash=edit-warning-1622-lines-3-ops
- ts=2026-02-15T21:04:44.597215Z source_id=obs-edit-210444 source_hash=edit-warning-986-lines-2-ops

## Notes
Large multi-hundred/ thousand-line edit warnings recur in this stream and were followed by lint/type cleanup, indicating safer progress comes from tighter-scoped edits.
