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
- Append an agent-optimized entry to LOOM_CHANGELOG.

Process:
1) Run `compound_bootstrap`.
2) Gather context:
   - `compound_git_summary()`
   - If a ticket ID was provided, `compound_ticket(argv=["show", "$ARGUMENTS"])`
3) Write 1-5 memory notes using `compound_memory_add`:
   - Scope at least one note to `command:workflows:plan` (use `command="workflows:plan"`)
   - Add file/folder scopes for areas touched (e.g. `file:...`, `folder:...`, from changedFiles in git summary)
4) Propose skill operations as a **CompoundSpec v2** JSON object:
   - Prefer **updating** existing skills over adding near-duplicates.
   - Skills must be procedural: steps, examples, gotchas.
   - Each skill body is markdown **without** frontmatter.
5) Call `compound_apply` with `spec_json` set to the JSON string.
6) Finish with `compound_sync`.

Required output:
- A short “Compound report” section (what we learned).
- The exact JSON spec you applied (for auditability).
