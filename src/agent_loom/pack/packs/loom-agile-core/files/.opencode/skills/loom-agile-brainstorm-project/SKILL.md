---
name: loom-agile-brainstorm-project
description: Brainstorm project direction and pick concrete next steps.
license: MIT
compatibility: opencode
---

## Outcomes
- A short list of viable directions
- A recommended direction (with why)
- The next 1-3 concrete steps

## Inputs
- Ticket id (recommended)
- Any constraints (time, budget, platform, compliance)

## Procedure
1) Anchor the work
   - If there is no ticket: `loom ticket create "<title>" --status in_progress`
   - If there is a ticket: `loom ticket show <id>`

2) Frame the problem
   - What is the user trying to achieve?
   - Who is it for?
   - What is success (measurable)?

3) Generate options (3-7)
   - Include one conservative option and one bold option.
   - Keep options mutually distinct.

4) Evaluate and narrow
   - Score each option on impact, feasibility, risk.
   - Pick one recommendation.

5) Produce next steps
   - Choose one of:
     - `/loom-agile-create-brief <id>`
     - `/loom-agile-research <id>`
     - `/loom-agile-create-prd <id>`

6) Update the ticket
   - `loom ticket add-note <id> "Options: ... | Recommend: ... | Next: ..."`
