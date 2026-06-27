Status: active
Created: 2026-06-23
Updated: 2026-06-25
Parent:
Depends-On: .10x/tickets/2026-06-23-add-ledger-import-preview.md

# Ledger Import Parent

## Scope

Coordinate Ledger import preview closure after child execution.

Included:

- Preserve the reusable fixture replay procedure as the current source skill
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
- Treat superseded research references to
  `.10x/skills/replay-ledger-import-fixtures/SKILL.md` as historical naming
  only.
- Preserve `sourceRef` vocabulary as knowledge.
- Open a bounded follow-up owner for archive malformed-currency coverage.

Excluded:

- Direct parent implementation.
- Archive import code changes.
- Creating speculative `.claude`, `.agents`, or `.opencode` skill mirrors when
  no such harness-native directory exists in this workspace.
- Creating or updating the superseded
  `.10x/skills/replay-ledger-import-fixtures/SKILL.md` path.

## Acceptance Criteria

- Child ticket closure is supported by recorded evidence and active specs.
- Retrospective extraction captures the fixture procedure using the current
  source skill identity
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
- No source skill or mirror is created under the superseded
  `replay-ledger-import-fixtures` identity.
- If no harness-native skills directory exists, the parent records that no
  exposure target is present instead of inventing a mirror directory.

## Progress And Notes

- 2026-06-23: Child executor reported implementation complete.
- 2026-06-23: Evidence and review pass for the child scope.
- 2026-06-25: Active knowledge names
  `.10x/skills/ledger-import-fixture-replay/SKILL.md` as the replacement skill
  identity. The old `replay-ledger-import-fixtures` slug appears only in
  superseded research.
- 2026-06-25: Inspection found no `.claude/skills`, `.agents/skills`, or
  `.opencode/skills` directory in this workspace.

## Blockers

- Awaiting parent closure check and retrospective extraction.
