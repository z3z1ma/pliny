---
id: 20260211211958-memory-scope-kinds-ignore-unknown-11557cf3
title: Memory scope kinds ignore unknown
tags:
- memory
- scopes
scopes:
- kind: file
  raw: src/agent_loom/memory/scopes.py
  path: src/agent_loom/memory/scopes.py
- kind: command
  raw: "loom memory recall --scope glob:src/**/*.py"
  pattern: "loom memory recall --scope glob:src/**/*.py"
visibility: shared
status: active
created_at: "2026-02-11T21:19:58Z"
updated_at: "2026-02-11T21:19:58Z"
---

Unknown memory scope kinds are ignored as no-ops during parse and normalization. Supported matching lives in [[20260211210414-memory-scope-wildcard-semantics-50ed9a78|20260211210414-memory-scope-wildcard-semantics-50ed9a78]] where wildcard behavior is attached to file:/folder: values only; there is no standalone glob scope kind compatibility path.
