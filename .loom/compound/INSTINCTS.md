# INSTINCTS

## Active instincts (grouped by domain)

### workflow

- **maintain-todo-state-throughout-execution** (83%) [workflow, planning, tracking, discipline]
  - Trigger: When work spans multiple edits, validations, and checkpoints
  - Action: Create a todo list early, keep exactly one in-progress item, and update todo state immediately after each major step or validation milestone.
  - Source: local
- **prefer-surgical-edit-operations** (82%) [workflow, editing, safety, diff-quality]
  - Trigger: When modifying existing files with Edit/Write and the change is logically small-to-medium
  - Action: Use narrow, hash-anchored edits at the smallest logical locus; avoid whole-file or very large block replacements unless the intent is genuinely full-file replacement.
  - Source: local
- **validate-focused-tests-before-full-suite** (74%) [workflow, testing, iteration, validation]
  - Trigger: When implementing or debugging changes scoped to a specific module or harness
  - Action: Run targeted pytest files for the area being changed until green, then run repository-wide lint/type/test gates.
  - Source: local

## Notes

- Instincts are the pre-skill layer: small, repeatable heuristics.
- Promote stable instincts into harness-native skills, commands, and agents when warranted.
