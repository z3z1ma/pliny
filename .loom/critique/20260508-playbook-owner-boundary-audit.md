---
id: critique:playbook-owner-boundary-audit
kind: critique
status: final
created_at: 2026-05-08T02:21:22Z
updated_at: 2026-05-08T02:25:02Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:plybk508 owner-boundary-pruned optional playbook set"
links:
  ticket:
    - ticket:plybk508
  evidence:
    - evidence:peer-playbook-integration-check
  research:
    - research:peer-playbook-integration-candidates
  spec:
    - spec:core-and-playbooks-package-contract
external_refs: {}
---

# Summary

Reviewed the reduced `loom-playbooks` set after applying the stricter owner-layer
boundary: optional playbooks may remain only when they provide genuine workflow
composition or specialist discipline on top of core owner layers. Playbooks that
merely duplicate core owner skills or mandatory using-Loom doctrine should be
removed or routed to core.

# Review Target

Target: `ticket:plybk508` current uncommitted diff after pruning:

- removed `loom-planning`, `loom-spec-driven`, and `loom-verification`
- renamed/tightened `loom-docs-adrs` into `loom-docs-sync`
- updated active playbook references to route plan/spec/verification truth to core
- amended `spec:core-and-playbooks-package-contract#REQ-004`
- amended `plan:split-core-and-playbooks-packages` playbook membership
- amended `research:peer-playbook-integration-candidates`
- refreshed `evidence:peer-playbook-integration-check`

Profiles: `protocol-change`, `operator-clarity`, `skill-boundary`.

# Verdict

`pass_with_findings`

The current 22-playbook package passes the owner-layer boundary audit. No further
optional playbook needs removal under the strict criterion. The prior stale 25-skill
evidence/critique state was a closure blocker until the evidence and ticket were
reconciled for the pruned set.

# Findings

## FIND-001: Acceptance records still pointed to the pre-prune 25-skill state

Severity: medium
Confidence: high
State: resolved

Observation:

After pruning, package smoke reported `skillCount: 22`, but the existing evidence
and prior critique still described the pre-prune 25-skill package state.

Why it matters:

Tickets are the live ledger and evidence must match the current package surface.
Closing against stale 25-skill evidence would incorrectly accept removed playbooks
as still present and reviewed.

Resolution:

`evidence:peer-playbook-integration-check` now records the owner-boundary-pruned
22-skill package smoke, dry-run pack output, changed-surface scans over 38 changed
`loom-playbooks/skills` files, removed-playbook active-reference checks, and scoped
diff whitespace checks. `ticket:plybk508` consumes that refreshed evidence and this
critique before closure.

Challenges:

- `ticket:plybk508#ACC-004`
- `ticket:plybk508#ACC-005`
- `ticket:plybk508#ACC-006`

# Evidence Reviewed

- `loom-playbooks/skills/*/SKILL.md`
- `loom-playbooks/skills/*/references/*.md`
- `spec:core-and-playbooks-package-contract#REQ-004`
- `plan:split-core-and-playbooks-packages` playbook membership
- `research:peer-playbook-integration-candidates`
- `ticket:plybk508`
- `evidence:peer-playbook-integration-check`
- package smoke output showing `skillCount: 22`
- npm dry-run pack output showing 58 total files
- changed-surface and tracked-diff scans for removed playbook references,
  placeholders, rejected peer runtime terms, and required runtime wording

# Residual Risks

- Long-term operator clarity remains empirical; future use may reveal overlap among
  remaining specialist playbooks that should be tightened later.
- Core owner layers intentionally receive spec-first, planning, verification, and
  ADR/decision material instead of playbook wrappers; this audit did not expand core
  documentation with every peer detail.
- Harness runtime behavior beyond local OpenCode smoke remains outside this review.

# Required Follow-up

- Record ticket-owned disposition for `FIND-001` before closure.

# Acceptance Recommendation

`accept-after-ticket-reconciliation`

After the ticket records refreshed evidence, completed critique disposition, and
the resolved medium finding, no owner-boundary blocker remains.
