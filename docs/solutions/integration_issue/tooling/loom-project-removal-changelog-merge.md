---
title: Removed LOOM_PROJECT.md; merged LOOM_CHANGELOG.md into ROADMAP.md
category: integration_issue
area: tooling
tags:
  - docs
  - compound
  - roadmap
  - changelog
  - drift
symptoms:
  - "Project direction is duplicated across multiple root docs"
  - "AI/agents reference different sources of truth"
  - "Roadmap and changelog drift or contradict"
---

# Removed LOOM_PROJECT.md; merged LOOM_CHANGELOG.md into ROADMAP.md

## Root cause

We had overlapping responsibilities across root documentation:

- `LOOM_PROJECT.md` acted as a constitution / always-on context.
- `.loom/compound/ROADMAP.md` described direction.
- `LOOM_CHANGELOG.md` tracked changes.

This created drift (the same idea maintained in multiple places) and made agent behavior nondeterministic when different prompts/tools pointed at different files.

## Solution steps

1) Choose a single source of truth for direction + history: `.loom/compound/ROADMAP.md`.

2) Migrate any durable "constitution" content from `LOOM_PROJECT.md` into one of:

- `AGENTS.md` (agent-facing invariants / always-on context), or
- the top of `.loom/compound/ROADMAP.md` (if it directly clarifies the roadmap).

3) Merge `LOOM_CHANGELOG.md` into `.loom/compound/ROADMAP.md` under a stable, greppable section header (for example: `## Changelog`).

4) Delete `LOOM_PROJECT.md` and stop referencing it.

5) Update internal pointers so every place that previously linked to either file now links to `.loom/compound/ROADMAP.md`:

- compound/plugin docs pointers
- `AGENTS.md` references (for example: "Constitution: …")
- `README.md` (and any templates/scaffolds)

## Why it works

- One file becomes the canonical "what" (roadmap) and "what changed" (changelog), reducing divergence.
- Agents see consistent context because prompts/tools converge on a single path.
- Search becomes simpler: one grep surface for direction + history.

## Prevention

- Add a lightweight contract check (test or CI) that asserts:
  - `LOOM_PROJECT.md` does not exist
  - `LOOM_CHANGELOG.md` does not exist
  - `.loom/compound/ROADMAP.md` contains `## Changelog`
  - `AGENTS.md` (and any templates) do not reference removed paths
- In new docs, link to `.loom/compound/ROADMAP.md` only (avoid introducing parallel "source of truth" files).

## References

- `AGENTS.md`
- `.loom/compound/ROADMAP.md`
- `LOOM_PROJECT.md` (removed)
- `LOOM_CHANGELOG.md` (merged)
