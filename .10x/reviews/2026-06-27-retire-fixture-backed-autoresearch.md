Status: pass
Created: 2026-06-27
Updated: 2026-06-27
Relates-To: .10x/tickets/done/2026-06-27-retire-fixture-backed-autoresearch.md, .10x/evidence/2026-06-27-retire-fixture-backed-autoresearch.md

# Review: Retire Fixture-Backed Autoresearch

## Verdict

Pass.

## Review

The change aligns the implementation with the intended methodology: the LLM
researcher designs and inspects trials, while Python runs one registered live
trial and preserves artifacts.

The removed files are the static fixture/scoring/calibration surface:
`offline_score.py`, `run_micro.py`, `calibrate_scorer.py`, `results.py`, offline
fixture JSON, calibration labels, score-artifact schema, and matching tests.

The remaining live path is coherent:

- `run_codex_subject.py` records raw trial artifacts and command/workspace
  artifacts only.
- `run_once.py` still runs exactly one registered live Codex subject experiment
  and writes the canonical guard plus report.
- `report.py` is now a secondary trial-artifact view and explicitly does not
  grade or promote.
- Active docs/templates/spec/catalogs now point readers toward scientist
  inspection and durable `.10x/` verdict records.

## Residual Risk

The live seed directory has been renamed to `autoresearch/trial-seeds/`; the
old path is no longer part of the active runner, docs, or seed manifests.

The report exposes only the `--artifacts` input flag. The old score-report
command surface was removed instead of kept as an alias.

## Verification

- `python3 autoresearch/validate.py` passed.
- `python3 -m unittest discover -s autoresearch/tests` passed: 41 tests.
- `git diff --check` passed.
- Retired seed-path residue search across `.10x` and `autoresearch` returned
  no matches.
