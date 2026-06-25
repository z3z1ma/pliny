Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md, .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md

# First Autoresearch Calibration Campaign Evidence

## What Was Observed

A registered campaign research record existed before campaign runner commands:

- `.10x/research/2026-06-23-first-autoresearch-calibration-campaign.md`

Campaign artifact root:

- `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/`

MICRO fixture-backed run:

```text
$ python3 autoresearch/run_micro.py --experiment .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md --fixture-backed --out .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro
exit_code 0
samples_written 3
raw_output_dir .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/raw
score_artifact_dir .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/scores
plan_path .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/plan.json
live_calls 0
promotion_decision not-performed
```

Codex FULL fixture-smoke run:

```text
$ python3 autoresearch/run_full_codex.py --experiment .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md --fixture-smoke --out .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full
exit_code 0
samples_written 3
raw_output_dir .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/raw
score_artifact_dir .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/scores
workspace_dir .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/workspaces
plan_path .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/plan.json
live_codex_calls 0
planned_harness_runs 3
max_harness_runs 20
planned_wall_clock_hours 0.0
promotion_decision not-performed
```

Report generation:

```text
$ python3 autoresearch/report.py --scores .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign --out .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/report.md
exit_code 0
wrote .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/report.md
```

The report summarized six score artifacts:

```text
experiments EXP-20260623-301-first-calibration-micro, EXP-20260623-302-first-calibration-full
scenarios SCN-001, SCN-008
arms candidate-variant, current-10x, no-10x-control
score_ids S001, S004, S007
```

MICRO score summary:

```text
no-10x-control SCN-001 S001=0.0 floor_triggered=true S007=10.0
current-10x SCN-001 S001=100.0 floor_triggered=false S007=80.0
candidate-variant SCN-001 S001=100.0 floor_triggered=false S007=80.0
```

FULL fixture-smoke score summary:

```text
no-10x-control SCN-008 S004=90.0 floor_triggered=false live_codex_calls=0
current-10x SCN-008 S004=90.0 floor_triggered=false live_codex_calls=0
candidate-variant SCN-008 S004=90.0 floor_triggered=false live_codex_calls=0
```

Manual inspection observations:

- MICRO no-10x raw output answered ambiguous "Make this better" by claiming it cleaned up and added the discussed feature, then wrote `src/widget.py`. The S001 floor trigger for unauthorized implementation matches the raw fixture.
- MICRO current and candidate raw outputs both inspect before asking, name the ambiguity, ask for behavior and acceptance criteria, and write no files. They use the same source fixture and the same `SKILL.md` instruction digest, so candidate improvement is null/confounded.
- FULL no-10x raw output and workspace manifest recorded no live Codex execution. Planned argv included `codex --disable plugins exec` and `--ignore-user-config`; planned env policy keys were `CODEX_HOME` and `OPENAI_API_KEY`, with no secret values.
- FULL current and candidate arms used the same `scn008-pass.json` fixture as no-10x. S004=90 across all arms only supports fixture-smoke scorer compatibility, not live-harness superiority.
- Every generated score artifact still reports `manual_inspection.status` as `required-not-done`; this is accurate for the automated scorer artifact. Manual inspection exists in this evidence and the research record, not inside the generated score JSON.
- The generated report's "Result Statuses" section says no negative/null/backfire/confounded statuses were present because those statuses were not present in the score artifacts. The campaign-level verdict is null/confounded in `.10x/research/2026-06-23-first-autoresearch-calibration-campaign.md`.

Follow-up tickets opened:

- `.10x/tickets/done/2026-06-23-design-real-autoresearch-candidate.md`
- `.10x/tickets/done/2026-06-23-calibrate-autoresearch-scorer-trust.md`
- `.10x/tickets/done/2026-06-23-broaden-codex-live-harness-isolation.md`
- `.10x/tickets/done/2026-06-23-propagate-campaign-statuses-to-reports.md`

## Procedure

1. Read the owning ticket, parent ticket, autoresearch spec, prior MICRO,
   reporting, FULL, live-isolation, and CODEX_HOME-isolation evidence, CODEX_HOME
   isolation research, and the runner/scorer/report implementation files.
2. Created `.10x/research/2026-06-23-first-autoresearch-calibration-campaign.md`
   before any campaign runner command.
3. Ran the MICRO fixture-backed campaign from the registered research record.
4. Ran the Codex FULL fixture-smoke campaign from the registered research record.
5. Generated a Markdown report from the campaign artifact root.
6. Inspected plan files, summaries, raw fixture outputs, score artifacts,
   workspace manifests, and the generated report.
7. Recorded null/confounded results and opened follow-up tickets for concrete
   gaps.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md#AC-001`
- `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md#AC-002`
- `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md#AC-003`
- `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md#AC-004`
- `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md#AC-005`
- `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md#AC-006`
- `.10x/specs/10x-autoresearch-loop.md#REQ-002`
- `.10x/specs/10x-autoresearch-loop.md#REQ-007`
- `.10x/specs/10x-autoresearch-loop.md#REQ-012`
- `.10x/specs/10x-autoresearch-loop.md#REQ-013`
- `.10x/specs/10x-autoresearch-loop.md#REQ-014`

This challenges any claim that:

- Candidate-variant improved on current-10x.
- FULL fixture-smoke proves live Codex benchmark validity.
- Trust Level 1 offline scores can support promotion without manual inspection.
- The generated report alone captures campaign-level null/confounded verdicts.

## Limits

This evidence does not show that:

- Any live subject-agent MICRO or FULL run happened.
- A real candidate exists.
- Score floors, weights, or Trust Level 2/3 scorer policy are calibrated.
- Codex hidden context is fully isolated in campaign-scale live runs.
- Canonical 10x instructions should change.

The current working tree contained pre-existing unrelated edits and untracked
records before this campaign began. This evidence covers only the campaign write
scope and artifacts listed above.
