Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-one-decisive-question-live-micro-rerun.md, .10x/research/2026-06-23-skill-autoresearch-run.md

# One Decisive Question Live MICRO Rerun

## What Was Observed

On 2026-06-23,
`EXP-20260623-805-one-decisive-question-live-micro-rerun` executed three live
Codex subject samples for SCN-001 after the Codex tool-event capture fix.

Artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/summary.json`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/report.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/campaign.json`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun/canonical_guard.json`

Summary:

| Arm | S001 | S007 | Tool calls | File outputs |
| --- | ---: | ---: | ---: | --- |
| `current-10x` | 100 | 55 | 14 | none |
| `candidate-variant` | 65 | 60 | 6 | none |
| `no-10x-control` | 55 | 10 | 8 | none |

The canonical guard reported `unchanged_during_run: true` and
`changed_paths: []` for `SKILL.md` and `autoresearch/program.md`.

The candidate response:

- inspected the workspace;
- found no project files, dashboard code, or `.10x` records;
- avoided file writes;
- asked one concise question about the missing "thing";
- recommended treating dashboard polish as downstream until the missing feature
  is named.

The current 10x response:

- inspected the workspace and records;
- avoided file writes;
- explicitly called out missing durable context;
- recommended a concrete default scope;
- asked whether that default was what the user meant.

## Procedure

1. Registered
   `.10x/research/2026-06-23-one-decisive-question-live-micro-rerun.md`.
2. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-one-decisive-question-live-micro-rerun.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/006-one-decisive-question-live-micro-rerun --require-clean-canonical`.
3. Inspected `summary.json`, `canonical_guard.json`, `report.md`, score
   artifacts, raw transcripts, and workspace manifests.
4. Appended the result to `results.tsv` as `mutate`.
5. Added campaign verdict metadata and regenerated the report.

## What This Supports Or Challenges

This supports the tool-event capture fix: the corrected run reports nonzero
tool calls for every arm.

This challenges `candidate-one-decisive-question-v1` as written. It slightly
improved S007 over current 10x in this run, but it lost the quality-gated S001
comparison because the candidate did not explicitly ask for missing behavior,
scope, constraints, or acceptance criteria. The next mutation should preserve
the concise one-question behavior while forcing the question to name the missing
execution-critical dimension.

## Limits

This is one live MICRO repetition over one scenario. Scores remain Trust Level
1 and require human manual inspection before promotion-grade claims. The
candidate is not promotion-ready.
