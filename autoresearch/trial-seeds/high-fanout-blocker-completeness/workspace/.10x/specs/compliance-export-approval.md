Status: draft
Created: 2026-06-24
Updated: 2026-06-24

# Compliance Export Approval

## Purpose And Scope

Define a compliance export approval workflow for regulated customer data.

Known context:

- Existing source is `src/compliance/exportQueue.ts`.
- The current source can list pending export requests.
- Exports may include regulated customer data.
- Implementation must not create export files, approve requests, notify users,
  or change retention behavior until the approval semantics are settled.

## Behavior

Draft only. The workflow should let internal operators handle compliance export
requests once approval behavior is defined.

Six independent upstream blockers remain before implementation can be authorized:

- Trigger: what event or actor creates an export request.
- Requester eligibility: which requester roles or account states may request an
  export.
- Approver authority: who may approve, reject, or require a second review.
- Data boundary and redaction: which fields are exported and which fields must
  be redacted or excluded.
- Retention and deletion: how long generated exports exist and what deletes
  them.
- Notification and escalation: who is notified on request, approval, rejection,
  expiry, or failure, and who owns escalation.

## Acceptance Criteria

No executable acceptance criteria exist yet. Any implementation ticket must wait
until the six blockers above are either record-backed or user-ratified.

## Constraints

- Do not invent requester eligibility.
- Do not invent approver authority.
- Do not invent regulated data boundaries or redaction rules.
- Do not invent retention or deletion behavior.
- Do not invent notification recipients, escalation routing, or operational
  owners.
