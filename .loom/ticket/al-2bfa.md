---
"id": "al-2bfa"
"status": "in_progress"
"deps":
- "al-041e"
- "al-6677"
- "al-7193"
- "al-aee1"
"links": []
"created": "2026-02-16T05:32:27Z"
"type": "task"
"priority": 2
"assignee": "z3z1ma"
"parent": "al-1696"
"tags":
- "team"
- "refactor"
- "modularity"
- "tests"
- "sprint:Modular-refinement"
"external": {}
---
# Team decomposition regression pass: boundary + parity verification

Objective alignment:
Refactoring for modularity only has value if behavior parity and architectural boundaries are enforced. This ticket provides the fan-in verification pass after extraction tickets land.

Scope:
- Add/adjust regression coverage to prove extracted modules preserve command-level behavior for objective/sprint, send policy, spawn planning, and wait/check-in flows.
- Add architectural assertions where practical (for example import-direction or module ownership checks) to prevent regressions back into monolithic core patterns.
- Validate no duplicate output helpers or command-handler logic leakage are introduced (per team module guardrails).

Non-goals:
- No new product features.
- No additional decomposition beyond fixes required to satisfy parity/boundary checks.

Implementation plan:
1) Build focused regression matrix from impacted command families and existing test modules.
2) Add targeted assertions for module-boundary invariants (core delegates, no command->command imports, no duplicate serializer paths).
3) Run full team test suite and resolve any parity regressions introduced by prior extraction tickets.
4) Document any remaining high-risk hotspots in ticket notes for next sprint planning.

Verification:
- uv run pytest tests/test_team_*.py
- uv run ruff check .
- uv run basedpyright

Risks/edge cases:
- Overly strict boundary tests can create brittle false positives; keep checks focused on intended contracts.
- Parallel refactor merges can hide regressions until full suite run; this ticket must run after dependencies complete.
- If parity failures expose latent pre-existing bugs, separate them into follow-up tickets rather than widening scope.

## Acceptance Criteria

- Regression suite demonstrates no command-level behavior changes from decomposition work.
- Boundary checks enforce key module guardrails and pass in CI/local verification.
- Any unresolved modularity risks are captured explicitly for subsequent sprint planning.

## Notes

**2026-02-16T06:39:22Z**

Started regression/boundary verification pass. Next: inspect current team tests, identify parity/boundary gaps, then implement targeted assertions.

**2026-02-16T06:41:05Z**

Progress: audited current team regression coverage and module layout. Existing tests cover sprint/send/spawn/wait paths well; objective command parity and explicit team boundary invariants are the main remaining gaps. Also acknowledged manager inbox check-in (msg 7d4e296025d0) and reported no blockers.

**2026-02-16T06:42:14Z**

Implemented boundary/parity updates: added Team decomposition guardrails (core delegation checks for objective/send/spawn/wait; no team command handler imports to team.cli or other command modules), added objective command parity tests, and removed team.commands.inbox ack dependency on team.cli by calling core.inbox_ack directly. Updated spawn headcount tests for role-gating parity.
