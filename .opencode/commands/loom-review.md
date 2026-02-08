---
description: Loom Review -> multi-angle review before merge, record findings to tickets.
agent: build
subtask: false
---

You are running **Loom Review**.

Ticket:
$ARGUMENTS

Goals:
- Review changes for correctness, security, performance, and docs.
- Record required follow-ups back into the ticket.

Process:
1) If compound scaffolding isn't installed yet, install it once:
   - Run via bash: `loom compound init`
2) Gather context:
   - `loom ticket show $ARGUMENTS`
   - Run via bash: `git status --porcelain` and `git diff --stat`
   3) If the OpenCode `task` tool is available, run three subreviews (subagents):
    - agent: `loom-review-quality`
    - agent: `loom-review-security`
    - agent: `loom-review-docs`
   Provide them the diff summary + ticket details.
    If `task` is not available, do a single-agent review with those lenses.
4) Synthesize findings into:
   - must-fix
   - should-fix
   - nice-to-have
5) Update the ticket:
   - add notes
   - create new tickets if issues are substantial

Optional:
- `loom compound refresh` (refresh derived docs)

Output:
- Review summary.
- Concrete, prioritized findings.
- Ticket updates performed.
