---
id: ticket:srcmeta13
kind: ticket
status: closed
change_class: documentation-explanation
risk_class: low
created_at: 2026-05-03T01:57:25Z
updated_at: 2026-05-03T02:55:50Z
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
  packet:
    - packet:ralph-ticket-srcmeta13-20260503T025211Z
  evidence:
    - evidence:research-source-metadata-validation
  critique:
    - critique:research-source-metadata-review
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
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-016` | `evidence:research-source-metadata-validation` | `critique:research-source-metadata-review` | supported |
| `ticket:srcmeta13#ACC-001` through `ticket:srcmeta13#ACC-005` | `evidence:research-source-metadata-validation` | `critique:research-source-metadata-review` | supported |

# Execution Notes

Likely touched surface is `skills/loom-research/references/source-handling.md`.
Touch `skills/loom-research/SKILL.md` only if read-order wording needs a small
cross-reference adjustment.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:driveref9`.

Ralph packet `packet:ralph-ticket-srcmeta13-20260503T025211Z` was consumed in
scope, evidence was recorded, oracle critique passed with no findings, and
acceptance is complete.

# Route Readiness

Acceptance review readiness:

Evidence `evidence:research-source-metadata-validation` and oracle critique
`critique:research-source-metadata-review` support closure with no findings.

# Evidence

Recorded: `evidence:research-source-metadata-validation`.

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

`critique:research-source-metadata-review` - no findings; mandatory oracle
critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Research source metadata and freshness guidance was promoted directly into
  `skills/loom-research/references/source-handling.md`.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched research source-handling reference.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T02:55:50Z
Basis: Ralph packet `packet:ralph-ticket-srcmeta13-20260503T025211Z`; evidence
`evidence:research-source-metadata-validation`; oracle critique
`critique:research-source-metadata-review` with no findings.
Residual risks: guidance is intentionally lightweight and judgment-based; it does
not define a rigid citation schema. Correct use depends on operators recording
source metadata honestly when external or current sources matter.

# Dependencies

None.

# Journal

- 2026-05-03T01:57:25Z: Created from follow-up validation after `ticket:wssupp4`.
- 2026-05-03T02:52:11Z: Marked active and compiled Ralph packet
  `packet:ralph-ticket-srcmeta13-20260503T025211Z` for research source metadata
  and freshness guidance.
- 2026-05-03T02:53:57Z: Ralph iteration
  `packet:ralph-ticket-srcmeta13-20260503T025211Z` completed in scope. Evidence
  recorded in `evidence:research-source-metadata-validation`; next route is
  mandatory oracle critique.
- 2026-05-03T02:55:50Z: Mandatory oracle critique
  `critique:research-source-metadata-review` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
