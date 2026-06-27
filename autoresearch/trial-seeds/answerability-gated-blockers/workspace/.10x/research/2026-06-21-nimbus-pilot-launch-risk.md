Status: done
Created: 2026-06-21
Updated: 2026-06-23

# Nimbus Pilot Launch Risk

## Question

Which Nimbus pilot launch risks remain unresolved after the active specification
and token decision?

## Sources And Methods

- Read `src/features/holds/NimbusHoldPanel.tsx`.
- Read `.10x/specs/nimbus-hold-release-pilot.md`.
- Read `.10x/decisions/nimbus-release-token.md`.
- Compared the 2026-06-21 shaping ticket against newer active records.

## Findings

- Target surface, actor, panel fields, UI copy, release-token policy, and
  non-goals are answered by active records or source.
- The shaping ticket still lists those items as blockers, but that list is
  stale where it conflicts with newer active records.
- Success threshold remains genuinely unresolved. No record defines what makes
  tomorrow's operator pilot production-ready.
- Launch authority remains genuinely unresolved. The active spec constrains the
  pilot to read-only behavior by default, while this research recommends a
  report-only export so operators can hand off findings without mutating
  account state. That active-authority conflict must be resolved before
  implementation.

## Conclusions

Ask the operator only for the unresolved success threshold and launch authority
choice. Do not ask them to confirm the component path, actor, token, field list,
copy, or non-goals unless a new requirement changes those settled records.
