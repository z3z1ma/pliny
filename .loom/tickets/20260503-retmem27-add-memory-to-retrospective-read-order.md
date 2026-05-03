---
id: ticket:retmem27
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T06:20:11Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-third-pass-follow-up-validation
external_refs: {}
depends_on:
  - ticket:shipacc1
---

# Summary

Add `loom-memory` to retrospective read order when memory promotion or pruning is
possible.

# Context

Retrospective already coordinates memory updates for support-only continuity, but
its read order does not direct operators to `loom-memory` when memory is involved.

# Why Now

Retrospective should not leave memory as the only source of promoted truth or fail
to prune stale support context.

# Scope

- Add `loom-memory/SKILL.md` or equivalent memory-skill cue to retrospective read
  order when memory promotion/pruning is possible.
- Preserve memory as support recall, not canonical truth.

# Out Of Scope

- Do not make memory a canonical owner layer.
- Do not create new memory lifecycle requirements.

# Acceptance Criteria

- ACC-001: Retrospective read order includes memory when memory context may need
  promotion, pointer replacement, or pruning.
- ACC-002: Guidance preserves memory as support-only recall.
- ACC-003: Ticket closure remains owned by ticket acceptance, not retrospective or
  memory.
- ACC-004: Evidence records targeted retrospective/memory searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-028`
- `ticket:retmem27#ACC-001`
- `ticket:retmem27#ACC-002`
- `ticket:retmem27#ACC-003`
- `ticket:retmem27#ACC-004`
- `ticket:retmem27#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-028` | pending | pending | open |
| `ticket:retmem27#ACC-001` | pending | pending | open |
| `ticket:retmem27#ACC-002` | pending | pending | open |
| `ticket:retmem27#ACC-003` | pending | pending | open |
| `ticket:retmem27#ACC-004` | pending | pending | open |
| `ticket:retmem27#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-retrospective/SKILL.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: retrospective memory read-order cue.
Write boundary: retrospective skill read-order guidance only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, memory read-order observations, and
critique recommendation.

# Evidence

Expected: targeted searches for `loom-memory`, memory promotion/pruning, support
recall, ticket closure boundary, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: retrospective promotion can affect support recall and closure
follow-through.

Required critique profiles:

- memory-boundary
- retrospective-boundary
- operator-clarity

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Pending after critique.

# Wiki Disposition

Pending retrospective decision after critique.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

- `ticket:shipacc1`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass secondary polish finding.
