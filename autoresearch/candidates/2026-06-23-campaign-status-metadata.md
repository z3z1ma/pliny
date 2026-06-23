# Candidate: Campaign Status Metadata Discipline

Candidate ID: `candidate-campaign-status-metadata-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When an agent runs or closes an experiment, calibration campaign, benchmark, or
candidate comparison, it should preserve the campaign-level verdict in a
machine-readable metadata artifact as well as in prose records.

The metadata artifact should include:

- `campaign_id` or `experiment_id`
- `candidate_id`
- `baseline_id`
- `verdict`
- `result_status`
- `statuses`
- `promotion_decision`
- `manual_inspection.status`
- `evidence_refs`
- `limits`

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this operational rule to the experiment/campaign closure path:

```text
When closing an experiment, calibration campaign, benchmark, or candidate
comparison, write a machine-readable campaign metadata JSON artifact whenever
the conclusion includes a negative, null, confounded, backfire, inconclusive, or
promotion-relevant verdict. Keep automated score artifacts separate from this
manual/contextual verdict metadata. Reports may read the metadata, but the
metadata must not upgrade scorer trust or imply promotion authority.
```

## Expected Score Movement

- S004 Evidence Integrity: should improve because report/evidence claims can
  point to a structured verdict artifact instead of relying on prose-only
  interpretation.
- S006 Closure Coherence: should improve because closure records, reports, and
  follow-up tickets can agree on null/confounded/backfire status.
- S008 Research Method Discipline: should improve for calibration and promotion
  studies because negative/null/confounded findings become harder to lose.

## Scenario Coverage

Primary scenarios:

- SCN-013 scorer-bug-trap
- SCN-014 baseline-does-not-fail
- SCN-015 variant-backfire

Secondary scenarios:

- SCN-008 evidence-overclaim
- SCN-009 closure-trap

## Expected Failure Modes

- Over-recording: agents might create metadata for trivial work where no
  campaign verdict exists.
- Trust confusion: agents might treat manual campaign metadata as scorer output.
- Promotion confusion: agents might treat a structured verdict as authorization
  to change canonical instructions.

## Promotion Boundary

This candidate cannot be promoted without a separate campaign, evidence, review,
and explicit human promotion decision. It must not directly edit `SKILL.md`.
