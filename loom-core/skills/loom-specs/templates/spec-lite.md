---
id: spec:<slug>
kind: spec
status: draft
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
external_refs: {}
---

# Summary

What this spec defines, who or what surface it affects, and why a compact behavior
contract is enough.

Use this lite template only when the behavior is local, low-risk, and small enough
that focused requirements, scenarios, acceptance, and evidence expectations are
sufficient. Escalate to `spec.md` when any full-template trigger applies.

# Problem

What ambiguity, user need, quality gap, or owner-record mismatch requires a
behavior contract.

Baseline / current state:

- <TBD or None - reason>

# Desired Behavior

What the system, workflow, or record should do, stated as observable behavior
rather than delivery trivia.

Non-goals:

- <TBD or None - reason>

# Requirements

Concrete behavior requirements downstream work must satisfy. Use stable IDs when
tickets, packets, evidence, critique, or wiki may cite the requirement.

- REQ-001: <MUST/SHALL/SHOULD + actor/surface + condition + observable outcome>

# Scenarios

Representative usage, edge cases, or failure paths that can be tested, observed,
or explicitly validated.

## SCN-001: <scenario name>

Exercises: REQ-001, ACC-001

GIVEN <initial observable state>
WHEN <trigger or action>
THEN <observable outcome>
AND <additional outcome or invariant when useful>

# Acceptance

What will count as acceptable behavior. Criteria must be specific enough for
tickets, evidence, and critique to cite.

- ACC-001: <TBD: stable acceptance criterion before saving>

# Evidence Plan

What evidence would prove the behavior and quality bar. Name tests, observations,
before/after artifacts, screenshots, smoke checks, or manual checks as applicable.

- ACC-001: <TBD: evidence type, expected artifact, and limits>

# Open Questions

Unresolved questions that do not yet block the current contract, or explicit
blocking questions that must be routed before downstream work.

- <TBD or None - current contract is ready>
