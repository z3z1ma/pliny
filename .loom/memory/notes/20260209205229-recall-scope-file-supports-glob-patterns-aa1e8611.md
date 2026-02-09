---
id: 20260209205229-recall-scope-file-supports-glob-patterns-aa1e8611
title: "Recall scope file: supports glob patterns"
tags:
- memory
- scopes
scopes:
- kind: file
  raw: src/agent_loom/memory/scopes.py
  path: src/agent_loom/memory/scopes.py
- kind: command
  raw: "loom memory recall --scope file:src/.../*.py"
  pattern: "loom memory recall --scope file:src/.../*.py"
visibility: shared
status: active
created_at: "2026-02-09T20:52:29Z"
updated_at: "2026-02-09T20:52:29Z"
---

You can pass glob patterns via `--scope file:<pattern>` (or `--scope folder:<pattern>`) when recalling memories.

Implementation notes:
- If a file:/folder: scope value contains glob metacharacters (`*`, `?`, `[`), Loom treats it as a glob scope internally (so wildcard file scopes do not trigger file existence validation).
- Scope matching supports context glob scopes against note file/folder scopes.

Example:
- `loom memory recall --scope file:src/agent_loom/memory/*.py --limit 10`
