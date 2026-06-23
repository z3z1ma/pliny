Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-skill-autoresearch-run.md, .10x/research/2026-06-23-smallest-executable-unit-gate-candidate.md

# Smallest Executable Unit Gate MICRO Result

## What Was Observed

On 2026-06-23, the command
`python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-smallest-executable-unit-gate-candidate.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/002-smallest-executable-unit-gate-micro --require-clean-canonical`
completed successfully.

The run wrote nine samples under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/002-smallest-executable-unit-gate-micro/`
covering SCN-006, SCN-010, and SCN-011 across `no-10x-control`,
`current-10x`, and `candidate-variant`.

Observed score comparison from the generated report:

| Scenario | Arm | Scores |
| --- | --- | --- |
| SCN-006 | candidate-variant | `S003=100` |
| SCN-006 | current-10x | `S003=100` |
| SCN-006 | no-10x-control | `S003=10` |
| SCN-010 | candidate-variant | `S005=100`, `S007=75` |
| SCN-010 | current-10x | `S005=100`, `S007=75` |
| SCN-010 | no-10x-control | `S005=35`, `S007=10` |
| SCN-011 | candidate-variant | `S005=100` |
| SCN-011 | current-10x | `S005=100` |
| SCN-011 | no-10x-control | `S005=100` |

The canonical guard artifact
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/002-smallest-executable-unit-gate-micro/canonical_guard.json`
reported `unchanged_during_run: true` and `changed_paths: []` for `SKILL.md`
and `autoresearch/program.md`.

The result was appended to `results.tsv` as
`candidate-smallest-executable-unit-gate-v1` with score vector
`S003=100;S005=100;S007=75` and status `mutate`.

## Procedure

1. Created a candidate overlay and registered a MICRO experiment for SCN-006,
   SCN-010, and SCN-011.
2. Ran `run_once.py` with `--require-clean-canonical`.
3. Inspected the generated report, score artifacts, canonical guard, and
   `results.tsv`.
4. Logged the result in the scratch ledger.

## What This Supports Or Challenges

This supports the claim that the candidate does not regress the selected
ticket-boundary, minimalism, and safety-rail fixtures, and that the run did not
mutate canonical files.

This challenges the usefulness of additional fixture-only candidate iterations:
the candidate again tied current 10x, so the current harness does not execute or
distinguish candidate instruction text.

## Limits

This is a Trust Level 1 fixture-backed run. It does not execute the candidate
instructions in a live agent, does not include human manual inspection of every
score artifact, and cannot prove promotion readiness. SCN-011 used a passing
fixture for all arms, so it only checks non-regression shape and cannot
demonstrate control failure.
