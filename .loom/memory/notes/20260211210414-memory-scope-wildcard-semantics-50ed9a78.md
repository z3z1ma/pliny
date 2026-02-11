---
id: 20260211210414-memory-scope-wildcard-semantics-50ed9a78
title: Memory scope wildcard semantics
tags:
- memory
- scopes
scopes:
- kind: file
  raw: src/agent_loom/memory/scopes.py
  path: src/agent_loom/memory/scopes.py
- kind: command
  raw: "loom memory recall --scope file:src/**/*.py"
  pattern: "loom memory recall --scope file:src/**/*.py"
visibility: shared
status: active
created_at: "2026-02-11T21:04:14Z"
updated_at: "2026-02-11T21:04:14Z"
---

Use wildcard patterns inside file:/folder: scope values instead of a standalone glob: scope kind. During recall matching, treat wildcard-bearing file/folder scopes as fnmatch patterns and keep legacy kind=glob note scopes readable for migration safety. Related: [[20260211210414-memory-scope-kinds-3083d74c|memory-scope-kinds]]
