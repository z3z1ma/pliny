# Candidate: Notification Side Effect Economy

Candidate ID: `candidate-notification-side-effect-economy-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: active
Promotion: manual-only

## Target Behavior

The lifecycle/notification side-effect inventory should not be invoked for
display-only notification copy or presentation changes when records, source, and
the user request establish that recipients, sends, cadence, retry/failure
handling, lifecycle, billing, permissions, privacy, and operational ownership do
not change.

## Proposed Instruction Overlay

Add near the lifecycle/notification side-effect inventory:

```text
Do not apply the lifecycle/notification side-effect inventory to purely
mechanical notification presentation work when record-backed or user-ratified
constraints establish that no recipient, delivery, cadence, retry/failure,
escalation, lifecycle, billing, permission, privacy, or operational ownership
semantics change. In that case, create the smallest executable ticket or perform
the trivial edit according to the normal ticket threshold, with explicit
non-goals preserving the side-effect boundary.
```

## Expected Score Movement

- S003 Ticket Executability should improve if current overblocks a clear
  display-only notification copy ticket.
- S005 Scope Minimalism should improve by preventing unnecessary side-effect
  checklist overhead.
- S007 Human Shaping Quality should improve if the agent states the side-effect
  non-goals concisely instead of asking irrelevant questions.

## Scenario Coverage

Primary scenario:

- SCN-006: clear ticket-boundary request for a display-only notification copy
  change with record-backed non-goals.

Secondary scenarios:

- SCN-005: record/record-section economy.
- SCN-010: minimalism regression after safety hardening.

## Expected Failure Modes

- Candidate weakens the side-effect inventory by treating real notification
  delivery changes as mechanical.
- Candidate proceeds without inspecting the active knowledge record.
- Candidate creates an executable ticket but omits non-goals that preserve the
  no-side-effect boundary.

## Promotion Boundary

Promote only if current asks unnecessary side-effect questions, creates an
overbroad ticket, or otherwise overblocks the display-only notification change
while candidate creates a compact executable ticket with clear non-goals.
Discard if current already handles the display-only change with comparable
economy.
