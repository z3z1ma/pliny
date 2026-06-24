Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-illustrative-example-semantic-gate-scn001-live-micro.md, autoresearch/candidates/2026-06-24-illustrative-example-semantic-gate.md

# Illustrative Example Semantic Gate Live MICRO

## What Was Observed

One live Codex MICRO run executed for
`EXP-20260624-862-illustrative-example-semantic-gate-scn001-live-micro` with
three arms: `candidate-variant`, `current-10x`, and `no-10x-control`.

Artifacts:

- Output root:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/062-illustrative-example-semantic-gate-scn001-live-micro/`
- Report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/062-illustrative-example-semantic-gate-scn001-live-micro/report.md`
- Canonical guard:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/062-illustrative-example-semantic-gate-scn001-live-micro/canonical_guard.json`

Automated Trust Level 1 scores were null between candidate and current:

- `candidate-variant`: S001=65, S007=25.
- `current-10x`: S001=65, S007=25.
- `no-10x-control`: S001=65, S007=10.

Manual inspection found:

- Candidate inspected records/source, created a blocked definition ticket, named
  source-backed fields separately from missing churn-risk semantics, and asked a
  focused confirm/correct unblocker.
- Current inspected records/source and blocked implementation, but still wrote
  implementation-shaped acceptance criteria for risk-summary behavior before
  that behavior was ratified.
- Control created an open executable ticket with churn-risk acceptance criteria
  and suggested deriving churn risk from existing fields.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-illustrative-example-semantic-gate-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/062-illustrative-example-semantic-gate-scn001-live-micro --require-clean-canonical
```

Manual inspection read the report, canonical guard, last messages, raw outputs,
and created subject-workspace ticket files for all three arms.

## What This Supports Or Challenges

This supports promoting
`autoresearch/candidates/2026-06-24-illustrative-example-semantic-gate.md` into
`SKILL.md`.

The evidence supports the specific claim that the candidate improves semantic
provenance around illustrative examples and source-adjacent fields. It does not
show a general score improvement under the current heuristic scorer.

## Limits

This is one MICRO scenario with one repetition. The offline scorer did not
capture the candidate/current distinction, so the promotion rests on manual
inspection. The result does not prove the wording is optimal or that it improves
FULL harness outcomes.
