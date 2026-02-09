---
name: loom-agile-edit-prd
description: Apply PRD edits based on feedback while preserving intent.
license: MIT
compatibility: opencode
---

## Procedure
1) Identify the feedback source
   - user message
   - review notes
   - implementation constraints discovered later

2) Apply edits
   - Preserve original goals unless explicitly changed
   - Update scope + acceptance criteria accordingly
   - Keep open questions current

3) Summarize delta
   - What changed?
   - Why?

4) Persist
   - `loom ticket add-note <id> "PRD edited: <what changed>"`
