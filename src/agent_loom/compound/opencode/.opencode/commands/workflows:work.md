---
description: Work → execute a ticket in an isolated worktree (loom workspace), update ticket status/notes (loom ticket).
agent: build
subtask: false
---

You are running the **Work** phase.

Ticket to execute:
$ARGUMENTS

Goals:
- Work inside an isolated git worktree (loom workspace).
- Update ticket status/notes as you go (loom ticket).
- Implement the plan with tests.

Process:
1) Run `compound_bootstrap`.
2) Read the ticket:
   - `compound_ticket(argv=["show", "$ARGUMENTS"])`
3) Set status to in_progress:
   - `compound_ticket(argv=["update", "$ARGUMENTS", "--status", "in_progress"])`
4) Create a worktree for this ticket:
   - Branch naming convention: `ticket-<id>-<short-slug>`
   - Use `compound_workspace(argv=["repo", "worktree", "add", "<branch>"])`
   - NOTE: OpenCode operates in one working directory. After creating the worktree, do the actual code changes in that worktree (often by starting OpenCode in the worktree directory).
5) Implement the ticket:
   - Small commits
   - Add/update tests
   - Keep docs aligned
6) Update the ticket during work:
   - `compound_ticket(argv=["add-note", "$ARGUMENTS", "<progress note>"])`
7) When done:
   - run the relevant test commands
   - set status to `closed`
8) End with `compound_sync` to refresh derived doc sections.

Output:
- What changed.
- Commands/tests run and their results.
- Ticket status update.
