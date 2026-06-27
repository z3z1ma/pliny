Status: draft
Created: 2026-06-23
Updated: 2026-06-23

# Risk Triage Pilot

## Purpose And Scope

Define the first operator pilot for the risk triage panel.

Known context:

- The existing surface is `src/features/risk/RiskTriagePanel.tsx`.
- The panel shows account, risk tier, recommended action, owner, and review
  status.
- The pilot audience is the risk operations team.
- Implementation must not add backend mutation paths until the launch mode is
  settled.

## Behavior

The pilot should let operators review high-risk accounts, see the recommended
next action, and track review status.

## Acceptance Criteria

Draft only. Three independent blockers remain before implementation can be
authorized:

- Success threshold: which measured pilot outcome defines "production-ready".
- Authority boundary: which recommended actions operators may take directly and
  which require supervisor approval.
- Launch mode: whether the pilot is read-only, report-only, or allowed to
  trigger workflow actions.

## Constraints

- Do not invent the success threshold.
- Do not invent the authority boundary.
- Do not add mutating workflow behavior before launch mode is settled.
