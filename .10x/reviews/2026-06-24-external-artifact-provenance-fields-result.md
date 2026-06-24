Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: autoresearch/candidates/2026-06-24-external-artifact-provenance-fields.md
Verdict: pass

# External Artifact Provenance Fields Promotion Review

## Target

`candidate-external-artifact-provenance-fields-v1` and the proposed `SKILL.md`
promotion near "Keep 10x as the Index".

Supporting evidence:

- `.10x/evidence/2026-06-24-external-artifact-provenance-fields-result.md`
- `.10x/research/2026-06-24-external-artifact-provenance-fields-scn004-live-micro.md`
- `.10x/research/2026-06-24-external-artifact-provenance-thin-index-regression-scn004-live-micro.md`
- `.10x/research/2026-06-24-external-artifact-provenance-local-canonical-regression-scn004-live-micro.md`

## Findings

None blocking.

The candidate targeted a real observed gap: current `SKILL.md` created the
correct PR-discussion decision record but failed to preserve enough available
external provenance for future agents to refind and assess authority.

The promotion is narrow and belongs in `SKILL.md`: it clarifies what a thin
external index must preserve, forbids inventing missing metadata, forbids
copying the whole external artifact, and preserves the separate local-canonical
authority-transfer behavior.

Regression coverage is adequate for this promotion:

- Thin-index behavior remained compact and external-canonical.
- Local-canonical behavior still produced a full implementation contract.
- The candidate did not create implementation tickets, source edits, or test
  changes in the evaluated scenarios.

## Verdict

Pass. Promote the external provenance-field rule to `SKILL.md`.

## Residual Risk

Coverage is still limited to simulated exported GitHub and Google Docs
artifacts. Jira/Linear delivery-state records, external design-doc supersession,
external status changes, and non-Codex harness behavior remain future
conformance work.
