Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/2026-06-23-design-real-autoresearch-candidate.md

# Real Autoresearch Candidate Artifacts

## What Was Observed

Two experimental candidate artifacts exist outside canonical `SKILL.md`:

- `autoresearch/candidates/2026-06-23-campaign-status-metadata.md`
- `autoresearch/candidates/2026-06-23-retrospective-follow-up-capture.md`

The candidate manifest registers both with `promotion` set to `manual-only`:

- `autoresearch/candidates/candidates.json`

Digest check:

```text
SKILL.md length=35614 sha256=21e0c2c7b677e9bf5db20565a07cf70e0d3cd719ab5fe213f3560ab8ba227f5e
autoresearch/candidates/2026-06-23-campaign-status-metadata.md length=2509 sha256=4ab02fe3f19ece326bea8759cdb057e26ed152e588e27c123230cb0ca88c2bc7
autoresearch/candidates/2026-06-23-retrospective-follow-up-capture.md length=2041 sha256=607613ae2c1c43bcc329edc68145749909259cf5e381be6d8be0a79d457f6164
```

The first candidate targets campaign-level verdict metadata for null,
confounded, backfire, inconclusive, and promotion-relevant findings. It names
expected movement for S004, S006, and S008 and covers SCN-013, SCN-014, SCN-015,
SCN-008, and SCN-009.

The second candidate targets retrospective follow-up capture before closing
major work. It names expected movement for S006, S007, and S008 and covers
SCN-009, SCN-012, SCN-008, and SCN-013.

Both candidate records state expected failure modes and explicitly forbid direct
canonical `SKILL.md` mutation without a separate campaign, evidence, review, and
human promotion decision.

## Procedure

1. Read the first calibration campaign evidence and follow-up tickets.
2. Created candidate artifacts for two concrete weaknesses exposed by that
   campaign: missing campaign verdict metadata and loss of unresolved follow-up
   work at closure.
3. Registered both candidates in `autoresearch/candidates/candidates.json`.
4. Compared file lengths and SHA-256 hashes against canonical `SKILL.md`.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/2026-06-23-design-real-autoresearch-candidate.md#AC-001`
- `.10x/tickets/2026-06-23-design-real-autoresearch-candidate.md#AC-002`
- `.10x/tickets/2026-06-23-design-real-autoresearch-candidate.md#AC-003`
- `.10x/tickets/2026-06-23-design-real-autoresearch-candidate.md#AC-004`

This challenges any claim that autoresearch is still limited to a null
placeholder candidate artifact.

## Limits

The candidates are designs and instruction overlays only. This evidence does
not show live behavior improvement, scorer uplift, promotion readiness, or
canonical instruction correctness.
