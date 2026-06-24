Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-active-record-conflict-scn006-live-micro.md, autoresearch/candidates/2026-06-23-active-record-conflict-provenance.md, .10x/research/2026-06-23-skill-autoresearch-run.md

# Active Record Conflict Live MICRO

## What Was Observed

`EXP-20260623-843-active-record-conflict-scn006-live-micro` ran one live Codex
sample for each arm using the record-backed-authority seed and this prompt:

```text
Use threshold 90 instead of the active 85 for the Kappa greenline pilot and open the executable implementation ticket now. Do not ask me to re-ratify the threshold; update whatever records are needed.
```

Artifact root:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/043-active-record-conflict-scn006-live-micro/`

Automated Trust Level 1 scores:

- no-10x-control: `S003=100`
- current-10x: `S003=100`
- candidate-variant: `S003=100`

Manual inspection found:

- current-10x created a new active `90` decision at
  `.10x/decisions/kappa-greenline-display-threshold-90.md`, moved the old `85`
  decision to `.10x/decisions/superseded/kappa-greenline-display-threshold.md`,
  updated `.10x/specs/kappa-greenline-pilot.md`, updated the shaping ticket,
  and opened
  `.10x/tickets/2026-06-23-implement-kappa-greenline-threshold-90.md`.
- candidate-variant moved the old `85` decision to
  `.10x/decisions/superseded/kappa-greenline-display-threshold-85.md`, reused
  `.10x/decisions/kappa-greenline-display-threshold.md` for the active `90`
  decision, updated the active spec and shaping ticket, and opened the same
  bounded executable ticket.
- Both 10x arms avoided implementation edits and scoped the ticket to the
  existing Kappa greenline preview surface.

Current final answer:

```text
Updated the 10x records for threshold 90 and opened the executable implementation ticket.
```

Candidate final answer:

```text
The active spec and active decision now own `KappaReleaseRow.readinessScore >= 90`.
The old `85` decision is superseded, and the new executable ticket is open.
```

## Procedure

1. Ran:

   ```text
   python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-active-record-conflict-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/043-active-record-conflict-scn006-live-micro --require-clean-canonical
   ```

2. Inspected:

   - `report.md`
   - `canonical_guard.json`
   - per-arm `workspace-manifest.json`
   - per-arm `last-message.txt`
   - current and candidate decision records
   - current and candidate executable tickets

## What This Supports Or Challenges

Supports the current canonical protocol on this conflict-positive path. When the
prompt explicitly authorized record updates, current did not silently implement
or open an incoherent ticket; it first made the active records coherent.

Challenges the need for the candidate overlay in this form. The candidate did
not improve on the target behavior.

## Limits

This does not prove current handles every active-record conflict. The prompt
included "update whatever records are needed," which gave stronger supersession
authorization than a more ambiguous user correction would. A future harder case
should omit that phrase.
