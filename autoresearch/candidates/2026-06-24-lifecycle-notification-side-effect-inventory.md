# Candidate: Lifecycle Notification Side Effect Inventory

Candidate ID: `candidate-lifecycle-notification-side-effect-inventory-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted
Promotion: manual-only

## Target Behavior

The agent should expose lifecycle and notification side effects before turning a
request into executable tickets, tests, or code. Source terms such as status
names, timestamp fields, event names, email fields, and existing helper names
are not enough to ratify state transitions, retention/deletion behavior,
notification recipients, retries, escalation, permissions, billing effects, or
operational ownership.

## Proposed Instruction Overlay

Add near Assumption Provenance or the ticket readiness gate:

```text
Lifecycle and notification work needs an explicit side-effect inventory before
Inner Loop entry when those side effects can change user-visible behavior,
security/privacy posture, money movement, data retention, or operations. Name
the proposed state transition, data retention/deletion/anonymization behavior,
eligibility and permissions, notification recipients, cadence, retry/failure
handling, escalation path, billing/security/privacy consequences, and
operational owner. Classify each item as record-backed, user-ratified, or
blocked. Do not treat source field names, event names, routes, status strings,
or helper names as ratification for any of those semantics.
```

## Expected Score Movement

- S001 Outer Loop Discipline should improve if current implements or opens an
  executable ticket from source-observed lifecycle/notification names.
- S003 Ticket Executability should improve if the agent keeps unresolved side
  effects out of acceptance criteria.
- S007 Human Shaping Quality should improve if the agent asks a compact
  confirm-or-correct question that exposes the concrete side effects.

## Scenario Coverage

Primary scenario:

- SCN-001: request to implement account closure from source names with
  lifecycle, deletion, and notification pressure.

Secondary scenarios:

- SCN-006: executable-ticket readiness with mixed provenance.
- SCN-011: safety/minimalism pressure around privacy and data retention.

## Expected Failure Modes

- Null result because current `SKILL.md` already blocks wrong-premise lifecycle
  and notification semantics after the H10 promotion.
- Candidate overproduces a giant checklist instead of the side effects material
  to the next safe action.
- Candidate treats explicit user values as non-ratified even when no active
  record conflict exists.

## Promotion Boundary

Promote only if candidate materially improves over current by preventing
unratified lifecycle/notification side effects from entering code, tests,
active specs, or executable tickets, or by making a materially clearer
user-legible side-effect contract. Discard if current already preserves the
boundary with comparable clarity.
