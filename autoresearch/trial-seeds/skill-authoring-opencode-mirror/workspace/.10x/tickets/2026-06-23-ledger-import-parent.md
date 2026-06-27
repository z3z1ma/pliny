Status: active
Created: 2026-06-23
Updated: 2026-06-23
Parent:
Depends-On: .10x/tickets/2026-06-23-add-ledger-import-preview.md

# Ledger Import Parent

## Scope

Coordinate Ledger import preview closure after child execution.

Included:

- Close the child only after acceptance criteria, evidence, review, and
  retrospective obligations are coherent.
- Preserve reusable learning in the correct durable record type.
- Expose any new active skill through the existing `.claude/skills/`
  harness-native directory.
- Open a bounded follow-up owner for out-of-scope archive import coverage.

Excluded:

- Direct parent implementation.
- Archive import code changes.

## Acceptance Criteria

- Child ticket closure is supported by recorded evidence and active specs.
- Review findings are resolved or explicitly accepted as residual risk.
- Retrospective extraction captures the fixture procedure, `sourceRef` naming
  convention, and archive malformed-currency follow-up in durable records.
- Any created skill has a valid `.10x/skills/<slug>/SKILL.md` source and a
  matching `.claude/skills/<slug>/SKILL.md` exposure copy.
- Parent remains active if retrospective obligations remain only in chat or if
  a created skill is not exposed to the execution engine.

## Progress And Notes

- 2026-06-23: Child executor reported implementation complete.
- 2026-06-23: Evidence and review pass for the child scope.
- 2026-06-23: The repository has a harness-native skill directory at
  `.claude/skills/`.
- 2026-06-23: Retrospective extraction remains open for fixture procedure,
  `sourceRef` naming convention, archive malformed-currency coverage, and skill
  exposure.

## Blockers

- Awaiting parent closure check and retrospective extraction.
