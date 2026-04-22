---
id: critique:evidence-gate-review
kind: critique
status: final
created_at: 2026-04-22T00:00:00Z
updated_at: 2026-04-22T00:00:00Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:risk0001
links:
  ticket:
    - ticket:risk0001
  evidence:
    - evidence:evidence-gate-structural-check
external_refs: {}
---

# Summary

Reviewed a high-risk protocol authority change to the evidence gate.

# Review Target

ticket:risk0001 and the changed validation rule fixture.

# Verdict

Do not close until follow-up text clarifies evidence minimums.

# Findings

## FIND-001: Evidence minimum is still underspecified

Severity: high
Confidence: medium
Disposition: open

Observation:

The rule requires evidence but does not say what kind of evidence is sufficient.

Why it matters:

Agents may close work with weak proof.

Follow-up:

- ticket:risk0001

Challenges:
- ticket:risk0001#CLAIM-001

# Evidence Reviewed

- ticket:risk0001
- evidence:evidence-gate-structural-check
- `after/rules/07-validation-and-honesty.md`

# Residual Risks

The evidence rule could still be read as allowing weak proof if the follow-up
does not define sufficiency.

# Required Follow-up

Clarify evidence minimums before closure.

# Acceptance Recommendation

Keep ticket:risk0001 in `review_required`.
