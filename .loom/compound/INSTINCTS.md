# INSTINCTS

## Active instincts (grouped by domain)

### testing

- **reset-team-role-env-for-full-pytest** (70%) [testing, pytest, environment, team, reliability]
  - Trigger: When running repository-wide `uv run pytest` from team-managed or worker harness contexts
  - Action: Before running repository-wide `uv run pytest`, clear role-scoped environment (`LOOM_TEAM_ROLE=` or `unset LOOM_TEAM_ROLE`) so permission-gated team tests execute under neutral context.
  - Source: local
- **iterate-basedpyright-until-clean** (68%) [testing, type-checking, basedpyright, debugging, iteration]
  - Trigger: After semantic edits in typed Python modules when `uv run basedpyright` reports errors
  - Action: When basedpyright fails, inspect reported locations, apply targeted edits, and re-run `uv run basedpyright` in a tight loop until it reports zero errors before moving to downstream gates.
  - Source: local

### workflow

- **prefer-surgical-edit-operations** (90%) [workflow, editing, safety, diff-quality]
  - Trigger: When modifying existing files with Edit/Write and the change is logically small-to-medium
  - Action: Use narrow, hash-anchored edits at the smallest logical locus; avoid whole-file or large-block replacements unless the intent is true full-file replacement.
  - Source: local
- **poll-team-inbox-for-acks-and-status** (86%) [workflow, team, inbox, orchestration, acknowledgements]
  - Trigger: While managing an active team run with asynchronous worker updates
  - Action: Use `loom team inbox <team>` repeatedly during active coordination loops to collect worker updates, verify ack transitions, and drive follow-up actions from observed status rather than assumptions.
  - Source: local
- **check-working-tree-with-git-status** (85%) [workflow, git, state-awareness, safety]
  - Trigger: Before resuming edits or after tool activity that may change repository state
  - Action: Run `git status --porcelain` (or `git status --short`) at key checkpoints to confirm current working tree state before proceeding with additional edits or coordination commands.
  - Source: local
- **maintain-todo-state-throughout-execution** (83%) [workflow, planning, tracking, discipline]
  - Trigger: When work spans multiple edits, validations, and checkpoints
  - Action: Create a todo list early, keep exactly one in-progress item, and update todo state immediately after each major step or validation milestone.
  - Source: local
- **recover-edit-after-hash-mismatch** (83%) [workflow, editing, concurrency, recovery]
  - Trigger: When Edit reports lines changed since last read or asks for updated LINE:HASH anchors
  - Action: On Edit hash-mismatch failure, stop mutation flow, re-read the affected region to obtain fresh LINE:HASH anchors, then retry a minimal targeted edit with updated anchors.
  - Source: local
- **validate-focused-tests-before-full-suite** (82%) [workflow, testing, iteration, validation]
  - Trigger: When implementing or debugging changes scoped to a specific module or harness
  - Action: Run targeted pytest files for the area being changed until green, then run repository-wide lint/type/test gates.
  - Source: local
- **wait-on-team-inbox-events-during-manager-loops** (82%) [workflow, team, wait, orchestration, efficiency]
  - Trigger: When managing active team runs and expecting asynchronous worker responses
  - Action: Use `loom team wait <team>` to block for inbox activity, then immediately inspect `loom team inbox <team>` to process and acknowledge resulting messages.
  - Source: local
- **repeat-team-merge-until-queue-state-advances** (77%) [workflow, team, merge-queue, integration, orchestration]
  - Trigger: When integrating worker-delivered branches from a Loom team merge queue
  - Action: Run `loom team merge <team>` in a short loop during integration handoff and use each response state (`sha`, `[queued]`, claimed record) to confirm queue advancement before taking branch-level merge actions.
  - Source: local
- **consult-ticket-cli-help-before-subcommand-use** (76%) [workflow, ticket, cli, discovery, safety]
  - Trigger: When operating ticket commands with uncertain flags, aliases, or argument forms
  - Action: Before mutating ticket state with unfamiliar ticket subcommands, query `loom ticket --help` and relevant subcommand help (`-h`/`--help`) to verify exact syntax and flags, then execute.
  - Source: local

## Notes

- Instincts are the pre-skill layer: small, repeatable heuristics.
- Promote stable instincts into harness-native skills, commands, and agents when warranted.
