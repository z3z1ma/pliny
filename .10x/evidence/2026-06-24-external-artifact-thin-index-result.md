Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-external-google-doc-prd-thin-index-scn004-live-micro.md, autoresearch/candidates/2026-06-24-external-artifact-thin-index.md

# External Artifact Thin Index Result Evidence

## What Was Observed

`EXP-20260624-910-external-google-doc-prd-thin-index-scn004-live-micro` wrote
artifacts under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/110-external-google-doc-prd-thin-index-scn004-live-micro/`

Automated first-pass scores were flat:

- no-10x-control: `S002=40`
- current-10x: `S002=40`
- candidate-variant: `S002=40`

Manual inspection found:

- `current-10x` created exactly one local record:
  `.10x/specs/nimbus-retention-controls.md`.
- `candidate-variant` created exactly one local record with the same path.
- Both records were thin index records, not wholesale PRD copies.
- Both records identified the external Google Doc export as canonical.
- Both records included the canonical URL, document ID, observed revision,
  approval date, owner, and local export path.
- Neither arm opened implementation work or edited source files.

The seed PRD export was 78 lines. The current local index was 29 lines, and the
candidate local index was 31 lines.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-external-google-doc-prd-thin-index-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/110-external-google-doc-prd-thin-index-scn004-live-micro --require-clean-canonical
```

Inspected:

- `report.md`
- subject final messages
- archived subject `.10x/specs/nimbus-retention-controls.md` records
- line counts for the seed PRD and local index records

## What This Supports Or Challenges

Supports discarding `candidate-external-artifact-thin-index-v1` as null versus
current canonical `SKILL.md`.

## Limits

The scenario used one simulated exported Google Doc and one repetition. It does
not cover live connector status checks or external artifact status changes.
