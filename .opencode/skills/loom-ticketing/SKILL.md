---
name: loom-ticketing
description: Use loom ticket for ticket creation, status updates, deps, and notes.
license: MIT
compatibility: opencode
metadata:
  created_at: "2026-01-27T17:03:09.731823+00:00"
  updated_at: "2026-01-27T17:03:09.731823+00:00"
  version: "1"
  tags: "tickets,workflow"
---

<!-- BEGIN:compound:skill-managed -->
## Canonical commands

Initialize (creates `.tickets/`):

- `loom ticket init`

Create:

- `loom ticket create "Add foo support" -p 2 -t task --tags "foo,bar"`

List / view:

- `loom ticket list`
- `loom ticket ready`
- `loom ticket show <id>`

Update:

- `loom ticket update <id> --status in_progress`
- `loom ticket update <id> --status closed`

Notes:

- `loom ticket add-note <id> "Found X. Fixed by Y."`

Dependencies:

- `loom ticket dep <id>`
- `loom ticket dep-add <id> <dep-id>`
- `loom ticket dep-rm <id> <dep-id>`

## Best practices

- One “epic” ticket per feature, with task tickets beneath.
- Record decisions and gotchas as notes, not in your head.
- Use deps to make sequencing explicit (and reviewable).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
