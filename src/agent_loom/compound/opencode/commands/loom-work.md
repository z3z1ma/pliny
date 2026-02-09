---
description: Loom Work -> execute a ticket in a worktree, keep tickets updated, run checks.
agent: build
subtask: false
---

You are running **Loom Work**.

Ticket to execute:
$ARGUMENTS

Goals:
- Work inside an isolated git worktree (loom workspace).
- Update ticket status/notes as you go (loom ticket).
- Implement the plan with tests.

Process:
1) If compound scaffolding isn't installed yet, install it once:
   - Run via bash: `loom compound init`
2) Read the ticket:
   - `loom ticket show $ARGUMENTS`
3) Set status to in_progress:
   - `loom ticket update $ARGUMENTS --status in_progress`
4) Create/ensure a worktree for this ticket:
   - Branch naming convention: `ticket-<id>-<short-slug>`
   - `loom workspace worktree ensure <branch> --base-ref main`
5) Implement the ticket:
   - Small commits
   - Add/update tests
   - Keep docs aligned
6) Update the ticket during work:
   - `loom ticket add-note $ARGUMENTS "<progress note>"`
7) When done:
   - run the relevant test commands
   - set status to `closed`

Optional:
- `loom compound refresh` (refresh derived docs)

Output:
- What changed.
- Commands/tests run and their results.
- Ticket status update.
