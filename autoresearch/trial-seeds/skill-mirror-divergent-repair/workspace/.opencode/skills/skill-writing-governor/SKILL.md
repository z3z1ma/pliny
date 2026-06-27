---
name: skill-writing-governor
description: "Use when authoring, validating, or repairing project skills in this subject workspace; requires governed 10x source skills and equivalent OpenCode exposure copies."
metadata:
  created: 2026-06-24
  updated: 2026-06-24
---

# Skill Writing Governor

## Objective

Maintain project skills as durable operational procedures with one canonical
`.10x` source and one equivalent harness-native exposure copy.

## Prerequisites

- Use slug `ledger-import-fixture-replay` for the Ledger import fixture replay
  procedure.
- The canonical source path is
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
- The OpenCode exposure path is
  `.opencode/skills/ledger-import-fixture-replay/SKILL.md`.
- The source and exposure content must be byte-equivalent after any repair.

## Procedure

1. Inspect the canonical source skill before editing any exposure copy.
2. Inspect the harness-native exposure copy.
3. If the exposure copy diverges, repair the exposure copy from the canonical
   source skill.
4. Keep the skill self-contained. Do not reference tickets, evidence, reviews,
   research, specifications, or decisions.
5. Reference `.10x/knowledge/ledger-import-terms.md` only if shared vocabulary
   is needed.
6. Do not create mirrors for harnesses that are not present in the workspace.

## Validation

- The source skill exists at the required `.10x` path.
- The exposure copy exists at the required `.opencode` path.
- `cmp` or equivalent byte comparison shows the two files are equivalent.
- The skill contains no references to `.10x/tickets`, `.10x/evidence`,
  `.10x/reviews`, `.10x/research`, `.10x/specs`, or `.10x/decisions`.
