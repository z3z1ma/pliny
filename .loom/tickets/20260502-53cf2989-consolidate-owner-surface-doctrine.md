---
id: ticket:53cf2989
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T08:46:28Z
updated_at: 2026-05-02T11:05:21Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  initiative:
    - initiative:skills-corpus-protocol-sharpening
  research:
    - research:skills-corpus-council-review
  evidence:
    - evidence:skills-corpus-council-review
    - evidence:owner-surface-consolidation-validation
  critique:
    - critique:owner-surface-consolidation-review
  packet:
    - packet:ralph-ticket-53cf2989-20260502T105317Z
  plan:
    - plan:skills-corpus-protocol-sharpening
  supersedes:
    - ticket:3uv5l5fh
external_refs: {}
depends_on:
  - ticket:4e8ebe92
---

# Summary

Consolidate duplicated atlas, retrospective, spike/sketch, and skill metadata
doctrine under the owner skill that should teach each shape.

# Context

The council found several duplication hotspots. Atlas guidance appears across
codemap and wiki surfaces. Retrospective mechanics are spread between records and
retrospective guidance. Spike/sketch variants appear in research and spike
surfaces. Skill metadata conventions need an explicit owner in skill authoring.

# Why Now

Duplication makes the corpus harder to keep perfect. This slice should reduce
drift by assigning each repeated doctrine area one clear owner surface and
replacing duplicate detail with pointers where appropriate.

# Scope

- Make atlas page shape canonical in the wiki surface, then point codemap guidance
  to that owner shape while preserving codemap's evidence/research/wiki route.
- Move or point retrospective mechanics to `loom-retrospective`, keeping
  `loom-records` focused on shared grammar and validation.
- Let `loom-research` define spike/sketch as research variants at a high level;
  let `loom-spike` own procedural workflow detail.
- Tighten `loom-skill-authoring` metadata guidance for `skill_kind`,
  `compatibility`, activation descriptions, and skill frontmatter expectations.
- Preserve useful domain nuance before deleting or shortening duplicated text.

# Non-goals

- Do not remove doctrine merely because it is repeated; first make sure the owner
  surface contains the needed instruction.
- Do not change atlas, retrospective, spike, or sketch into new canonical layers.
- Do not rewrite all skill metadata by hand unless the owner guidance requires a
  minimal consistency fix.
- Do not update examples broadly; create follow-up work if fixtures become stale.

# Acceptance Criteria

- ACC-001: Atlas shape has one clear owner surface, with codemap pointing to it
  rather than teaching a competing full shape.
- ACC-002: Retrospective workflow mechanics are owned by `loom-retrospective`, with
  `loom-records` retaining only shared grammar or pointer guidance.
- ACC-003: Spike/sketch guidance distinguishes research-owned truth from
  spike-owned workflow procedure without duplicating full instructions.
- ACC-004: `loom-skill-authoring` defines or explicitly leaves open `skill_kind`,
  `compatibility`, and related metadata conventions.
- ACC-005: Targeted searches show no obvious stale duplicate doctrine left in the
  touched surfaces.

# Coverage

Covers:

- `initiative:skills-corpus-protocol-sharpening#OBJ-004`
- `research:skills-corpus-council-review#CLAIM-008`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-protocol-sharpening#OBJ-004` | `evidence:owner-surface-consolidation-validation` | `critique:owner-surface-consolidation-review` | supported |
| `research:skills-corpus-council-review#CLAIM-008` | `evidence:skills-corpus-council-review`; `evidence:owner-surface-consolidation-validation` | `critique:owner-surface-consolidation-review` | supported |

# Execution Notes

This is a consolidation pass. It should make owner boundaries clearer without
turning pointers into vague cross-references that force future agents to chase too
many files.

# Blockers

None. Dependency `ticket:4e8ebe92` is closed.

# Next Move / Next Route

Closed. Continue with the next sequenced plan ticket, `ticket:cdf664af`.

# Ralph Readiness

Bounded iteration:

Consolidate duplicated atlas, retrospective, spike/sketch, and metadata doctrine.

Write boundary:

- `skills/loom-wiki/**`
- `skills/loom-codemap/**`
- `skills/loom-retrospective/**`
- `skills/loom-records/**`
- `skills/loom-research/**`
- `skills/loom-spike/**`
- `skills/loom-skill-authoring/**`

Likely verification posture:

Observation-first structural validation.

Expected output contract:

- changed files,
- owner surface chosen for each duplicated doctrine area,
- removed/replaced duplicate wording summary,
- validation output.

# Evidence

Recorded:

- `evidence:owner-surface-consolidation-validation`
- `git diff --check` passed with no output.
- Targeted searches confirmed wiki-owned atlas shape with codemap pointer,
  retrospective mechanics in `loom-retrospective` with records retaining shared
  grammar, research/spike split, skill-authoring metadata conventions, and no
  obvious stale duplicate full-shape sections in touched surfaces.

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:

This changes workflow doctrine placement and could lose nuance if consolidation is
too aggressive.

Required critique profiles:

- operator-clarity
- routing-safety

Findings:

All findings resolved in `critique:owner-surface-consolidation-review`.

Disposition status: complete

Deferral / not-required rationale:

Not deferred. Oracle critique is recorded in
`critique:owner-surface-consolidation-review`.

# Wiki Disposition

Deferred intentionally. The accepted consolidation guidance lives in the owner
skill surfaces. No separate wiki page is needed for this ticket; the final
corpus-wide validation ticket may still choose broader wiki promotion.

# Acceptance Decision

Accepted by: OpenCode parent agent

Accepted at: 2026-05-02T11:05:21Z

Basis: Ralph packet `packet:ralph-ticket-53cf2989-20260502T105317Z`, validation
evidence `evidence:owner-surface-consolidation-validation`, and final oracle
critique `critique:owner-surface-consolidation-review` with all findings
resolved.

Residual risks: Validation targeted the touched product surfaces and did not
exhaustively audit every example fixture or unrelated skill; final corpus-wide
validation remains owned by `ticket:cdf664af`.

# Dependencies

- `ticket:4e8ebe92`

# Journal

- 2026-05-02T08:46:28Z: Split from cancelled broad ticket `ticket:3uv5l5fh` as
  the owner-surface consolidation slice.
- 2026-05-02T10:53:18Z: Started Ralph iteration
  `packet:ralph-ticket-53cf2989-20260502T105317Z` for owner-surface doctrine
  consolidation.
- 2026-05-02T10:58:16Z: Moved to review after Ralph implementation and structural
  validation.
- 2026-05-02T11:05:21Z: Accepted and closed after oracle critique findings were
  resolved, evidence was refreshed, and retrospective disposition was recorded.
