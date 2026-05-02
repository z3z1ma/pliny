---
id: critique:<slug>
kind: critique
status: draft
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
review_target: <scalar record ref, path, PR, branch, commit, diff range, or target summary>
links: {}
external_refs: {}
---

# Summary

What this critique reviewed.

# Review Target

Name the specific target and why it was reviewed. The frontmatter
`review_target` field for a direct critique record is intentionally a scalar,
human-readable search handle. For code review, name the branch, commit, diff
range, pull request, or changed file set here rather than nesting structured
metadata in the critique record frontmatter.

# Verdict

Use one verdict value and explain it:

- `pass`
- `pass_with_findings`
- `changes_required`
- `inconclusive`

Set `status: final` only when evidence reviewed, findings, residual risks, and
acceptance recommendation are complete enough for the ticket to consume. Final
critique status does not close the ticket.

# Findings

List concrete findings with stable finding IDs. Remove the example finding or
write `None - no findings` when no finding applies.

## FIND-<nnn>: Short finding title

Severity: <TBD: choose low, medium, or high>
Confidence: <TBD: choose low, medium, or high>
State: <TBD: choose open or withdrawn>

Observation:

Why it matters:

Follow-up:

If `State: withdrawn`, record the withdrawal rationale here. Withdrawn findings
may be cited by tickets for audit history, but they do not require ticket-owned
finding dispositions.

When recommending follow-up work, cite an existing or proposed ticket reference
when practical, for example `ticket:<token>`. Tickets consume this as a
ticket-owned disposition such as `critique:example-review#FIND-001` — converted
to follow-up ticket `ticket:<token>`.

Do not record `resolved`, `accepted_risk`, `superseded`, or
`converted_to_follow_up` as critique-owned state. Those are ticket-owned finding
dispositions recorded in the ticket acceptance gate.

For claim-specific findings, include:

Challenges:

List real qualified claim IDs, or write `None - not claim-specific`.

# Evidence Reviewed

What records, files, diffs, tests, outputs, or evidence were inspected.

# Residual Risks

What still looks risky after the review.

# Required Follow-up

What should happen before acceptance or closure.

# Acceptance Recommendation

Use a concrete recommendation: close-ready, complete pending acceptance,
review required, active follow-up required, blocked, or accepted risk needed.
This recommendation informs the ticket-owned acceptance decision; it does not
close the ticket by itself.
