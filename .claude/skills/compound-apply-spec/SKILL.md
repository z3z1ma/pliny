---
name: compound-apply-spec
description: Write a CompoundSpec v2 JSON payload and apply it via compound_apply to create/update skills and docs.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-27T17:03:09.731823+00:00"
  updated_at: "2026-01-27T17:03:09.731823+00:00"
  version: "1"
  tags: "skills,compounding,schema"
---
<!-- BEGIN:compound:skill-managed -->
## Why this exists

The plugin is deterministic. The agent is not.
So we separate:

- **Agent**: decides what to learn (writes the spec).
- **Tool** (`compound_apply`): validates and applies changes safely.

## CompoundSpec v2

A **single JSON object** matching the v2 schema.

### Top-level shape

- `schema_version`: must be `2`
- `auto`: `{ reason, sessionID }`
- `instincts` (optional):
  - `create[]`: `{ id, title, trigger, action, confidence }`
  - `update[]`: `{ id, confidence_delta, evidence_note }`
- `skills` (optional):
  - `create[]`: `{ name, description, body }`
  - `update[]`: `{ name, description?, body }`
- `docs` (optional):
  - `sync`: boolean
  - `blocks.upsert[]`: `{ file, id, content }`
- `changelog` (optional): `{ note }`

### Output discipline

- Output **only** the JSON object.
- No code fences.
- No commentary.

### Scope discipline

- Only propose changes to skills/instincts/memory notes and AI-managed docs blocks.
- Do **not** propose product-code changes.

### Skill rules

- `name` must match `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`.
- `body` is markdown **without** frontmatter.
- For `skills.update[]`, `body` must be the **entire final managed body** (not a diff/snippet).
- Canonical skill location is `.opencode/skills/<name>/SKILL.md`.

### Repo path rule

When referencing repo files/dirs in markdown, use repo-root-relative paths (no absolute paths).

### Autolearn mode

When responding to a background autolearn prompt:

- Produce the CompoundSpec v2 JSON object.
- **Do not** call `compound_apply` in the same response.

## Apply (interactive use)

1. Produce the CompoundSpec v2 JSON object.
2. Apply it via the tool call:
   - `compound_apply(spec_json="<the JSON string>")`

The tool validates the JSON and applies updates to skills/docs/indexes safely.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
