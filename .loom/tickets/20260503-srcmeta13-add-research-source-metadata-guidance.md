---
id: ticket:srcmeta13
kind: ticket
status: ready
change_class: documentation-explanation
risk_class: low
created_at: 2026-05-03T01:57:25Z
updated_at: 2026-05-03T01:57:25Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
external_refs: {}
depends_on: []
---

# Summary

Add research source provenance and freshness guidance for external or current
sources.

# Context

Follow-up validation found `skills/loom-research/references/source-handling.md` is
still minimal. It says to name source quality and incomplete evidence, but it does
not give agents enough metadata expectations for external sources, access dates,
freshness, or recheck triggers.

# Why Now

Research records preserve reusable investigation results. When research relies on
external or time-sensitive sources, future agents need to know what was observed,
when it was observed, how reliable it seemed, and when it may need rechecking.

# Scope

- Add source metadata guidance for external/current research sources.
- Cover access date, provenance, source quality, freshness window, and recheck or
  invalidation triggers.
- Keep research as evidence synthesis and recommendations, not a new evidence or
  wiki owner.

# Out Of Scope

- Do not require full raw source dumps in research records.
- Do not add source-fetching automation or external-source validators.
- Do not make research own accepted wiki explanation or ticket acceptance.

# Acceptance Criteria

- ACC-001: Research source-handling guidance names metadata expected for external
  or current sources, including access date and provenance.
- ACC-002: Guidance asks researchers to state source quality, freshness limits, and
  recheck or invalidation triggers when they matter.
- ACC-003: Guidance preserves the distinction between research synthesis,
  observed evidence, accepted wiki explanation, and ticket acceptance.
- ACC-004: Evidence records before/after searches for source metadata, freshness,
  access date, recheck triggers, and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-016`
- `ticket:srcmeta13#ACC-001`
- `ticket:srcmeta13#ACC-002`
- `ticket:srcmeta13#ACC-003`
- `ticket:srcmeta13#ACC-004`
- `ticket:srcmeta13#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-016` | pending | pending | open |
| `ticket:srcmeta13#ACC-001` through `ticket:srcmeta13#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surface is `skills/loom-research/references/source-handling.md`.
Touch `skills/loom-research/SKILL.md` only if read-order wording needs a small
cross-reference adjustment.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: research source provenance and freshness guidance.
Write boundary: research source guidance, this ticket, one evidence record, one
critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `access date`, `freshness`, `source quality`,
`recheck`, `invalidation`, and `git diff --check`.

# Critique Disposition

Risk class: low

Critique policy: mandatory

Policy rationale: user instruction requires oracle critique for every ticket;
source metadata affects future research trust.

Required critique profiles:

- evidence-quality
- operator-clarity
- owner-boundary

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

None.

# Journal

- 2026-05-03T01:57:25Z: Created from follow-up validation after `ticket:wssupp4`.
