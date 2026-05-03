---
id: evidence:research-source-metadata-validation
kind: evidence
status: recorded
created_at: 2026-05-03T02:53:57Z
updated_at: 2026-05-03T02:53:57Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:srcmeta13
  packet:
    - packet:ralph-ticket-srcmeta13-20260503T025211Z
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  critique:
    - critique:research-source-metadata-review
external_refs: {}
---

# Summary

Observation-first validation for `ticket:srcmeta13`: research source-handling
guidance now names external/current source metadata, access date, provenance,
freshness limits, and recheck/invalidation triggers while preserving owner
boundaries.

# Procedure

Observed at: 2026-05-03T02:53:57Z
Source state: baseline commit `23305565fd7e4af907de38b70c35c940da122410` plus
uncommitted Ralph child diff
Procedure: reviewed the child product diff, ran baseline/current targeted
searches, and ran `git diff --check`
Procedure verdict / exit code: pass; `git diff --check` exited 0 with no output

# Artifacts

Changed file:

- `skills/loom-research/references/source-handling.md`

Baseline search at `2330556`:

```text
2330556:skills/loom-research/SKILL.md:3:description: "Maintain reusable investigations, experiments, evidence synthesis, comparisons, and recommendations. Use when the project needs discovery before commitment, when tradeoffs should remain citable, or when implementation findings deserve a durable record instead of disappearing into chat."
2330556:skills/loom-research/SKILL.md:23:- evidence synthesis
2330556:skills/loom-research/SKILL.md:26:- conclusions and recommendations grounded in evidence
2330556:skills/loom-research/SKILL.md:30:- the project lacks evidence for a decision
2330556:skills/loom-research/SKILL.md:53:- what evidence was gathered
2330556:skills/loom-research/SKILL.md:61:- recommendations are bounded by actual evidence
2330556:skills/loom-research/SKILL.md:70:   source quality matter.
2330556:skills/loom-research/references/source-handling.md:14:When source quality varies, say so.
2330556:skills/loom-research/references/source-handling.md:16:When evidence is incomplete, say so.
2330556:skills/loom-research/references/source-handling.md:22:If the research result becomes accepted understanding that future agents should read first, promote the synthesis into the wiki and link back to the research note.
```

Current search after implementation:

```text
skills/loom-research/SKILL.md:70:   source quality matter.
skills/loom-research/references/source-handling.md:27:- provenance, such as publisher, author, repository, organization, quoted
skills/loom-research/references/source-handling.md:30:- access date for time-sensitive or web sources
skills/loom-research/references/source-handling.md:31:- short note on source quality when reliability, authority, or completeness
skills/loom-research/references/source-handling.md:34:State freshness limits when a conclusion may expire. Name the recheck or
skills/loom-research/references/source-handling.md:35:invalidation trigger when it matters, such as a vendor release, policy change,
skills/loom-research/references/source-handling.md:36:API deprecation, repository ref change, or new contradictory evidence.
skills/loom-research/references/source-handling.md:39:dumps. Observed artifacts and command outputs belong in evidence when they need
skills/loom-research/references/source-handling.md:40:to persist as observations. Accepted explanatory synthesis belongs in the wiki
skills/loom-research/references/source-handling.md:41:after it is settled. Live execution state and ticket acceptance remain owned by
```

Whitespace check:

```text
$ git diff --check
<passed with no output>
```

# Supports Claims

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-016`
- `ticket:srcmeta13#ACC-001`
- `ticket:srcmeta13#ACC-002`
- `ticket:srcmeta13#ACC-003`
- `ticket:srcmeta13#ACC-004`

# Challenges Claims

None.

# Environment

Commit: `23305565fd7e4af907de38b70c35c940da122410` plus uncommitted Ralph child diff
Branch: `main`
Runtime: none; Markdown protocol corpus only
OS: darwin
Relevant config: no app runtime or automated test suite in this repository

# Validity

Valid for: working tree after Ralph child output for `ticket:srcmeta13` and
before oracle critique.
Fresh enough for: structural validation of `ticket:srcmeta13#ACC-001` through
`ticket:srcmeta13#ACC-004`.
Recheck when: research source-handling guidance, research skill read-order,
research/evidence/wiki/ticket ownership boundaries, or ticket acceptance criteria
change again.
Invalidated by: newer edits that remove source metadata, access-date,
freshness/recheck/invalidation, or owner-boundary guidance.
Supersedes / superseded by: None.

# Limitations

This evidence records structural searches, diff review, and whitespace validation
only. It does not establish oracle critique sufficiency, ticket acceptance, or
closure by itself.

# Result

Research source-handling guidance now asks for provenance, access date, source
quality, freshness limits, and recheck/invalidation triggers when external or
current sources matter. The same guidance preserves the distinction between
research synthesis, evidence observations, accepted wiki explanation, and ticket
acceptance. `git diff --check` passed.

# Interpretation

The structural observations support `ACC-001` through `ACC-004`. `ACC-005`
requires the mandatory oracle critique to pass with no unresolved findings.

# Related Records

- `ticket:srcmeta13`
- `packet:ralph-ticket-srcmeta13-20260503T025211Z`
- `critique:research-source-metadata-review`
