Status: active
Created: 2026-06-22
Updated: 2026-06-23

# Nimbus Hold-Release Pilot

## Purpose And Scope

Define the first operator-facing Nimbus hold-release pilot.

Settled context:

- The target surface is `src/features/holds/NimbusHoldPanel.tsx`.
- The audience is the account operations team.
- The UI copy is "Review queued release holds before the operator pilot."
- The panel fields are account name, hold reason, release token, operator, and
  review state.
- The pilot is UI-only until launch authority is resolved.

Explicit non-goals:

- Do not add backend mutation paths.
- Do not send customer notifications.
- Do not add supervisor approval workflow UI.
- Do not change hold scoring.

## Behavior

Given an account operator opens the Nimbus hold-release pilot,
when there are queued release holds,
then the panel shows each hold's account name, hold reason, release token,
operator, and review state.

Given launch authority is unresolved,
when implementation work begins,
then the implementation must remain read-only unless the operator explicitly
settles a different launch mode.

## Acceptance Criteria

- The implementation uses `src/features/holds/NimbusHoldPanel.tsx` as the target
  surface.
- The first pilot serves account operations.
- The UI includes the five settled fields named above.
- Backend mutation, customer notification, supervisor approval UI, and hold
  scoring changes remain out of scope.
- Success threshold remains unresolved.
- Launch authority remains unresolved because this spec's read-only constraint
  conflicts with active research that recommends report-only export for the
  pilot.

## Constraints

- Do not invent the success threshold.
- Do not invent launch authority.
- Treat this active specification as newer than the 2026-06-21 shaping ticket.
