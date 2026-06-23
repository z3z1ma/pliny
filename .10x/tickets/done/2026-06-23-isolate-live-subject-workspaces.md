Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/research/2026-06-23-skill-autoresearch-run.md
Depends-On: .10x/evidence/2026-06-23-ticket-readiness-gate-scn006-live-micro.md

# Isolate Live Subject Workspaces

## Scope

Fix the live Codex subject runner so one arm cannot read another arm's generated
workspace during the same experiment.

Included:

- Run each subject sample from an isolated temporary workspace that has no
  sibling arm workspaces.
- Archive the completed workspace into the existing artifact directory after the
  sample finishes so reports, manifests, and file-output inspection still work.
- Add a regression test for the isolation behavior.
- Mark the handoff SCN-006 run that exposed the leak as confounded.

Excluded:

- Changing score definitions.
- Changing candidate instructions.
- Re-running all prior experiments.

## Acceptance Criteria

- AC-001: During live subject execution, the Codex process cannot discover prior
  arm workspaces by traversing sibling directories under the artifact root.
- AC-002: After execution, workspace manifests and file outputs remain archived
  under the configured experiment output directory.
- AC-003: A regression test fails against the old shared-workspace behavior and
  passes with isolation.
- AC-004: `python3 -m unittest discover -s autoresearch/tests` and
  `python3 autoresearch/validate.py` pass.
- AC-005: The confounded handoff run is recorded as not valid candidate uplift
  evidence.

## Progress and Notes

- 2026-06-23: Opened after
  `EXP-20260623-820-ticket-readiness-gate-scn006-handoff-live-micro` showed the
  candidate arm read a sibling current-arm workspace and reused its ticket as
  prior art.
- 2026-06-23: Updated `autoresearch/run_codex_subject.py` so `_run_sample`
  executes Codex in a private temporary workspace and archives the completed
  workspace afterward to the planned artifact path.
- 2026-06-23: Added
  `CodexSubjectRunnerTest.test_live_run_hides_sibling_arm_workspaces_during_execution`.
  This regression test would fail against the old shared artifact-parent
  layout because later arms could see earlier `arm-marker.txt` files.
- 2026-06-23: Marked
  `.10x/research/2026-06-23-ticket-readiness-gate-scn006-handoff-live-micro.md`
  confounded and recorded
  `.10x/evidence/2026-06-23-ticket-readiness-gate-scn006-handoff-live-micro.md`.
- 2026-06-23: Verified `python3 -m unittest discover -s autoresearch/tests`,
  `python3 autoresearch/validate.py`, and `git diff --check`.
- 2026-06-23: Recorded review
  `.10x/reviews/2026-06-23-live-subject-workspace-isolation.md` with verdict
  pass.

## Blockers

None.
