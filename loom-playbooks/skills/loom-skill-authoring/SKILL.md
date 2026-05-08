---
name: loom-skill-authoring
description: "Maintain Loom-compatible skills. Use when adding, tightening, reviewing, or auditing skill boundaries, activation descriptions, common triggers, templates, references, routing, or anti-rationalization guidance."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: authoring
---

# loom-skill-authoring

Use this skill to author Loom-compatible skills.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Skill Owns

- skill activation descriptions
- skill frontmatter and metadata conventions
- skill boundaries and overlap review
- skill review and pressure-scenario validation
- skill directory structure
- reference/template placement
- anti-pattern review for hidden runtimes or vague ownership
- skill-routing and pressure-scenario adaptation from peer skill systems

## What Good Loom Skills Do

A good Loom skill:

- has a broad activation description that names ordinary user/task triggers and
  owner boundaries
- uses frontmatter metadata consistently with the skill boundary
- owns one subsystem or one coherent capability
- tells the agent what it governs and what it does not
- teaches a practical procedure
- names common rationalizations when agents are likely to skip the discipline
- names red flags that show the skill is being violated
- ends with evidence-backed verification, not a vibe check
- provides references for nuanced judgment
- provides templates when artifact creation is part of the workflow

## Pressure-Scenario Validation

When a skill change affects routing, verification, critique, acceptance, closure,
or operator discipline, test the behavior with at least one realistic pressure
scenario when proportional.

Use the smallest honest loop:

1. RED: name the prompt-shaped temptation the old or missing guidance would likely
   mishandle, such as "skip formalities", "the fix is obvious", "the screenshot
   looks fine", or "the child said done".
2. GREEN: edit the smallest skill surface that makes the correct Loom route,
   owner record, or refusal obvious.
3. REFACTOR: remove duplicate prose, hidden runtime assumptions, over-broad
   activation, or new owner ambiguity introduced by the fix.

Preserve the scenario in evidence or critique when the ticket needs durable
support. For small wording edits, a written scenario plus structural review may be
enough; do not invent a hidden skill-test harness.

## Use This Skill When

- you are adding a new skill
- you are collapsing duplicate skills
- you are tightening a vague skill description
- you are deciding whether a subsystem should exist as its own skill

## Do Not Use This Skill When

- the work really belongs to a canonical project record
- the "new skill" is just a one-off task
- you are trying to hide core rules inside a skill that should really be always-on doctrine

## Common Rationalizations

- **Rationalization:** "The skill reads well, so it is done."
  **Reality:** Skill edits change future operator behavior; validation must check activation, boundaries, references, templates, and proportional evidence.
- **Rationalization:** "This rule can live in the new skill only."
  **Reality:** Always-on doctrine belongs in using-Loom; owner truth belongs in owner records. Skills coordinate behavior without hiding core policy.
- **Rationalization:** "A broad description means the skill owns all related truth."
  **Reality:** Broad activation improves discovery. Durable truth still routes to the owning Loom layer.
- **Rationalization:** "The pressure scenario is obvious, so I do not need to write it down."
  **Reality:** Behavior-changing skill edits need a concrete check against the rationalization they are meant to prevent.

## Red Flags

- activation is too vague for an agent to know when to load the skill
- the skill duplicates another owner or creates a shadow owner layer
- required references are a bare index instead of immediate versus conditional reads
- templates introduce placeholder IDs, vague completion claims, or hidden runtime assumptions
- verification is only the author's confidence that the prose sounds right
- behavior-changing guidance lacks a pressure scenario, critique, or evidence posture proportional to risk

## Verification

- [ ] Frontmatter names `name`, `description`, `compatibility`, and appropriate `metadata`.
- [ ] The description names ordinary activation triggers without becoming the workflow shortcut.
- [ ] Ownership boundaries and non-owners are clear enough to prevent overlap.
- [ ] References are immediate or conditional for a stated reason.
- [ ] Templates exist only for artifact shapes the skill owns.
- [ ] Behavior-changing edits have structural checks, pressure scenarios, critique, or evidence proportional to risk.
- [ ] Pressure scenarios target real shortcut prompts and do not require hidden runtime machinery.

## Done Means

- the skill has a broad activation description with ordinary triggers, aliases,
  and owner boundaries where relevant
- frontmatter names `name`, `description`, `compatibility`, and appropriate
  `metadata` fields
- the skill states what it owns and what it does not own
- the skill teaches process over reference knowledge
- common rationalizations, red flags, and verification are present when they would
  change agent behavior
- references and templates are placed only where they serve the skill boundary
- the skill does not duplicate another owner or create a hidden runtime

## Read In This Order

Read immediately for skill authoring:

1. `references/principles.md` when deciding whether a skill should exist and
   what it should own.
2. `references/structure.md` when laying out files, references, and templates.
3. `references/skill-routing-and-pressure-testing.md` when adapting peer skills,
   designing activation boundaries, or testing skills against rationalizations.

Then read conditionally:

4. `references/anti-patterns.md` when checking overlap, hidden runtime
   dependency, or vague activation.
5. `references/skill-review.md` when a skill changes operator behavior,
   discipline, routing, or protocol authority and needs pressure-testing or
   critique before acceptance.
6. `templates/simple-skill.md` when creating an owner-layer, workflow, support,
   shared-grammar, inner-loop, control-plane, entry-doctrine, or authoring skill with a
   single coherent boundary.
7. `templates/router-skill.md` when creating a workflow coordinator that routes
   among multiple owner layers without owning a new truth layer.
