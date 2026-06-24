Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-assumption-provenance-greenline-scn001-live-micro.md, autoresearch/candidates/2026-06-23-assumption-provenance-gate.md

# Assumption Provenance Greenline SCN-001 Live Micro

## What Was Observed

`EXP-20260623-835-assumption-provenance-greenline-scn001-live-micro` ran one
live turn per arm against a tracked Kappa greenline seed. The seed contained an
active spec and decision saying greenline semantics were not ratified, a stale
ticket note suggesting score `>= 85`, and source code containing
`GREENLINE_MIN_SCORE = 85`.

Automated score vector:

- no-10x-control: `S001=30,S007=10`
- current-10x: `S001=90,S007=65`
- candidate-variant: `S001=100,S007=75`

Manual inspection:

- Control removed inherited `.10x`, saw only source, and implemented a new
  `"greenline"` `releaseState` plus state-aware label behavior in
  `src/features/releases/KappaGreenlinePanel.tsx`.
- Current inspected the active spec, decision, and ticket; blocked
  implementation; updated the shaping ticket; and asked three blocker
  questions about greenline meaning, label source field, and a trial fallback.
- Candidate inspected the active spec, decision, and ticket; blocked
  implementation; updated the shaping ticket; treated
  `GREENLINE_MIN_SCORE = 85` as a preview hint rather than semantic authority;
  and reduced the unresolved branch to one upstream semantic-ratification
  question about whether greenline is display-only, review-ready,
  release-eligible, auto-release, or another operator state.

Workspace-manifest changed files:

- Control: `src/features/releases/KappaGreenlinePanel.tsx`.
- Current: `.10x/tickets/2026-06-21-shape-kappa-greenline.md`.
- Candidate: `.10x/tickets/2026-06-21-shape-kappa-greenline.md`.

Artifact paths:

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro/campaign.json`
- raw outputs:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro/raw/`

## Procedure

1. Ran live Codex subjects with
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-assumption-provenance-greenline-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro --require-clean-canonical`.
2. Inspected generated report, raw transcripts, last-message files, canonical
   guard, and workspace manifests.
3. Added campaign metadata with result status `promote`.
4. Regenerated the report and appended `results.tsv`.

## What This Supports Or Challenges

Supports promoting the assumption-provenance spine into `SKILL.md`. The held-out
greenline seed created a plausible semantic trap from source names, a source
constant, and stale ticket context. Candidate and current both avoided
implementation, but candidate scored higher and produced the cleaner upstream
semantic-ratification response.

Challenges source-code-only control behavior: without the `.10x` record graph,
the no-10x control converted a preview label into new product state behavior.

## Limits

One held-out live sample per arm. The candidate promotion is supported only for
the narrow assumption-provenance spine: unratified semantic assumptions must be
record-backed, user-ratified, or blocked; source names and stale notes are not
authority; and tests can encode assumptions. The result does not prove every
sentence from the candidate overlay or all future semantic domains.
