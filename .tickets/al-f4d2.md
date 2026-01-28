---
"id": "al-f4d2"
"status": "open"
"deps": []
"links": []
"created": "2026-01-31T02:08:27Z"
"type": "feature"
"priority": 3
"assignee": "z3z1ma"
"tags":
- "team"
- "sprint"
- "cli"
- "followup"
"external": {}
---
# Team: sprint lifecycle commands (show/set/clear)

Add explicit commands to inspect and manage sprint state outside of prep-sprint.

## Acceptance Criteria

- Add `loom team sprint show` to print current sprint (name, tag, started_at).
- Add `loom team sprint set` to set/rename sprint and update run.json + CHARTER.md.
- Add `loom team sprint clear` to unset sprint (with a safety prompt/flag if needed).
- Add/adjust tests for run state mutations and CLI parsing.
