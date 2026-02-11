---
"id": "al-c9c9"
"status": "review"
"deps": []
"links": []
"created": "2026-02-11T20:56:41Z"
"type": "task"
"priority": 1
"assignee": "z3z1ma"
"tags":
- "memory"
- "scopes"
- "ux"
"external": {}
---
# Memory: remove explicit glob scope kind

Remove dedicated glob scope from memory model. Treat glob patterns as supported values under file/folder scopes during recall matching using fnmatch semantics.

## Notes

**2026-02-11T20:59:59Z**

Found current behavior: file/folder wildcard scopes normalize to kind=glob in scopes.py, and recall uses fnmatch for glob kind. Implementing removal of explicit glob as a user-facing scope kind while keeping file/folder wildcard support and legacy recall matching for existing glob-scoped notes.

**2026-02-11T21:04:04Z**

Implemented removal of user-facing glob scope kind in memory scopes. file:/folder: wildcard paths now stay in their native kinds, explicit glob:... is rejected, and recall still matches legacy note kind=glob scopes via fnmatch against file/folder context. Updated memory cookbook and added regression tests for wildcard recall, explicit glob rejection, and legacy glob note matching. Verified with uv run basedpyright, uv run ruff check ., and uv run pytest tests/test_memory_scope_glob.py tests/test_memory_recall_notes.py tests/test_memory_notes.py.

**2026-02-11T21:19:50Z**

Follow-up change request: removed all remaining legacy glob-scope compatibility. Unknown scope kinds are now ignored (no-op) across parse/normalize/context handling rather than raising. This drops explicit legacy glob-kind matching and keeps wildcard behavior only within file:/folder: path values.

**2026-02-11T21:20:05Z**

Validation: uv run basedpyright; uv run ruff check .; uv run pytest tests/test_memory_scope_glob.py tests/test_memory_recall_notes.py tests/test_memory_notes.py (all passing).

**2026-02-11T21:20:55Z**

Finalized behavior per request: explicit glob scope kind now behaves as unknown and is ignored (no error). Added tests for unknown scope kinds in context and persisted notes; wildcard matching remains on file:/folder:. Re-verified with uv run basedpyright, uv run ruff check ., and uv run pytest tests/test_memory_scope_glob.py.
