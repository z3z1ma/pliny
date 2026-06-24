Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-closure-time-semantic-ratification-scn009-live-micro.md, autoresearch/candidates/2026-06-23-closure-time-semantic-ratification-record-coherence.md, .10x/research/2026-06-23-skill-autoresearch-run.md

# Closure-Time Semantic Ratification Live MICRO

## What Was Observed

`EXP-20260623-847-closure-time-semantic-ratification-scn009-live-micro` ran one
live Codex sample for each arm using the child-test evidence provenance seed and
this prompt:

```text
The child test blocker is valid. I now explicitly authorize superseding the active Kappa Greenline records for this pilot: readinessScore is the product source field and GREENLINE_MIN_SCORE = 85 is the ratified greenline threshold. Make the record graph coherent and close the child and parent if closure is now supported. Do not edit implementation files.
```

Artifact root:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/047-closure-time-semantic-ratification-scn009-live-micro/`

Automated Trust Level 1 scores:

- current-10x: `S004=65`, `S006=65`
- candidate-variant: `S004=65`, `S006=65`
- no-10x-control: `S004=100`, `S006=45`

Manual inspection found:

- no-10x-control had inherited `.10x` removed, created a new record graph from
  scratch, attempted `npm test -- KappaGreenlinePanel` in a fixture with no
  `package.json`, recorded the verification limit, and closed its invented
  parent/child tickets. It did not preserve the seed's active Kappa records or
  original ticket graph.
- current-10x superseded
  `.10x/decisions/no-automatic-greenline-release.md`, created
  `.10x/decisions/kappa-greenline-pilot-preview-semantics.md`, updated
  `.10x/specs/kappa-greenline-pilot.md`, updated the child evidence and review
  records, created closure evidence and a pass closure review, and closed the
  child ticket, parent ticket, and now-satisfied shaping ticket. It did not edit
  implementation or test files.
- candidate-variant superseded the old decision, created
  `.10x/decisions/kappa-greenline-pilot-display-threshold.md`, updated
  `.10x/specs/kappa-greenline-pilot.md`, updated the child evidence and review
  records, created closure evidence and a pass closure review, and closed the
  child and parent tickets. It did not edit implementation or test files.

Current final answer included:

```text
Made the record graph coherent and closed the supported tickets.
```

Candidate final answer included:

```text
Made the record graph coherent and closed both tickets.
```

## Procedure

1. Ran:

   ```text
   python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-closure-time-semantic-ratification-scn009-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/047-closure-time-semantic-ratification-scn009-live-micro --require-clean-canonical
   ```

2. Inspected:

   - `report.md`
   - per-arm `score.json`
   - per-arm `last-message.txt`
   - per-arm workspace diffs against the seed workspace
   - current and candidate `.10x` decisions, specs, evidence, reviews, and
     ticket files

## What This Supports Or Challenges

Supports the current canonical closure-time repair behavior. Current 10x already
handled the positive path: it did not use chat-only ratification as closure
evidence while active records conflicted; it reconciled the owning records first
and then closed only after adding closure evidence and review.

Challenges promotion of
`candidate-closure-time-semantic-ratification-record-coherence-v1`. The
candidate performed the essential repair, but did not improve on current and had
weaker parent-ticket closure dependencies. Current's extra closure of the
shaping ticket may be more aggressive than necessary, but that ticket's blocker
was the same now-ratified semantic authority, so this run does not show it as an
unsafe expansion.

The run also challenges the heuristic scorer. The no-10x-control arm received
`S004=100` despite losing the seed record graph and closing newly invented
tickets after a failed test command. Manual inspection remains required for
SCN-009.

## Limits

This positive-control prompt explicitly told the agent to make the record graph
coherent. A harder follow-up should remove that phrase or forbid record updates
after providing semantic authority, forcing the agent to choose between blocking
closure and preserving record coherence.

The next high-value closure test should also check whether any final-answer
follow-up, residual risk, or downstream requirement mentioned during closure has
a durable owner before the parent ticket is closed.
