---
"id": "al-df4b"
"status": "closed"
"deps": []
"links": []
"created": "2026-02-09T20:25:19Z"
"type": "feature"
"priority": 1
"assignee": "z3z1ma"
"tags": []
"external": {}
---
# Hydrate wikilinks on memory add/edit and auto-create stubs

When adding/editing memory notes, parse body for [[wikilinks]]. Normalize each link target to a slug, resolve to an existing note id (timestamped ids), or auto-create a stub note if missing. Rewrite the originating note so wikilinks point at ids (keeping display text via alias) and return a machine-readable mapping of rewrites/created notes. Also add  as an alias of .

## Acceptance Criteria

- `loom memory add` rewrites `[[Concept]]` to `[[<note-id>|Concept]]` when Concept resolves
- If Concept is missing, it auto-creates a stub note (same visibility as the source note) and rewrites links to the new id
- `loom memory edit` does the same for edited body content (including append/body override)
- Response payload includes `hydration` info with `rewrites`, `created_notes`, and `ambiguous`
- `loom memory update` behaves as an alias of `loom memory edit`
- Links inside fenced code blocks are not rewritten
- Tests cover creation + reuse + rewrite and update alias parsing

## Notes

**2026-02-09T20:32:38Z**

Implemented wikilink hydration on memory writes.

Changes:
- `loom memory add` and `loom memory edit` now scan the note body for `[[wikilinks]]` (excluding fenced code blocks).
- Each target is normalized to a slug, resolved to an existing note id when possible, otherwise a stub note is auto-created (same visibility as the source note).
- The source note body is rewritten to point at canonical ids using alias form: `[[<id>|Display]]`.
- Command JSON responses now include `hydration` with `rewrites`, `created_notes`, and `ambiguous`.
- Added `loom memory update` as an alias of `edit` (and ensured runtime dispatch handles it).

Tests: added `tests/test_memory_link_hydration.py` and updated golden validate expectations (missing wikilinks now become stub notes).
