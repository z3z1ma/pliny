# Make Outer-Loop Shaping Mandatory For Ambiguity

ID: ticket:20260513-mandatory-shaping-doctrine
Type: Ticket
Status: closed
Created: 2026-05-13
Updated: 2026-05-13
Risk: medium - changes mandatory Core doctrine and aligned docs, but is prose-only and directly inspectable.

## Summary

Strengthen Loom Core doctrine so non-concrete asks must stay in outer-loop
shaping before execution. The closure claim is that shipped skill prose and
aligned restatements make ambiguity default to human-shaped engineering judgment,
not silent ticket, packet, or patch execution from inferred defaults.

## Related Records

- `loom-core/skills/using-loom/SKILL.md` - owns session-entry doctrine and routing posture.
- `loom-core/skills/using-loom/references/shaping-with-humans.md` - owns the canonical outer-loop shaping behavior.
- `loom-core/skills/using-loom/references/how-loom-thinks.md` - owns surface routing doctrine.
- `loom-core/skills/loom-tickets/references/creating-tickets.md` - constrains ticket readiness from shaped work.
- `evidence:20260513-mandatory-shaping-doctrine-checks` - records scans and package checks for closure.

## Scope

May change Core model-visible skill prose that controls session routing,
outer-loop shaping, ticket creation readiness, and implementation-playbook guards.
May update human-facing docs that restate that doctrine. Must not change adapter
load order, manifests, package entrypoints, hooks, runtime assumptions, or add a
new Loom surface.

## Acceptance

- ACC-001: `using-loom` explicitly states that ambiguity defaults to shaping and
  fuzzy asks must not be turned into ticket, packet, or patch execution before
  the direction-setting choices are shaped.
  - Evidence: source inspection plus targeted grep for the new ambiguity language.
  - Audit: separate audit would not add useful trust for this prose-only wording criterion.

- ACC-002: `shaping-with-humans` defines a concrete-ask gate and required shaping
  actions for non-concrete asks.
  - Evidence: source inspection plus targeted grep for the concrete-ask gate.
  - Audit: separate audit would not add useful trust for this prose-only wording criterion.

- ACC-003: ticket creation and implementation-playbook guidance prevent fuzzy asks
  from becoming premature executable tickets or implementation slices.
  - Evidence: source inspection of the ticket and playbook prose.
  - Audit: separate audit would not add useful trust for this prose-only wording criterion.

- ACC-004: human-facing protocol and package docs that restate the operating loop
  are aligned with the mandatory shaping gate.
  - Evidence: source inspection of updated docs.
  - Audit: separate audit would not add useful trust for this prose-only wording criterion.

- ACC-005: repository checks for Markdown/package surfaces still pass.
  - Evidence: `git diff --check`, Core smoke, Playbooks smoke, Core pack check, and Playbooks pack check.
  - Audit: command evidence is sufficient for syntax/package smoke claims.

## Current State

Closed. Core skill doctrine now makes ambiguity default to outer-loop shaping and
names the direction-setting choices that must be shaped before execution: scope,
exclusions, system-shape and state implications, design coherence, evidence
posture, and owning Loom surface. Ticket, plan, spec, delegation, and
implementation-playbook guidance now reinforce the same gate.
Human-facing docs are aligned but are not treated as the authoritative fix.

Evidence `evidence:20260513-mandatory-shaping-doctrine-checks` supports the
acceptance criteria. Separate audit was not performed because the criteria are
prose-inspection and package-check claims, and each criterion records why separate
audit would not add useful trust.

## Journal

- 2026-05-13: Created ticket with Status `active` from the operator request to
  strengthen mandatory outer-loop shaping language after evals showed agents
  jumping from fuzzy asks to execution without shaping the direction-setting
  judgment first.
- 2026-05-13: Reframed the change away from symptom-specific wording and into
  systemic skill-directory doctrine covering scope choices, system-shape and state
  implications, design coherence, and execution-readiness gates.
- 2026-05-13: Revised wording again after operator feedback that mirrored language
  was too literal. Replaced quoted concept labels with behavior-oriented doctrine
  about direction selection, exclusions, seams, state relationships, coherence, and
  surface ownership.
- 2026-05-13: Restored `data model` terminology where it is the correct
  engineering concept after operator feedback that the prior cleanup overcorrected.
  Reran targeted scans plus Markdown/package checks; evidence record updated.
- 2026-05-13: Recorded `evidence:20260513-mandatory-shaping-doctrine-checks` after
  targeted scans, `git diff --check`, Core smoke, Playbooks smoke, Core pack check,
  and Playbooks pack check passed. Closed the ticket.
