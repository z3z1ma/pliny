---
description: Compound → extract reusable patterns into skills + memory, update docs and changelog.
agent: build
subtask: false
---

You are running the **Compound** phase.

Ticket (if applicable):
$ARGUMENTS

This is where we convert “we learned a thing” into **procedural memory**.

Goals:
- Store recallable memory notes (loom memory) so future planning retrieves them automatically.
- Create/update skills under `.opencode/skills/` (and mirror to `.claude/skills/`).
- Update AI-managed blocks in AGENTS + LOOM docs.
- Append an agent-optimized entry to LOOM_ROADMAP.

Process:
1) Run `compound_bootstrap`.
2) Gather context:
   - `compound_git_summary()`
   - If a ticket ID was provided, `loom ticket show $ARGUMENTS`
3) Write 1-5 memory notes using `compound_memo_add`:
   - Scope at least one note to `command:workflows:plan`
   - Add file/folder scopes for areas touched (from changedFiles in git summary)
4) Create/update skills using `compound_skill_upsert`.
5) Create/update instincts using `compound_instinct_upsert` (only if the heuristic is durable).
6) Update doc blocks using `compound_docblock_upsert` (allowed blocks only).
7) Append a short entry using `compound_changelog_append`.
8) Finish with `compound_sync`.

Required output:
- A short “Compound report” section (what we learned).
- A short list of changes applied (skills/instincts/docs/memos).
