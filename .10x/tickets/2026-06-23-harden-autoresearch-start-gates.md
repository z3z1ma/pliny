Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/decisions/autoresearch-program-owned-loop.md, .10x/tickets/2026-06-23-simplify-autoresearch-program-loop.md

# Harden Autoresearch Start Gates

## Scope

Raise confidence before starting a multiday autoresearch run by adding practical
guardrails around the program-owned loop architecture. The goal is not to make
discovery certain; it is to make unsafe or misleading execution materially less
likely before the LLM begins autonomous iteration.

Included:

- Add a canonical-file guard to `run_once.py` so every experiment snapshots and
  verifies `SKILL.md` and `autoresearch/program.md`.
- Add an opt-in clean-canonical check for multiday starts that fails if canonical
  files differ from git before an experiment.
- Record canonical guard output under the experiment output directory.
- Add a simple results ledger helper so `results.tsv` has a consistent header
  and append validation.
- Add an eval split file that distinguishes exploration scenarios from held-out
  review scenarios.
- Update `autoresearch/program.md` with start gates:
  - use a dedicated branch;
  - initialize results ledger;
  - run with canonical guard;
  - keep `SKILL.md` and `program.md` unchanged;
  - use held-out scenarios for review candidates;
  - run ablations/parallel variants before review;
  - treat automated scores as non-promotion-grade.
- Add tests for the guard, ledger helper, and held-out split validation.
- Record evidence and review.

Excluded:

- Automatic promotion into canonical `SKILL.md`.
- Live subject-agent evaluation implementation.
- A Python-owned autonomous loop.
- Claims that discovery or promotion proof reaches 99%.

## Acceptance Criteria

- AC-001: `run_once.py` writes a canonical guard artifact containing pre/post
  SHA-256 hashes for `SKILL.md` and `autoresearch/program.md`.
- AC-002: `run_once.py` fails if either canonical file changes during the
  one-shot experiment.
- AC-003: `run_once.py --require-clean-canonical` fails if git reports canonical
  files as modified, deleted, or untracked before the run.
- AC-004: `autoresearch/results.py` can initialize a TSV ledger and append
  validated rows without commas or malformed statuses.
- AC-005: A checked-in split file identifies exploration and held-out scenarios
  and is validated by `autoresearch/validate.py`.
- AC-006: `program.md` describes the start gates and the confidence boundary:
  safe operation can approach 99%, but automated proof of promotion cannot.
- AC-007: README documents the guarded `run_once.py` invocation and results
  helper.
- AC-008: Tests cover canonical guard success/failure, clean-canonical refusal,
  results ledger init/append validation, and split validation.
- AC-009: `python3 autoresearch/validate.py` and
  `python3 -m unittest discover -s autoresearch/tests` pass.

## Progress And Notes

- 2026-06-23: Opened after the user requested executing all feasible measures to
  move autoresearch start confidence as close to 99% as physically possible
  before beginning.
- 2026-06-23: Added canonical guard, guarded `run_once.py`, results ledger
  helper, validated scenario split, `program.md`/README start gates, and tests.
  Guarded smoke showed `SKILL.md` and `autoresearch/program.md` unchanged during
  the run. `--require-clean` correctly fails until the setup is committed because
  `autoresearch/program.md` is still untracked. Evidence:
  `.10x/evidence/2026-06-23-harden-autoresearch-start-gates.md`. Review:
  `.10x/reviews/2026-06-23-harden-autoresearch-start-gates.md`.

## Blockers

None.
