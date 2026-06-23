Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-skill-autoresearch-run.md, .10x/research/2026-06-23-smallest-executable-unit-live-subject.md, .10x/tickets/done/2026-06-23-candidate-executing-evaluation-surface.md

# Smallest Executable Unit Live Subject Result

## What Was Observed

On 2026-06-23, the command
`python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-smallest-executable-unit-live-subject.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/004-smallest-executable-unit-micro-codex`
completed successfully.

The run wrote three live Codex subject-agent samples under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/004-smallest-executable-unit-micro-codex/`
covering SCN-010 across `no-10x-control`, `current-10x`, and
`candidate-variant`.

The run summary recorded:

| Field | Value |
| --- | --- |
| mode | `live` |
| samples_written | `3` |
| live_codex_calls | `3` |
| planned_harness_runs | `3` |
| timeout_seconds_per_run | `1800` |
| planned_wall_clock_hours | `0.5` |

Observed score comparison from the generated report:

| Arm | Scores | Wall seconds | Manual status |
| --- | --- | ---: | --- |
| `current-10x` | `S005=95`, `S007=30` | 94.62 | `required-not-done` |
| `candidate-variant` | `S005=80`, `S007=30` | 61.17 | `required-not-done` |
| `no-10x-control` | `S005=80`, `S007=10` | 82.56 | `required-not-done` |

The `candidate-variant` underperformed `current-10x` on S005 and tied
`current-10x` on S007. Campaign metadata at
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/004-smallest-executable-unit-micro-codex/campaign.json`
records verdict `discard`, result status `negative`, and promotion decision
`not-promoted` for this exact candidate variant.

The canonical guard artifact
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/004-smallest-executable-unit-micro-codex/canonical_guard.json`
reported `unchanged_during_run: true` and `changed_paths: []` for `SKILL.md`
and `autoresearch/program.md`.

The plan and command artifacts sanitize the Codex prompt argument as
`<prompt stored at ...>` instead of embedding full instruction text in argv.
Raw scoring transcripts include the scenario prompt and subject response, not
the full instruction prompt. Prompt text remains available as raw artifacts
under `prompts/`.

Workspace manifests reported no pre-run or post-run suppressed instruction
files for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, or
`.agents/skills`. The manifests still record the limitation that Codex system
context and authenticated home state remain outside complete runner control.

The result was appended to `results.tsv` as
`candidate-smallest-executable-unit-gate-v1` with score vector
`S005=80;S007=30` and status `discard`.

Two earlier attempts wrote partial artifacts under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/003-smallest-executable-unit-live-subject/`.
Those attempts were interrupted while correcting timeout and MICRO/FULL
harness semantics. They are not used as score evidence.

## Procedure

1. Registered the live Codex MICRO experiment in
   `.10x/research/2026-06-23-smallest-executable-unit-live-subject.md`.
2. Ran `run_once.py` against the live Codex subject-runner definition.
3. Inspected `summary.json`, `canonical_guard.json`, score artifacts, raw
   transcripts, plan metadata, command metadata, workspace manifests, and the
   generated report.
4. Added campaign verdict metadata for the contextual comparison result.
5. Regenerated the report with campaign metadata.
6. Logged the result in `results.tsv`.

## What This Supports Or Challenges

This supports that autoresearch can now run a candidate-executing MICRO
experiment through live Codex, produce score artifacts, preserve canonical-file
safety, record no-10x control isolation metadata, and keep one-iteration
discipline without a Python loop controller.

This challenges promotion of
`candidate-smallest-executable-unit-gate-v1`: in the first live SCN-010 Codex
MICRO, the candidate did not improve the numeric targets and lost to current
10x on S005.

This also challenges the report layer's previous artifact-only status wording.
The report was updated so that when campaign metadata is present and score
artifacts have no embedded statuses, the report points readers to the Campaign
Verdict rather than implying no negative contextual result exists.

This also challenged the scorer limit wording. The offline scorer previously
said it did not run live APIs or subject-agent harnesses even when scoring
previously captured live Codex outputs. The scorer now distinguishes fixture
inputs from live subject-agent artifacts and states that it scores previously
captured live harness outputs.

The holistic audit also found and removed the active FULL fixture-smoke runner
path. `run_once.py` is now live-only for MICRO and FULL experiments. Fixture
and smoke definitions are not part of its surface.

Verification after the fixes:

| Command | Result |
| --- | --- |
| `python3 -m unittest discover -s autoresearch/tests` | 43 tests, `OK` |
| `python3 autoresearch/validate.py` | `autoresearch contracts valid` |
| `python3 autoresearch/canonical_guard.py` | `SKILL.md` unchanged; `autoresearch/program.md` snapshot recorded |

## Limits

This is one live MICRO repetition over one scenario. The score artifacts remain
Trust Level 1 heuristic output with human manual inspection still marked
`required-not-done`. The campaign verdict rejects this exact candidate variant
for promotion; it does not prove the underlying instruction idea cannot be
improved. Codex system context and authenticated home state are not fully
controlled by the runner.
