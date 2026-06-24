Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-external-artifact-provenance-fields-scn004-live-micro.md, .10x/research/2026-06-24-external-artifact-provenance-thin-index-regression-scn004-live-micro.md, .10x/research/2026-06-24-external-artifact-provenance-local-canonical-regression-scn004-live-micro.md, autoresearch/candidates/2026-06-24-external-artifact-provenance-fields.md

# External Artifact Provenance Fields Result

## What Was Observed

Three live Codex MICRO runs evaluated
`candidate-external-artifact-provenance-fields-v1`.

Primary run:

- `EXP-20260624-930-external-artifact-provenance-fields-scn004-live-micro`
- Raw artifact root:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/130-external-artifact-provenance-fields-scn004-live-micro/`
- Automated Trust Level 1 scores: candidate `S002=60`, current `S002=60`,
  no-10x-control `S002=60`.
- Candidate created `.10x/decisions/acme-webhook-idempotency-key.md` with the
  correct `provider_delivery_id` decision and preserved canonical URL, source
  system, repository, thread id, PR status, export timestamp, local export path,
  and a statement that the PR discussion remains canonical.
- Current created the correct decision record but omitted most available
  external provenance, including canonical URL, thread id, PR status, and export
  timestamp.
- no-10x-control preserved the local export path and discussion id but omitted
  canonical URL, PR status, and export timestamp.

Thin-index regression:

- `EXP-20260624-931-external-artifact-provenance-thin-index-regression-scn004-live-micro`
- Raw artifact root:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/131-external-artifact-provenance-thin-index-regression-scn004-live-micro/`
- Automated Trust Level 1 scores: candidate `S002=40`, current `S002=40`,
  no-10x-control `S002=40`.
- Candidate created one thin specification-class Google Doc PRD index, kept it
  to 31 lines versus the 78-line external PRD, stated the Google Doc remains
  canonical, and did not copy the PRD body or acceptance criteria.

Local-canonical regression:

- `EXP-20260624-932-external-artifact-provenance-local-canonical-regression-scn004-live-micro`
- Raw artifact root:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/132-external-artifact-provenance-local-canonical-regression-scn004-live-micro/`
- Automated Trust Level 1 scores: candidate `S002=75`, current `S002=75`,
  no-10x-control `S002=60`.
- Candidate created one full active `.10x/specs/nimbus-retention-controls.md`
  canonical implementation contract, preserved external provenance, and did not
  leave the local spec as a thin pointer.

Across all three runs, subject workspaces contained only the expected `.10x`
record outputs plus the copied external artifacts. No source/test edits or
implementation tickets were observed.

## Procedure

Commands run:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-external-artifact-provenance-fields-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/130-external-artifact-provenance-fields-scn004-live-micro --require-clean-canonical
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-external-artifact-provenance-thin-index-regression-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/131-external-artifact-provenance-thin-index-regression-scn004-live-micro --require-clean-canonical
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-external-artifact-provenance-local-canonical-regression-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/132-external-artifact-provenance-local-canonical-regression-scn004-live-micro --require-clean-canonical
```

Manual inspection compared generated records under each `workspaces/sha256-*`
directory against the exported external artifacts and the manual inspection
requirements in the research records.

## What This Supports Or Challenges

Supports promoting
`autoresearch/candidates/2026-06-24-external-artifact-provenance-fields.md` into
`SKILL.md`.

The candidate fixes the observed PR-discussion provenance weakness without
regressing Google Doc thin-index behavior or local-canonical authority-transfer
behavior.

## Limits

The results cover one PR discussion and one Google Doc PRD seed. They do not yet
cover Jira or Linear delivery-state artifacts, external design documents
superseding local specs, stale external status changes, or non-Codex harnesses.

Automated scores were Trust Level 1 heuristics and failed to distinguish the
manual quality differences in the primary and thin-index cases. Manual
inspection is the authority for this evidence.
