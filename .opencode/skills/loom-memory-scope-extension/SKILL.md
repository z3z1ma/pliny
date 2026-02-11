---
name: loom-memory-scope-extension
description: Procedure for changing Loom memory scope syntax/kinds without parser drift, dead paths, or UX/test mismatch.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-11T21:21:38.402529Z"
  source_episode_ids: "883055ed0f173f797d74a5673db40cf642b8191663f6ef312188b017e1d17914,517a7d951e2d4ae1ee98b051a0d26883aa07cc0ac86eccf1300d39920d222962,de39f751f660e27dd86ac6a3f4e9fd7bf4cbc258fdb56bb916aded03026b05fb"
  source_instinct_ids: "scope-kind-explicit-prefixes,scope-normalize-paths-cautiously,scope-roundtrip-contract,scope-validation-errors-high-signal,centralize-scope-validation-and-normalization,memory-scope-contract-sync,scope-glob-requires-edge-coverage,memory-scope-change-is-cross-layer,remove-stale-scope-paths-immediately,scope-syntax-migration-needs-compat-tests,ship-scope-ux-with-doc-and-skill-sync"
  tags: "docs-sync,memory,procedure,scope,testing"
  updated_at: "2026-02-11T21:21:38.402529Z"
  version: "3"
---
<!-- BEGIN:compound:skill-managed -->
# loom-memory-scope-extension

Purpose: change Loom memory scope behavior safely across parser, runtime, docs, and UX tests.

When to use:
- Adding a new scope kind.
- Changing scope syntax (for example introducing or tightening `glob:` forms).
- Deprecating/removing legacy scope input forms.

Procedure:
1. Define the contract first.
   - Specify accepted scope inputs, normalization rules, and invalid forms.
   - Keep one canonical representation after parsing.

2. Update core scope plumbing together.
   - `src/agent_loom/memory/scopes.py`: parse + normalize + validation.
   - `src/agent_loom/memory/constants.py`: scope identifiers/enums.
   - `src/agent_loom/memory/core.py`: write-time scope handling.
   - `src/agent_loom/memory/recall.py`: read/filter behavior.

3. Remove dead legacy behavior.
   - Delete obsolete branches and compatibility shims once replacement behavior is in place.
   - Ensure there is a single active parser path per scope form.

4. Lock behavior with focused tests.
   - Add/extend `tests/test_memory_scope_glob.py` for:
     - valid new syntax,
     - legacy compatibility (if intentionally retained),
     - normalization outputs,
     - invalid/ambiguous inputs.

5. Sync user-facing guidance.
   - Update `src/agent_loom/memory/README.md` examples and wording to match exact accepted syntax.

6. Sync distributed skill copy.
   - If `.opencode/skills/loom-memory-scope-extension/SKILL.md` changes, mirror it at `src/agent_loom/compound/opencode/skills/loom-memory-scope-extension/SKILL.md`.

Validation gates:
- `uv run basedpyright`
- `uv run ruff check .`
- `uv run pytest tests/test_memory_scope_glob.py`
- Run broader `uv run pytest` when scope behavior touches shared memory flows.

Done criteria:
- Parser/runtime/docs/tests agree on accepted scope syntax.
- No legacy dead branches remain.
- Skill and distributed copy are in sync.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
