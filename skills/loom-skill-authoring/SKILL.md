---
name: loom-skill-authoring
description: "Create or refine Loom-compatible skills that are scoped, durable, discoverable, and template-backed. Use when adding a new subsystem skill, tightening a skill description, extending references/templates, or auditing a skill for overlap, ambiguity, or anti-patterns."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: authoring
---

# loom-skill-authoring

Use this skill to author Loom-compatible skills.

## What This Skill Owns

- skill activation descriptions
- skill boundaries and overlap review
- skill review and pressure-scenario validation
- skill directory structure
- reference/template placement
- anti-pattern review for hidden runtimes or vague ownership

## What Good Loom Skills Do

A good Loom skill:

- has a clear activation description
- owns one subsystem or one coherent capability
- tells the agent what it governs and what it does not
- teaches a practical procedure
- provides references for nuanced judgment
- provides templates when artifact creation is part of the workflow

## Use This Skill When

- you are adding a new skill
- you are collapsing duplicate skills
- you are tightening a vague skill description
- you are deciding whether a subsystem should exist as its own skill

## Do Not Use This Skill When

- the work really belongs to a canonical project record
- the "new skill" is just a one-off task
- you are trying to hide core rules inside a skill that should really be always-on doctrine

## Done Means

- the skill has a clear activation description
- the skill states what it owns and what it does not own
- references and templates are placed only where they serve the skill boundary
- the skill does not duplicate another owner or create a hidden runtime

## Read In This Order

Read immediately for skill authoring:

1. `references/principles.md` when deciding whether a skill should exist and
   what it should own.
2. `references/structure.md` when laying out files, references, and templates.

Then read conditionally:

3. `references/anti-patterns.md` when checking overlap, hidden runtime
   dependency, or vague activation.
4. `references/skill-review.md` when a skill changes operator behavior,
   discipline, routing, or protocol authority and needs pressure-testing or
   critique before acceptance.
5. The relevant template only when creating a new skill.
