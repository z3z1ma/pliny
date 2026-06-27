Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-noisy-retrospective-routing-scn012-live-micro.md

# Noisy Retrospective Routing Result Evidence

## What Was Observed

Ran `EXP-20260625-982-noisy-retrospective-routing-scn012-live-micro` with three
live Codex subject arms.

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/182-noisy-retrospective-routing-scn012-live-micro/`

Canonical guard:

- `unchanged_during_run: true`
- changed canonical paths: none

Score vectors:

- no-10x-control: `S002=45`, `S006=55`
- current-10x: `S002=70`, `S006=85`
- candidate-variant: `S002=70`, `S006=85`

Current `SKILL.md` arm changed:

- `.10x/evidence/2026-06-25-settlement-reconciliation-child-test-output.md`
- `.10x/evidence/2026-06-25-settlement-reconciliation-closure-coherence.md`
- `.10x/knowledge/settlement-reconciliation-vocabulary.md`
- `.10x/reviews/2026-06-25-settlement-reconciliation-child-review.md`
- `.10x/skills/settlement-reconciliation-replay-tests.md`
- `.10x/tickets/2026-06-25-historical-fx-rounding-tolerance-coverage.md`
- `.10x/tickets/done/2026-06-25-add-settlement-reconciliation-preview.md`
- `.10x/tickets/done/2026-06-25-settlement-reconciliation-parent.md`
- `.claude/skills/settlement-reconciliation-replay-tests/SKILL.md`

Current behavior details:

- Created a project skill for settlement reconciliation replay tests using
  tracked NDJSON fixtures, frozen date `2026-04-30`, and offline processor
  replay adapter.
- Mirrored the skill under `.claude/skills/`.
- Created knowledge for `settlementRef` and `pending_release` vocabulary.
- Opened a blocked follow-up for historical FX rounding tolerance coverage.
- Did not promote the `nr` alias, one-off `--runInBand`, laptop load, or Mara
  log preference into skills or knowledge.
- Recorded closure coherence and moved the child and parent tickets to
  `tickets/done/`.
- Did not edit implementation files.

Candidate-variant was materially equivalent. no-10x-control had `.10x` removed
by control isolation and could not exercise retrospective routing over the seed
record graph.

## Procedure

1. Created the tracked seed workspace
   `autoresearch/trial-seeds/noisy-retrospective-routing/`.
2. Registered the experiment
   `.10x/research/2026-06-25-noisy-retrospective-routing-scn012-live-micro.md`.
3. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-noisy-retrospective-routing-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/182-noisy-retrospective-routing-scn012-live-micro --require-clean-canonical`.
4. Read `report.md`, `canonical_guard.json`, raw transcripts, workspace
   manifests, generated records, and closure tickets.

## What This Supports Or Challenges

Supports that current `SKILL.md` can route noisy retrospective learning into the
right durable record types without creating skills or knowledge for local
one-off observations.

Challenges the Trust Level 1 S002 floor failure for this scenario; manual
inspection found the expected records and closure behavior.

## Limits

This remains a single-turn closure retrospective. It does not prove the same
quality across a longer execution window with multiple agents updating records
over time.
