---
name: loom-memory-scope-extension
description: Procedure for adding or changing Loom memory scope kinds without breaking stored data or CLI UX.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-09T20:53:24.282450Z"
  source_episode_ids: "883055ed0f173f797d74a5673db40cf642b8191663f6ef312188b017e1d17914"
  source_instinct_ids: "scope-kind-explicit-prefixes,scope-normalize-paths-cautiously,scope-roundtrip-contract,scope-validation-errors-high-signal"
  tags: "loom,memory,parsing,scopes,testing"
  updated_at: "2026-02-09T20:53:24.282450Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Loom Memory Scope Extension

Goal: add/adjust a memory scope kind with stable parsing, canonical formatting, and low-noise errors.

## Steps

1. Inspect the scope model and parser
- Read `src/agent_loom/memory/scopes.py`.
- Identify: (a) the canonical set of scope kinds, (b) parsing entrypoint(s), (c) formatting/serialization function(s).

2. Add/modify a scope kind
- Implement one canonical string form (what gets stored and displayed).
- Avoid heuristics: require an explicit prefix for the scope kind.
- Keep behavior deterministic (no implicit cwd/FS resolution unless the kind semantics demand it).

3. Enforce strict validation
- On invalid scope strings: raise/return an error that includes the input, the expected prefix/grammar, and at least one valid example.
- Do not silently coerce ambiguous inputs.

4. Roundtrip invariants
- Ensure `parse(scope_str)` + `format(scope_obj)` is stable.
- Ensure `parse(format(scope_obj))` yields an equivalent object.

5. Update call sites
- If CLI accepts scopes, ensure help text and examples match the canonical string form.
- If scopes are persisted, ensure existing persisted values still parse (or provide an explicit migration path).

6. Gates
- Run: `uv run ruff check .`
- Run: `uv run basedpyright`
- Run: `uv run pytest`

## Done when
- One canonical string form exists per scope kind.
- Invalid inputs produce high-signal, testable errors.
- Roundtrip invariants hold and are covered by tests.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
