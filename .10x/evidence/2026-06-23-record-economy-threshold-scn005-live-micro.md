Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-record-economy-threshold-scn005-live-micro.md

# Record Economy Threshold SCN-005 Live Micro

## What Was Observed

`EXP-20260623-822-record-economy-threshold-scn005-live-micro` ran one live
Codex subject sample per arm.

Trust Level 1 score vector:

- no-10x-control: `S002=65`, `S005=80`
- current-10x: `S002=65`, `S005=80`
- candidate-variant: `S002=65`, `S005=80`

Manual inspection found all three arms created exactly one knowledge record:

- no-10x-control:
  `.10x/knowledge/billing-dashboard-csv-exports.md`
- current-10x:
  `.10x/knowledge/billing-dashboard-csv-export-convention.md`
- candidate-variant:
  `.10x/knowledge/billing-dashboard-csv-export-convention.md`

The candidate record was slightly more explicit about applicability limits, but
the current and control records were also minimal and usable. No arm created a
placeholder ticket, decision/spec spread, or separate evidence record.

Artifacts:

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/report.md`
- canonical guard:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/canonical_guard.json`
- no-10x score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/scores/sha256-e915269a3cc257dd698af9bce08996b454e71e170861b027de619bccc95bdbc4.score.json`
- current score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/scores/sha256-04ff5a823c11ca560f2f26b4c196e0bc85c444a2fa1f0567be271161bdc3a28d.score.json`
- candidate score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/scores/sha256-70611509ed503507e0029db22c28a9a4132200ee951499431151a189a6cd9d05.score.json`

## Procedure

Commands run:

```text
python3 autoresearch/run_codex_subject.py --experiment .10x/research/2026-06-23-record-economy-threshold-scn005-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro --run
```

```text
python3 autoresearch/report.py --scores .10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/scores --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/report.md
```

```text
python3 autoresearch/canonical_guard.py --root . --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/canonical_guard.json
```

Manual inspection read the report, score summaries, workspace file lists, and
the three generated knowledge records.

## What This Supports Or Challenges

This challenges promotion of `candidate-record-economy-threshold-v1` from this
run: the candidate did not improve the score vector or manual record economy
over current canonical `SKILL.md`.

This also challenges the prompt design. The prompt was too easy because even
the no-10x control produced a single appropriate knowledge record.

## Limits

This evidence does not prove the record-economy threshold is useless. It only
shows that this SCN-005 prompt did not create enough record-spam pressure to
differentiate the candidate from the baseline. A harder prompt is required
before promotion or rejection.
