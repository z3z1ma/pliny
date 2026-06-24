# Candidate: External Artifact Provenance Fields

Candidate ID: `candidate-external-artifact-provenance-fields-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted

## Target Behavior

When a local `.10x` record indexes an external canonical artifact, it should not
merely say "see external artifact." It should preserve enough available
provenance for future agents to refind the artifact and judge authority without
reconstructing the current session.

## Proposed Instruction Overlay

Add near "Keep 10x as the Index":

```text
When an external artifact remains canonical, the local 10x index record must
preserve the available provenance needed to refind and assess that artifact:
canonical URL, source system, external id or thread/document/issue identifier,
observed status, revision or export timestamp, local export path, and a clear
statement that the external artifact remains canonical. Include only fields the
artifact actually exposes; do not invent missing metadata.

This provenance requirement does not authorize copying the whole artifact. Keep
thin index records concise. If the user explicitly makes the local 10x record
canonical, include external provenance separately while writing the full local
behavioral contract required by that authority transfer.
```

## Expected Score Movement

- S002 Record Graph Fitness should improve for external PR/Jira/design-doc
  index records by preserving URL/id/status/revision provenance.
- S005 Economy should hold because the candidate explicitly forbids copying the
  whole artifact.
- S003 Ticket Readiness should hold because indexing external decisions should
  not create implementation tickets.

## Scenario Coverage

Primary scenario:

- SCN-004 external PR discussion contains a durable decision but remains the
  canonical review artifact.

Required regression controls before promotion:

- Google Doc PRD remains canonical and should get a thin index.
- Local `.10x` spec is explicitly made canonical and should become a full
  implementation contract with external provenance, not a thin pointer.

## Expected Failure Modes

- Candidate could encourage bloated metadata blocks or copying too much of the
  external artifact.
- Candidate could over-apply thin-index behavior when the user explicitly makes
  the local `.10x` record canonical.
- Candidate could invent provenance fields that the external artifact did not
  expose.

## Promotion Boundary

Promote only if candidate preserves available external provenance materially
better than current on the PR-decision scenario, while passing the thin-index
and local-canonical regression controls. Discard if current already improves on
rerun, or if candidate copies too much artifact content, invents metadata, or
weakens local-canonical authority transfer.

## Promotion Result

Promoted to `SKILL.md` on 2026-06-24 after:

- `EXP-20260624-930-external-artifact-provenance-fields-scn004-live-micro`
  showed candidate preserved the missing canonical URL, source system,
  repository, thread id, PR status, export timestamp, local export path, and
  canonical-authority statement while current omitted most of that provenance.
- `EXP-20260624-931-external-artifact-provenance-thin-index-regression-scn004-live-micro`
  showed candidate kept the Google Doc PRD index thin and did not copy the
  external artifact.
- `EXP-20260624-932-external-artifact-provenance-local-canonical-regression-scn004-live-micro`
  showed candidate still created a full local canonical implementation contract
  when Product and Engineering explicitly transferred authority into `.10x`.

Supporting records:

- `.10x/evidence/2026-06-24-external-artifact-provenance-fields-result.md`
- `.10x/reviews/2026-06-24-external-artifact-provenance-fields-result.md`
