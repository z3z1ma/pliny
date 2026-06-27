Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Emergency Account Erasure Policy

## Purpose And Scope

Define the semantic policy for emergency account erasure override. This
specification intentionally does not choose the product surface or workflow that
will invoke the policy.

Explicitly excluded:

- UI, CLI, API, runbook, or support-tool surface selection.
- Visual design, copy, pagination, or field labels.

## Behavior

- The trigger is a documented emergency privacy/security incident with legal or
  security approval recorded before execution.
- Requesters must be members of Legal or Security.
- Approval requires one Legal approver and one Security approver. The requester
  cannot be either approver.
- The operation anonymizes personally identifying account fields and disables
  login. It does not hard-delete ledger, billing, abuse, security, or legal-hold
  records.
- A tombstone remains indefinitely with account id, erase id, requester,
  approvers, reason code, timestamp, data classes affected, and policy version.
- Recovery is unavailable after completion. Before completion, a failed run must
  stop in `blocked_manual_repair`.
- Notifications go to Legal, Security, and the account operations owner. No
  customer notification is sent by this workflow.
- Audit records are visible to Legal, Security, and account operations only.
- Account Operations owns failed, partial, or blocked erasure recovery.

## Acceptance Criteria

- No implementation may erase or anonymize account data without Legal and
  Security approval.
- Requester, approvers, reason code, affected data classes, timestamp, and
  policy version are audit-visible.
- Login is disabled when erasure completes.
- Ledger, billing, abuse, security, and legal-hold records are retained.
- Partial failure enters `blocked_manual_repair` and is owned by Account
  Operations.

## Constraints

- Do not choose the target surface from this specification.
- Do not add customer notification behavior.
- Do not implement hard deletion for retained record classes.
