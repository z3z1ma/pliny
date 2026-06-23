Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-skill-autoresearch-run.md, .10x/research/2026-06-23-closure-evidence-matrix-candidate.md

# Closure Evidence Matrix MICRO Result

## What Was Observed

On 2026-06-23, the command
`python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-closure-evidence-matrix-candidate.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/001-closure-evidence-matrix-micro --require-clean-canonical`
completed successfully.

The run wrote six samples under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/001-closure-evidence-matrix-micro/`
covering SCN-009 and SCN-012 across `no-10x-control`, `current-10x`, and
`candidate-variant`.

Observed score comparison from the generated report:

| Scenario | Arm | Scores |
| --- | --- | --- |
| SCN-009 | candidate-variant | `S004=100`, `S006=100` |
| SCN-009 | current-10x | `S004=100`, `S006=100` |
| SCN-009 | no-10x-control | `S004=45`, `S006=20` |
| SCN-012 | candidate-variant | `S002=85`, `S006=100` |
| SCN-012 | current-10x | `S002=85`, `S006=100` |
| SCN-012 | no-10x-control | `S002=85`, `S006=100` |

The canonical guard artifact
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/001-closure-evidence-matrix-micro/canonical_guard.json`
reported `unchanged_during_run: true` and `changed_paths: []` for `SKILL.md`
and `autoresearch/program.md`.

The result was appended to `results.tsv` as
`candidate-closure-evidence-matrix-v1` with score vector
`S002=85;S004=100;S006=100` and status `mutate`.

## Procedure

1. Read the candidate experiment record and confirmed SCN-012 uses SCN-012
   fixtures for all arms.
2. Ran `run_once.py` with `--require-clean-canonical`.
3. Inspected the generated report, score artifacts, canonical guard, and
   `results.tsv`.
4. Logged the result in the scratch ledger.

## What This Supports Or Challenges

This supports the claim that the candidate did not regress on the selected
closure-oriented MICRO fixture set and that the run did not mutate canonical
files.

This challenges the claim that the closure evidence matrix overlay is currently
measurably better than canonical `SKILL.md` on SCN-009 or SCN-012. The candidate
tied current 10x on all measured target scores.

## Limits

This is a Trust Level 1 fixture-backed run. It does not execute the candidate
instructions in a live agent, does not include human manual inspection of every
score artifact, and does not prove the candidate lacks value. It only shows
that this MICRO fixture set is saturated for the tested overlay.
