Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: SKILL.md
Verdict: pass

# Review: Promote Illustrative Example Semantic Gate

## Target

Promotion of
`autoresearch/candidates/2026-06-24-illustrative-example-semantic-gate.md` into
`SKILL.md`.

## Findings

- pass: The promoted text is narrow. It does not create a broad new loop,
  state controller, or discretionary escape hatch.
- pass: The rule strengthens the existing assumption-provenance invariant by
  naming a concrete failure mode: illustrative examples plus adjacent source
  fields becoming executable semantics.
- pass: The wording preserves autonomy for source-backed facts while blocking
  missing or derived semantics from entering tickets, specs, tests, or code.
- minor: This may increase blocker questions in example-heavy product requests,
  but that is aligned with the current objective because the added question is
  confirm/correct rather than a broad product interview.

## Verdict

Pass. Promote the candidate.

## Residual Risk

The MICRO result was manually distinguished because the current heuristic scorer
could not separate candidate/current behavior. A future scorer improvement
should detect when blocked tickets still encode unratified acceptance criteria.
