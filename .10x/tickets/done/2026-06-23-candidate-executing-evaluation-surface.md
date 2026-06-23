Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/research/2026-06-23-skill-autoresearch-run.md, .10x/evidence/2026-06-23-closure-evidence-matrix-micro.md, .10x/evidence/2026-06-23-smallest-executable-unit-gate-micro.md, .10x/decisions/autoresearch-subject-harness-policy.md

# Add Candidate-Executing Evaluation Surface

## Scope

Create the smallest acceptable way to evaluate candidate instruction overlays by
actually executing the candidate text against subject-agent tasks, instead of
assigning the candidate arm to prewritten pass fixtures.

Included:

- Define a one-shot candidate-executing evaluation path that preserves the
  program-owned loop model.
- Execute or enable exactly one experiment at a time; do not add a Python loop
  controller, daemon, stop-file system, resume state machine, or automatic
  candidate generator.
- Record the loaded instruction source for `no-10x-control`, `current-10x`, and
  `candidate-variant`.
- Capture raw subject output, command metadata, workspace manifest, stderr or
  JSONL logs where available, score artifacts, and canonical guard output.
- Preserve no-10x control isolation from project `AGENTS.md`, `CLAUDE.md`,
  `.agents/skills`, and equivalent harness-native instruction locations.
- Make the result consumable by the existing report and `results.tsv` flow.

Excluded:

- Changing canonical `SKILL.md`.
- Unrelated edits to `autoresearch/program.md` beyond the operator-requested
  clarification that MICRO/FULL are scenario breadth tiers and fixture runners
  are calibration utilities.
- Adding a run loop, state controller, candidate generator, or background
  daemon.
- Automatic promotion from live output.
- Trust Level 2 or Trust Level 3 scorer approval.
- Claude Code, OpenCode, or oh-my-pi integration unless a later ticket scopes
  those harnesses separately.

## Acceptance Criteria

- AC-001: A registered experiment can execute a candidate instruction overlay
  live or through a manually inspected subject-agent transcript without using a
  prewritten pass fixture for the candidate arm.
- AC-002: The experiment records, for every arm, the instruction source,
  instruction digest or path, prompt/scenario, workspace, command metadata, raw
  output artifact, and score artifact.
- AC-003: The no-10x control arm records how project-level instruction files and
  harness-native skill locations were suppressed, or the ticket blocks with the
  exact contamination risk.
- AC-004: The run still uses the existing one-iteration discipline: one
  candidate, one experiment, one score/report output, one ledger row, and no
  autonomous Python loop.
- AC-005: Evidence demonstrates that `SKILL.md` and `autoresearch/program.md`
  did not change during the live candidate experiment.
- AC-006: The result distinguishes candidate-quality evidence from scorer
  calibration, manual inspection, and promotion authority.

## Progress And Notes

- 2026-06-23: Opened from active autoresearch run after two candidate overlays
  tied current 10x on fixture-backed MICRO runs. The repeated null/tie pattern
  showed that fixture-backed runs can validate guardrails and controls but do
  not execute candidate instruction text.
- 2026-06-23: Implementation started. Smallest accepted surface is a one-shot
  live Codex subject runner that reuses existing score artifacts and reporting
  instead of adding loop/state control.
- 2026-06-23: Added `autoresearch/run_codex_subject.py`, integrated it into
  `autoresearch/run_once.py` for Codex harness definitions without fixture
  mappings, and added focused unit tests. The runner stores full prompts as raw
  artifacts but keeps instruction text out of the score transcript to avoid
  rewarding quoted instructions.
- 2026-06-23: Registered live-subject experiment
  `.10x/research/2026-06-23-smallest-executable-unit-live-subject.md`.
- 2026-06-23: Corrected the model after operator feedback: MICRO and FULL are
  scenario breadth tiers, not execution modes. A MICRO can and should invoke a
  real harness when measuring behavior. `run_once.py` is live-only;
  fixture-backed calibration is separate from the one-shot iteration path.
  Decision recorded at
  `.10x/decisions/autoresearch-subject-harness-policy.md`.
- 2026-06-23: Ran live Codex MICRO experiment
  `EXP-20260623-803-smallest-executable-unit-live-subject` at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/004-smallest-executable-unit-micro-codex/`.
  The run wrote three live samples, one per arm, with `timeout_seconds_per_run`
  set to 1800. Canonical guard reported `unchanged_during_run: true` and
  `changed_paths: []`.
- 2026-06-23: Recorded live evidence at
  `.10x/evidence/2026-06-23-smallest-executable-unit-live-subject.md`.
  Candidate `candidate-smallest-executable-unit-gate-v1` scored
  `S005=80;S007=30` versus current `S005=95;S007=30`; campaign verdict is
  `discard` and promotion decision is `not-promoted`.
- 2026-06-23: Patched `run_once.py` limits so live subject runs no longer
  describe themselves as fixture-backed evidence. Patched report wording so an
  artifact-only status section cannot imply no negative contextual result when
  campaign verdict metadata is present.
- 2026-06-23: Deleted the active FULL fixture-smoke runner path
  (`autoresearch/run_full_codex.py` and its tests). Then simplified
  `run_once.py` further so it is live-only; fixture and smoke definitions are
  not part of its surface.
- 2026-06-23: Patched `offline_score.py` so live subject-agent artifacts no
  longer claim the scorer did not involve a live harness. Live artifacts now say
  the scorer evaluates previously captured live harness outputs.
- 2026-06-23: Verification passed:
  `python3 -m unittest discover -s autoresearch/tests` -> 43 tests OK;
  `python3 autoresearch/validate.py` -> `autoresearch contracts valid`;
  `python3 autoresearch/canonical_guard.py` recorded unchanged `SKILL.md` and a
  current `autoresearch/program.md` snapshot.
- 2026-06-23: Review recorded at
  `.10x/reviews/2026-06-23-live-harness-autoresearch-audit.md`. Residual risks
  are Trust Level 1 scorer authority, imperfect Codex system/home isolation, and
  single-run variance. These risks limit promotion claims but do not block the
  candidate-executing evaluation surface.
- 2026-06-23: Acceptance criteria checked:
  AC-001 live candidate overlay executed; AC-002 instruction/prompt/workspace/
  command/raw/score artifacts recorded; AC-003 no-10x isolation metadata
  recorded; AC-004 one-iteration discipline preserved; AC-005 canonical guard
  unchanged during run; AC-006 campaign metadata and report limits distinguish
  candidate-quality evidence from promotion authority.

## Blockers

None.
