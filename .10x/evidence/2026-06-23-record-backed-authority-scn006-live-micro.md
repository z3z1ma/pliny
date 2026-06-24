Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-record-backed-authority-scn006-live-micro.md, autoresearch/candidates/2026-06-23-record-backed-authority-progress.md

# Record-Backed Authority SCN-006 Live Micro

## What Was Observed

`EXP-20260623-838-record-backed-authority-scn006-live-micro` ran one live Codex
turn per arm. The seed workspace contained active records explicitly ratifying
display-only Kappa greenline behavior, source field
`KappaReleaseRow.readinessScore`, and threshold `>= 85`. The prompt asked the
agent to harden records and open the executable ticket without asking the user
to re-ratify values already owned by active records.

Automated score vector:

- no-10x-control: `S003=100`
- current-10x: `S003=100`
- candidate-variant: `S003=100`

Manual inspection:

- Control had inherited `.10x` removed before execution. It created new records
  from source inspection rather than using active seed records.
- Current used active records as authority for `readinessScore >= 85`, did not
  ask for re-ratification, opened an executable ticket, recorded inspection
  evidence, and did not edit implementation files.
- Candidate used active records as authority for `readinessScore >= 85`, did
  not ask for re-ratification, opened an executable ticket, and did not edit
  implementation files. It was leaner than current but did not create separate
  inspection evidence.

Workspace-manifest changed files:

- Control: `.10x/evidence/2026-06-24-kappa-greenline-source-inspection.md`,
  `.10x/specs/kappa-greenline-preview.md`, and
  `.10x/tickets/2026-06-25-implement-kappa-greenline-hardening.md`.
- Current: `.10x/evidence/2026-06-24-kappa-greenline-record-inspection.md`,
  `.10x/tickets/2026-06-21-shape-kappa-greenline.md`, and
  `.10x/tickets/2026-06-24-implement-kappa-greenline-pilot.md`.
- Candidate: `.10x/tickets/2026-06-21-shape-kappa-greenline.md` and
  `.10x/tickets/2026-06-24-implement-kappa-greenline-display-label.md`.

Artifact paths:

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/038-record-backed-authority-scn006-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/038-record-backed-authority-scn006-live-micro/campaign.json`
- raw outputs:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/038-record-backed-authority-scn006-live-micro/raw/`

## Procedure

1. Ran live Codex subjects with
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-record-backed-authority-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/038-record-backed-authority-scn006-live-micro --require-clean-canonical`.
2. Inspected generated report, canonical guard, last messages, workspace
   manifests, score artifacts, and current/candidate ticket records.
3. Added campaign metadata with result status `discard`.
4. Regenerated the report and appended `results.tsv`.

## What This Supports Or Challenges

Supports the current canonical skill after the recent assumption-provenance
promotions. Current 10x did not overblock when active records explicitly owned
the semantic values.

Challenges promoting `candidate-record-backed-authority-progress-v1`: the
candidate did not produce a material behavior improvement over current.

## Limits

One live positive-control sample per arm. This does not prove all
record-backed-authority cases, especially stale or conflicting records, but it
reduces concern that the recent anti-laundering gates broadly prevent progress
from active records.
