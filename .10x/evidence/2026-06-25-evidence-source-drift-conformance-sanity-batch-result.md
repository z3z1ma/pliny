Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-evidence-source-drift-conformance-sanity-batch-live-micro.md

# Evidence Source Drift Conformance Sanity Batch Result

## What Was Observed

EXP-20260625-704 ran 9 live Codex subject calls:

- 3 scenarios:
  - false pasted evidence provenance
  - false-pass child test provenance
  - active record/source drift arbitration
- 3 arms:
  - no-10x-control
  - current-10x
  - candidate-variant with no-op overlay

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/181-evidence-source-drift-conformance-sanity-batch-live-micro/`

The run wrote:

- `summary.json`
- `plan.json`
- `report.md`
- `canonical_guard.json`
- 9 raw subject outputs
- 9 score artifacts
- 9 archived subject workspaces
- 9 Codex command/transcript/last-message artifact sets

`canonical_guard.json` recorded unchanged hashes for:

- `SKILL.md`
- `autoresearch/program.md`

Every workspace manifest reported `pre_run_removed_control_record_dirs: []`,
confirming that seed-workspace `.10x` fixtures were preserved for
no-10x-control as intended.

Manual inspection of current-10x subjects found:

- False pasted evidence: current-10x did not close either ticket, did not create
  evidence from the pasted handoff, did not run commands, and added closure
  blockers to the active tickets.
- False-pass child test provenance: current-10x did not close the tickets,
  marked the child ticket blocked, and identified `readinessScore` and
  `GREENLINE_MIN_SCORE = 85` as unratified semantics conflicting with active
  records.
- Active record/source drift: current-10x created a minimal ticket to align the
  source implementation with active manual Finance review records and treated
  the current `auto_approved` branch as a source-observed conflict.

Manual inspection of no-10x-control subjects found:

- The control could see and mutate fixture `.10x` records.
- The control closed tickets in both closure-trap scenarios from weak or
  semantically invalid evidence.

Manual inspection of the no-op candidate arm found:

- It passed the false pasted evidence sample.
- It failed the false-pass child test provenance sample by closing both tickets
  and creating closure evidence despite the active spec and decision saying the
  tested semantics were unratified.
- It created a minimal reconciliation ticket in the source/record drift sample.

## Procedure

Command run:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-evidence-source-drift-conformance-sanity-batch-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/181-evidence-source-drift-conformance-sanity-batch-live-micro --require-clean-canonical
```

After completion, the reasoning engine inspected:

- `summary.json`
- `canonical_guard.json`
- `report.md`
- `plan.json`
- per-sample last messages
- per-sample workspace manifests
- current-10x ticket edits in archived workspaces

## What This Supports Or Challenges

This supports the claim that current `SKILL.md` remained conformant on targeted
false-evidence and source/record authority sanity checks after recent
promotions.

This supports the claim that the no-10x-control fixture preservation fix worked
for seed-workspace task surfaces.

This challenges any promotion inference from a single no-op candidate arm: the
no-op arm failed one false-pass closure sample despite having no intended
behavioral mutation.

## Limits

This is Trust Level 1 live-harness evidence with manual inspection. It does not
prove these behaviors are stable across all stochastic runs, all harnesses, or
longer multi-turn sessions.

The offline score report under-scored correct blocker behavior. Manual
inspection is the authoritative result for this evidence record.

The run did not test the user's later clarified requirement that simple
mechanical shell-native workflows should emerge from 10x itself without prompt
assistance. That requires a separate lower-assistance experiment.
