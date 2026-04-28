---
id: ticket:k7p4s2q9
kind: ticket
status: closed
change_class: behavior-contract
risk_class: medium
created_at: 2026-04-28T07:47:02Z
updated_at: 2026-04-28T18:47:27Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:superpowers-skill-workflow-adaptation
  evidence:
    - evidence:superpowers-workflow-adaptation-validation
  critique:
    - critique:superpowers-workflow-adaptation-review
external_refs:
  github:
    - https://github.com/obra/superpowers/tree/main/skills
depends_on: []
---

# Summary

Adapt every meaningful Superpowers skill into Loom's workflow vocabulary by adding only the first-class Loom workflow surfaces that are missing and tightening existing Loom skills where Superpowers concepts are already owned.

# Context

The operator asked to clone `obra/superpowers`, read Loom's README and full skill corpus, read every meaningful Superpowers skill, then adapt all Superpowers workflows that Loom does not already express.

Loom's constitution requires new workflows to compose over existing owner layers instead of creating new canonical truth layers or helper-owned behavior.

# Why Now

`constitution:main` identifies workflow regularity, execution waves, debug/spike/sketch/ship routes, and retrospective-prevention guidance as current product direction. Superpowers is already cited as an influence in `README.md`; this ticket makes that influence concrete in Loom's own layer model.

# Scope

- inspect the current Loom `skills/` corpus and `README.md`
- inspect every meaningful skill under `obra/superpowers/skills`
- record the adaptation analysis in research
- add new Loom workflow skills only where the capability is not already first-class
- deepen existing Loom skills where the Superpowers concept is already owned by a Loom subsystem
- keep all workflows composed through constitution, initiative, research, spec, plan, ticket, packet, evidence, critique, wiki, memory, source, and Git ownership boundaries
- update public skill maps and package/install surfaces as needed

# Non-goals

- do not copy Superpowers verbatim as a second methodology namespace
- do not add a runtime, command wrapper, hidden helper, or new canonical layer
- do not make Superpowers terminology outrank Loom's layer ownership model
- do not change harness packaging beyond exposing any new canonical skills already in `skills/`

# Acceptance Criteria

- every Superpowers skill is mapped to either an existing Loom skill update or a new Loom workflow skill
- new skills have clear activation descriptions, owner boundaries, procedures, and references/templates where useful
- existing skill changes preserve their owner boundaries and do not create duplicate ledgers
- README/package skill maps reflect any new canonical skills
- structural validation confirms skill frontmatter and references are coherent
- critique is performed or explicitly recorded before closure because this changes operator workflow behavior

# Coverage

Covers:

- ticket:k7p4s2q9/adapt-superpowers-skills

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| Every meaningful Superpowers skill is accounted for. | `evidence:superpowers-workflow-adaptation-validation` | `critique:superpowers-workflow-adaptation-review#FIND-003` | supported |
| Added or updated Loom skills preserve layer ownership. | `evidence:superpowers-workflow-adaptation-validation` | `critique:superpowers-workflow-adaptation-review#FIND-001`, `critique:superpowers-workflow-adaptation-review#FIND-002`, `critique:superpowers-workflow-adaptation-review#FIND-005` | supported |
| Public skill maps remain aligned with the product surface. | `evidence:superpowers-workflow-adaptation-validation` | `critique:superpowers-workflow-adaptation-review#FIND-004` | supported |

# Execution Notes

Initial route: research and local protocol edit. Ralph is not used because the operator explicitly asked the current agent to perform the full adaptation and the work requires parent-level synthesis across the product corpus.

# Blockers

None.

# Next Move / Next Route

Research and local edit, then evidence recording and direct critique.

# Ralph Readiness

Not applicable. This ticket is being handled as a parent-side protocol authoring pass rather than a child implementation packet.

# Evidence

Expected evidence:

- Superpowers skill inventory and mapping in `research:superpowers-skill-workflow-adaptation`
- structural grep/diff validation after edits in `evidence:superpowers-workflow-adaptation-validation`
- critique record for workflow-surface risks

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale: This changes how operators route work through Loom, but it should preserve existing layer ownership rather than changing constitutional authority.

Required critique profiles:

- workflow-boundary
- operator-surface

Findings:

- `critique:superpowers-workflow-adaptation-review#FIND-001` - resolved
- `critique:superpowers-workflow-adaptation-review#FIND-002` - resolved
- `critique:superpowers-workflow-adaptation-review#FIND-003` - resolved
- `critique:superpowers-workflow-adaptation-review#FIND-004` - resolved
- `critique:superpowers-workflow-adaptation-review#FIND-005` - resolved

Disposition status: completed

Deferral / not-required rationale:

None.

# Wiki Disposition

Not required as a separate wiki promotion for this ticket. The accepted workflow knowledge lives directly in shipped skills, README, and PROTOCOL. A future golden example remains useful but is not required for this adaptation.

# Acceptance Decision

Accepted by: operator
Accepted at: 2026-04-28T18:47:27Z
Basis: Operator accepted the completed adaptation after linked validation evidence and recommended critique showed all findings resolved.
Residual risks: Future golden examples may still be useful, but they are not required for this adaptation's closure.

# Dependencies

Depends on `constitution:main`, `decision:0001`, `decision:0002`, `decision:0004`, `decision:0006`, and the existing skill-authoring guidance.

# Journal

- 2026-04-28T07:47:02Z: Created ticket after cloning Superpowers into `/tmp/loom-superpowers.vDNOwa` and reading the repository README, constitution, workspace routing guidance, and skill-authoring guidance.
- 2026-04-28T07:58:23Z: Completed the adaptation matrix, updated existing Loom workflow skills instead of adding a Superpowers namespace, and recorded structural validation in `evidence:superpowers-workflow-adaptation-validation`. Critique remains pending.
- 2026-04-28T08:05:59Z: Recorded `critique:superpowers-workflow-adaptation-review`; all four findings were resolved, and the ticket moved to `complete_pending_acceptance` pending operator acceptance.
- 2026-04-28T15:35:47Z: Fixed operator-reported leakage in `skills/loom-critique/references/critique-lens.md` by replacing package-specific `product-surface` language with repository-agnostic `operator-surface` guidance. Verified no matching leakage strings remain in `skills/` and recorded `FIND-005` as resolved.
- 2026-04-28T18:47:27Z: Operator accepted the completed work and closed the ticket.
