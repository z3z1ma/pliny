---
name: loom-memory-wikilink-hydration
description: Procedure for making Loom memory writes hydrate `[[wikilinks]]` deterministically, with stable UX tests.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-09T20:36:30.408023Z"
  source_episode_ids: "e4839371bc5f19fceb720ecfddf70204dd97ec7a826c7875562727706e171b17"
  source_instinct_ids: "hydrate-wikilinks-on-memory-write,memory-golden-tests-for-ux"
  tags: "cli,loom,memory,python,tests,wikilinks"
  updated_at: "2026-02-09T20:36:30.408023Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Loom Memory Wikilink Hydration

## Goal
When a memory note is written (create/update), `[[wikilinks]]` are resolved in the write path so recall/backlinks/search behave consistently and deterministically.

## When to use
- You add/modify `loom memory add/update` behavior.
- You change parsing/serialization in `src/agent_loom/memory/*`.
- You introduce any new metadata derived from note content (links, tags, scopes).

## Procedure
1. Identify the write entrypoint(s)
   - Locate the CLI command handler and the core function that persists a note.
   - Ensure all write paths (create and update) flow through one hydration function.

2. Define the hydration contract
   - Parse the note body for `[[wikilinks]]`.
   - Normalize link tokens consistently (trim whitespace, keep case rules consistent with existing behavior).
   - Decide what “resolution” means:
     - If a link points to an existing note-id, attach that id.
     - If it points to a title/slug and you support implicit creation, create a referenced note-id deterministically.
   - Persist the hydrated link set (and any necessary mapping) as part of the stored note model.

3. Keep it deterministic
   - Stable ordering of links (e.g., sorted by normalized token) before persisting or rendering.
   - Avoid time-dependent or path-dependent behavior in hydration.

4. Update user-visible behaviors
   - Ensure `loom memory recall` and related commands reflect hydrated links consistently.
   - If output format changes, update tests to match the intended UX (not internal implementation details).

5. Add/adjust a golden UX test
   - Add a fixture note with multiple wikilinks, including edge cases (duplicates, whitespace, mixed casing if supported).
   - Assert the exact CLI output expected for the changed scenario.
   - Keep the fixture small and deterministic; avoid brittle snapshots of unrelated output.

6. Gate checks
   - Run: `uv run ruff check .`
   - Run: `uv run basedpyright`
   - Run: `uv run pytest`

## Done means
- Wikilinks are hydrated on write for all paths.
- Output and behavior are deterministic.
- Golden test(s) cover the precise UX delta.
- Ruff + basedpyright + pytest pass.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
