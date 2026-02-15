# INSTINCTS

## Active instincts (grouped by domain)

### workflow

- **prefer-surgical-edit-operations** (86%) [workflow, editing, safety, diff-quality]
  - Trigger: When modifying existing files with Edit/Write and the change is logically small-to-medium
  - Action: Use narrow, hash-anchored edits at the smallest logical locus; avoid whole-file or very large block replacements unless the intent is genuinely full-file replacement.
  - Source: local
- **maintain-todo-state-throughout-execution** (83%) [workflow, planning, tracking, discipline]
  - Trigger: When work spans multiple edits, validations, and checkpoints
  - Action: Create a todo list early, keep exactly one in-progress item, and update todo state immediately after each major step or validation milestone.
  - Source: local
- **recover-edit-after-hash-mismatch** (76%) [workflow, editing, concurrency, recovery]
  - Trigger: When Edit reports lines changed since last read or asks for updated LINE:HASH anchors
  - Action: On Edit hash-mismatch failure, stop mutation flow, re-read the affected region to obtain fresh LINE:HASH anchors, then retry a minimal targeted edit with updated anchors.
  - Source: local
- **validate-focused-tests-before-full-suite** (74%) [workflow, testing, iteration, validation]
  - Trigger: When implementing or debugging changes scoped to a specific module or harness
  - Action: Run targeted pytest files for the area being changed until green, then run repository-wide lint/type/test gates.
  - Source: local
- **check-working-tree-with-git-status** (62%) [workflow, git, state-awareness, safety]
  - Trigger: Before resuming edits or after tool activity that may change repository state
  - Action: Run `git status --porcelain` at key checkpoints to confirm current working tree state before proceeding with additional edits or commands.
  - Source: local

## Notes

- Instincts are the pre-skill layer: small, repeatable heuristics.
- Promote stable instincts into harness-native skills, commands, and agents when warranted.
