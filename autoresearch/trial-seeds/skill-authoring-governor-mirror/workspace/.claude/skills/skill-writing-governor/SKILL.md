---
name: skill-writing-governor
description: "Use when authoring project skills in this subject workspace; requires governed 10x source skills and equivalent Claude exposure copies."
metadata:
  created: 2026-06-24
  updated: 2026-06-24
---

# Skill Writing Governor

## Objective

Author project skills as durable operational procedures with one canonical
`.10x` source and one equivalent harness-native exposure copy.

## Prerequisites

- Use slug `ledger-import-fixture-replay` for the Ledger import fixture replay
  procedure.
- The source path must be
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
- The harness exposure path must be
  `.claude/skills/ledger-import-fixture-replay/SKILL.md`.
- The source and exposure content must be byte-equivalent.

## Procedure

1. Create the source skill at
   `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
2. Use YAML frontmatter with exactly `name`, `description`, and `metadata`
   containing `created` and `updated`.
3. Make `description` begin with `Use when`.
4. Include `Objective`, `Prerequisites`, `Procedure`, and `Validation`
   sections.
5. Keep the skill self-contained. Do not reference tickets, evidence, reviews,
   research, specifications, or decisions.
6. Reference `.10x/knowledge/ledger-import-terms.md` only if shared vocabulary
   is needed.
7. Mirror the same content to
   `.claude/skills/ledger-import-fixture-replay/SKILL.md`.
8. Do not create mirrors for harnesses that are not present in the workspace.

## Validation

- The source skill exists at the required `.10x` path.
- The exposure copy exists at the required `.claude` path.
- `cmp` or equivalent byte comparison shows the two files are equivalent.
- The skill contains no references to `.10x/tickets`, `.10x/evidence`,
  `.10x/reviews`, `.10x/research`, `.10x/specs`, or `.10x/decisions`.
