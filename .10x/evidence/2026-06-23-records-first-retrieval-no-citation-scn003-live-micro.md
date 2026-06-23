Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-records-first-retrieval-no-citation-scn003-live-micro.md

# Records-First Retrieval No-Citation SCN-003 Live Micro

## What Was Observed

`EXP-20260623-827-records-first-retrieval-no-citation-scn003-live-micro` ran one
live Codex subject sample per arm. The prompt did not explicitly ask subjects
to cite record paths.

Trust Level 1 score vector:

- no-10x-control: `S001=40`, `S002=50`, `S007=20`
- current-10x: `S001=100`, `S002=50`, `S007=60`
- candidate-variant: `S001=100`, `S002=60`, `S007=80`

Manual inspection found the candidate named both records used:

- `.10x/specs/enterprise-billing-dashboard-sales-validation.md`
- `.10x/tickets/2026-06-23-shape-enterprise-billing-dashboard-improvements.md`

Current answered from `.10x` records and linked the next ticket, but did not
make the source record set as explicit. No-10x control did not use `.10x` and
again moved toward implementation scope.

Artifacts:

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/campaign.json`
- canonical guard:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/canonical_guard.json`

## Procedure

Command run:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-records-first-retrieval-no-citation-scn003-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro --require-clean-canonical
```

Manual inspection read the report, raw outputs, last-message transcripts, score
artifacts, workspace manifests, and file-output lists.

## What This Supports Or Challenges

This supports keeping `candidate-records-first-retrieval-v1`: the positive
retrieval result repeated without explicit prompt wording to cite record paths.

It also challenges immediate promotion because the seed records were the same as
EXP-826. A fresh-record retrieval test is still needed.

## Limits

One live sample per arm. Seed context reused the same upstream-gated
continuation workspaces as EXP-826. The automated S002 scorer remains
conservative for retrieval continuations.
