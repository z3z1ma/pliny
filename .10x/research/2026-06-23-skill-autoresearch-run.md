Status: active
Created: 2026-06-23
Updated: 2026-06-23

# SKILL.md Autoresearch Run

## Question

Can a program-owned autoresearch loop produce candidate instruction overlays
that improve 10x behavior scores for `SKILL.md` without mutating canonical
`SKILL.md` or `autoresearch/program.md`?

## Sources And Methods

Run tag:

- `2026-06-23-skill-autoresearch`

Branch:

- `codex/autoresearch-2026-06-23-skill`

Program:

- `autoresearch/program.md`

Score and scenario split:

- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/splits/skill-improvement-v1.json`

Ledger:

- `results.tsv`

Artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/`

Canonical start guard:

- Every `run_once.py` experiment should use `--require-clean-canonical` when
  canonical files are clean in git.
- `SKILL.md` and `autoresearch/program.md` must remain unchanged during the run.

## Findings

- Baseline MICRO established that current 10x scores above no-10x control on
  SCN-001 for the initial fixture-backed calibration run.
- `candidate-closure-evidence-matrix-v1` did not regress but tied current 10x
  on SCN-009 and SCN-012. The candidate score vector was
  `S002=85;S004=100;S006=100`, with canonical guard unchanged.
- `candidate-smallest-executable-unit-gate-v1` did not regress but tied current
  10x on SCN-006, SCN-010, and SCN-011. The candidate score vector was
  `S003=100;S005=100;S007=75`, with canonical guard unchanged.
- The repeated tie is not evidence that the candidates lack value. It shows the
  current fixture-backed runner does not execute candidate instruction text and
  therefore cannot distinguish a real overlay from current 10x when both arms
  use prewritten pass fixtures.
- Candidate artifacts created during this run:
  - `autoresearch/candidates/2026-06-23-closure-evidence-matrix.md`
  - `autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md`
- Durable evidence created during this run:
  - `.10x/evidence/2026-06-23-closure-evidence-matrix-micro.md`
  - `.10x/evidence/2026-06-23-smallest-executable-unit-gate-micro.md`
- Follow-up ticket completed for the uncovered evaluation gap:
  `.10x/tickets/done/2026-06-23-candidate-executing-evaluation-surface.md`.
- Architecture correction recorded at
  `.10x/decisions/autoresearch-subject-harness-policy.md`: optimization
  requires live subject-harness execution through `run_once.py`; fixture-backed
  calibration is separate from the one-shot iteration path.
- Live Codex MICRO for `candidate-smallest-executable-unit-gate-v1` executed
  candidate instruction text on SCN-010. It scored `S005=80;S007=30` versus
  current 10x at `S005=95;S007=30`, so campaign verdict is `discard` and
  promotion decision is `not-promoted`.
- Durable live evidence created during this run:
  `.10x/evidence/2026-06-23-smallest-executable-unit-live-subject.md`.

## Conclusions

- Autoresearch has begun and can safely generate candidate overlays, run
  one-shot fixture-backed experiments, record score vectors, and preserve
  canonical-file safety.
- The current offline runner is useful for calibration, control discrimination,
  guardrail checks, and regression screening. It is not sufficient to improve
  `SKILL.md` by numbers because it does not execute candidate instructions.
- The next rational step is not more fixture-only candidates. It is a
  candidate-executing evaluation surface, followed by live or manually inspected
  MICRO runs against the existing candidates.
- No canonical `SKILL.md` promotion is supported by the current evidence.
- The first live MICRO result shows the current `SKILL.md` already handles the
  tested minimalism trap better than the smallest-executable-unit overlay.
  Further work should mutate the candidate idea, not promote it.

## Execution Log

- 2026-06-23: Run opened. Initialized `results.tsv`. Created branch
  `codex/autoresearch-2026-06-23-skill`.
- 2026-06-23: Baseline MICRO completed with canonical guard unchanged. Logged
  `baseline-current` with `S001=100;S007=80`.
- 2026-06-23: Added first candidate artifact
  `autoresearch/candidates/2026-06-23-closure-evidence-matrix.md` targeting
  S006/S007 closure and retrospective behavior.
- 2026-06-23: Ran
  `EXP-20260623-801-closure-evidence-matrix-micro` at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/001-closure-evidence-matrix-micro/`.
  Candidate tied current 10x on SCN-009 and SCN-012 with no canonical file
  changes. Logged `candidate-closure-evidence-matrix-v1` to `results.tsv` as
  `mutate` because the fixture set is saturated for this overlay.
- 2026-06-23: Added second candidate artifact
  `autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md`
  targeting S003 ticket readiness and S005 scope minimalism.
- 2026-06-23: Ran
  `EXP-20260623-802-smallest-executable-unit-gate-micro` at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/002-smallest-executable-unit-gate-micro/`.
  Candidate tied current 10x on SCN-006, SCN-010, and SCN-011 with no
  canonical file changes. Logged `candidate-smallest-executable-unit-gate-v1`
  to `results.tsv` as `mutate`. This is the second saturated fixture-backed
  candidate result, indicating the next useful step is a candidate-executing
  evaluation surface rather than more fixture-only overlays.
- 2026-06-23: Opened and completed
  `.10x/tickets/done/2026-06-23-candidate-executing-evaluation-surface.md` for
  the candidate-execution gap. Further fixture-only candidate generation would
  risk optimizing artifacts rather than `SKILL.md` behavior.
- 2026-06-23: Verification after iteration 2 passed:
  `python3 autoresearch/validate.py` reported `autoresearch contracts valid`;
  `python3 -m unittest discover -s autoresearch/tests` ran 42 tests with `OK`;
  `python3 autoresearch/canonical_guard.py --require-clean` reported unchanged
  `SKILL.md` and `autoresearch/program.md`.
- 2026-06-23: Added live Codex subject runner and corrected experiment
  semantics: MICRO/FULL are scenario breadth tiers. `run_once.py` is live-only;
  fixture-backed calibration remains outside the one-shot iteration path.
- 2026-06-23: Ran
  `EXP-20260623-803-smallest-executable-unit-live-subject` at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/004-smallest-executable-unit-micro-codex/`.
  Candidate scored `S005=80;S007=30`, current scored `S005=95;S007=30`, and
  control scored `S005=80;S007=10`. Logged
  `candidate-smallest-executable-unit-gate-v1` to `results.tsv` as `discard`.
- 2026-06-23: Completed holistic audit fixes: live-run limits, campaign verdict
  report wording, live-input scorer limits, experiment template defaults, and
  live-only `run_once.py` semantics. Verification passed:
  `python3 -m unittest discover -s autoresearch/tests` ran 43 tests with `OK`;
  `python3 autoresearch/validate.py` reported `autoresearch contracts valid`;
  `python3 autoresearch/canonical_guard.py` recorded unchanged `SKILL.md`.
