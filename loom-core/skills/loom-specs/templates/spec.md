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

What this spec defines and who should use it.

# Rigor Level

Choose the lightest useful shape: `lite` for local, low-risk behavior, or `full`
when public/shared interfaces, security/privacy, migrations, compatibility,
multiple tickets, or high ambiguity require more detail.

Rationale:

# Problem

What ambiguity, user need, or quality gap requires a behavior contract.

# Problem Pressure Check

Use only the lenses that matter; write `None - reason` when the pressure check is
not applicable.

- Evidence / baseline:
  - Current answer: <TBD or None - reason>
  - Disposition: <accepted, blocks, research, or owner route>
- Specific beneficiary or surface:
  - Current answer: <TBD or None - reason>
  - Disposition: <accepted, blocks, research, or owner route>
- Current workaround / counterfactual:
  - Current answer: <TBD or None - reason>
  - Disposition: <accepted, blocks, research, or owner route>
- Smallest valuable shape / solution attachment:
  - Current answer: <TBD or None - reason>
  - Disposition: <accepted, blocks, research, or owner route>
- Durability risk:
  - Current answer: <TBD or None - reason>
  - Disposition: <accepted, blocks, research, or owner route>

# Desired Behavior

What the system should do, stated as observable behavior rather than delivery trivia.

# Quality Bar

What would make the result materially better than the current or baseline state.
For UX/product work, name the primary user task, affordance, or quality delta a
reviewer should be able to observe.

# Options Considered

Use when multiple behavior, API, UX, architecture, or workflow shapes could fit.
Name two or three meaningful options, their tradeoffs, and why the chosen shape
fits the problem. If not applicable, write `None - reason`.

# Not Doing

Explicit non-goals and attractive exclusions that keep this contract focused.

# Boundary Tiers

Use only when authority or delivery boundaries matter; otherwise write
`None - reason`.

- Always:
- Ask first:
- Never:

# Interface / API Contract

Use for shared or public surfaces; otherwise write `N/A`.

- Inputs:
- Outputs:
- Error semantics:
- Validation boundary:
- Compatibility / deprecation:

# Examples / Non-Examples

Positive examples, negative examples, screenshots, references, concrete traits,
or anti-patterns. If none exist, write `None - reason`.

# Constraints

Boundaries, non-goals, compatibility requirements, safety limits, or design-system
rules that shape acceptable solutions.

# Requirements

Concrete behavior requirements downstream work must satisfy. Use stable IDs when
tickets, packets, evidence, critique, or wiki may cite the requirement. Keep each
requirement focused on one behavior, invariant, interface guarantee, error
semantic, or quality constraint.

- REQ-001: <MUST/SHALL/SHOULD + actor/surface + condition + observable outcome>

# Scenarios

Representative usage, edge cases, and failure paths. Each behavior-bearing
requirement should have at least one scenario that can be tested, observed, or
explicitly validated.

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

Coverage:

- ACC-001:
  - Requirements: REQ-001
  - Scenarios: SCN-001
  - Evidence target: <test, observation, screenshot, trace, or manual check>

# Evidence Plan

What evidence would prove the behavior and quality bar. Name tests, observations,
before/after artifacts, screenshots, smoke checks, or manual checks as applicable.

- ACC-001:
  - Evidence type: <test, observation, screenshot, trace, manual check>
  - Expected artifact: <path, command, evidence record, or TBD>
  - Limits / notes: <limits or None>

# Amendment Notes

Use when changing an existing spec. Otherwise write `None - new spec`.

- <added, modified, removed, renamed, or superseded>:
  - Affected IDs: <REQ/SCN/ACC IDs>
  - Disposition / successor: <reason, successor, compatibility, or removal boundary>
  - Reference reconciliation needed: <yes/no and target search>

# Contract Review

- Completeness: <material behavior, edge states, non-goals, constraints,
  acceptance IDs, and evidence expectations covered or explicitly out of scope>
- Correctness: <requirements reflect intended behavior and owner-record truth, not
  only current implementation or a preferred solution shape>
- Coherence: <requirements, scenarios, acceptance, interface details, and decision
  points use stable terms and do not contradict one another>

# Assumptions / Decision Points

Questions or assumptions whose answer would materially change behavior, UX,
architecture, acceptance, or risk.

- <TBD or None - no material assumptions>:
  - Reversible: <yes/no>
  - Blocks downstream work: <yes/no>
  - Disposition: <accepted, ask user, research, or spec follow-up>

# Open Questions

Unresolved questions that do not yet block the current contract, or explicit
blocking questions that must be routed before downstream work.
