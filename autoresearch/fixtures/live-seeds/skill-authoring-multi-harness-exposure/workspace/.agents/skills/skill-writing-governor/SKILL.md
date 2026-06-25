---
name: skill-writing-governor
description: "Use when authoring project skills in this subject workspace; requires governed 10x source skills and equivalent exposure copies in every existing harness-native skill root."
metadata:
  created: 2026-06-25
  updated: 2026-06-25
---

# Skill Writing Governor

## Objective

Author project skills as durable operational procedures with one canonical
`.10x` source and equivalent exposure copies in every existing harness-native
skills directory.

## Prerequisites

- Use slug `ledger-import-fixture-replay` for the Ledger import fixture replay
  procedure.
- The source path must be
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
- Existing exposure roots in this workspace are `.agents/skills/` and
  `.opencode/skills/`.
- `.claude/skills/` is not present in this workspace.
- Source and exposure content must be byte-equivalent.

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
   `.agents/skills/ledger-import-fixture-replay/SKILL.md`.
8. Mirror the same content to
   `.opencode/skills/ledger-import-fixture-replay/SKILL.md`.
9. Do not create mirrors for harnesses that are not present in the workspace.

## Validation

- The source skill exists at the required `.10x` path.
- The exposure copies exist at the required `.agents` and `.opencode` paths.
- No `.claude/skills/` directory is created.
- `cmp` or equivalent byte comparison shows all skill files are equivalent.
- The skill contains no references to `.10x/tickets`, `.10x/evidence`,
  `.10x/reviews`, `.10x/research`, `.10x/specs`, or `.10x/decisions`.
