---
description: Loom Agile help (route to the right workflow)
---

You are running Loom Agile Help.

Goal: route the user to the smallest next workflow and keep the work anchored in Loom.

1) Ensure there is a Loom ticket.
   - If the user has a ticket id: `loom ticket show <id>`
   - Otherwise: `loom ticket create "<short title>" --status in_progress`

2) Ask 1-3 targeted questions if intent is unclear.

3) Choose the next command and output the exact slash command:
- Brainstorming a new project: `/loom-agile-brainstorm-project <ticket-id>`
- Need research: `/loom-agile-research <ticket-id>`
- Need a brief: `/loom-agile-create-brief <ticket-id>`
- Need a PRD: `/loom-agile-create-prd <ticket-id>`
- Need to validate/edit a PRD: `/loom-agile-validate-prd <ticket-id>` or `/loom-agile-edit-prd <ticket-id>`
- Need architecture: `/loom-agile-create-architecture <ticket-id>`
- Need epics/stories: `/loom-agile-create-epics-and-stories <ticket-id>`
- Ready to implement: `/loom-agile-dev-story <ticket-id>` (or `/loom-agile-quick-dev <ticket-id>`)
- Need code review: `/loom-agile-code-review <ticket-id>`
- Drifted / needs replan: `/loom-agile-correct-course <ticket-id>`

4) Update the ticket with the chosen next step:
   - `loom ticket add-note <ticket-id> "Next: <command> (why)"`
