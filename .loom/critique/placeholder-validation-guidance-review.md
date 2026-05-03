---
id: critique:placeholder-validation-guidance-review
kind: critique
status: final
created_at: 2026-05-03T07:10:28Z
updated_at: 2026-05-03T07:10:28Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:phvalid16 diff 43cd5a3..working-tree"
links:
  ticket:
    - ticket:phvalid16
  evidence:
    - evidence:placeholder-validation-guidance-validation
  packet:
    - packet:ralph-ticket-phvalid16-20260503T070234Z
external_refs: {}
---

# Summary

Mandatory oracle critique for `ticket:phvalid16` after adding saved-record
placeholder validation guidance.

# Review Target

Current working-tree diff from baseline
`43cd5a384e9d7dcbeb07c279cc150e1cf92990bd`, covering the validation reference,
ticket reconciliation, Ralph packet consumption, and evidence record.

Required critique profiles: `validation-honesty`, `template-safety`, and
`workflow-boundary`.

# Verdict

`changes_required` - the initial evidence used a placeholder scan recipe whose
glob did not match saved `.loom` records from the repository root, so the scan was
effectively a no-op.

# Findings

## FIND-001: Placeholder scan glob missed saved Loom records

Severity: high
Confidence: high
State: open

Observation:

The original saved-record placeholder scan used
`--glob '{constitution,initiatives,research,specs,plans,tickets,critique,wiki,evidence,packets}/**/*.md'`
while searching from `.loom`. A control query with the same unprefixed glob, such
as `rg -n '^id:' .loom --glob '{tickets}/**/*.md'`, produced no output even
though ticket records exist. The corrected form prefixes the glob with `.loom/`,
for example `--glob '.loom/{tickets}/**/*.md'`.

Why it matters:

`ticket:phvalid16#ACC-004` requires evidence for targeted placeholder validation
searches. A no-op scan would let the ticket claim validation evidence that did
not actually inspect saved records.

Follow-up:

Update `skills/loom-records/references/validation.md` and
`evidence:placeholder-validation-guidance-validation` to use the `.loom/...` glob,
rerun the corrected scan, and rerun mandatory critique before closure.

Challenges:

- `ticket:phvalid16#ACC-004`

# Evidence Reviewed

- Scoped working-tree diff for `ticket:phvalid16` at the time of initial review.
- `skills/loom-records/references/validation.md`
- `ticket:phvalid16`
- `packet:ralph-ticket-phvalid16-20260503T070234Z`
- `evidence:placeholder-validation-guidance-validation`
- Control query: `rg -n '^id:' .loom --glob '{tickets}/**/*.md'` produced no output.
- Corrected control query: `rg -n '^id:' .loom --glob '.loom/{tickets}/**/*.md'`
  found ticket records.

# Residual Risks

- The placeholder scan remains heuristic and requires operator review of hits.

# Required Follow-up

- Resolve `critique:placeholder-validation-guidance-review#FIND-001` in the
  ticket-owned critique disposition before closure.
- Rerun mandatory critique after the fix.

# Acceptance Recommendation

`active follow-up required`
