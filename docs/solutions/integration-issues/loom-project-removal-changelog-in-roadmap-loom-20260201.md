---
module: Loom
date: 2026-02-01
problem_type: integration_issue
component: tooling
symptoms:
  - "Compound system created and maintained LOOM_PROJECT.md + LOOM_CHANGELOG.md, splitting core context across multiple files"
  - "Changelog lived in a separate file, making direction/backlog and change history harder to reason about together"
  - "Installer/templates, plugin behavior, and docs/prompt constraints drifted (extra files kept reappearing)"
root_cause: incomplete_setup
resolution_type: tooling_addition
severity: medium
tags: [compound, opencode-plugin, installer, template-mirror, loom-roadmap, changelog]
---

# Troubleshooting: Remove LOOM_PROJECT.md and embed changelog in ROADMAP.md

## Problem
The compound integration maintained three separate “core docs” (`LOOM_PROJECT.md`, `LOOM_ROADMAP.md`, `LOOM_CHANGELOG.md`). That split the always-on context and memory deltas across multiple files and made the compound scaffolding harder to keep consistent.

We now keep direction + backlog + changelog in a single canonical file: `.loom/compound/ROADMAP.md`.

## Environment
- Module: Loom
- Affected Component: Compound tooling (OpenCode plugin + installer templates)
- Date: 2026-02-01

## Symptoms
- `ensureBootstrap()` created `LOOM_PROJECT.md` and `LOOM_CHANGELOG.md`, even though the durable “always-on” context is already in `AGENTS.md` (`compound:loom-core-context`).
- Changelog entries were appended to `LOOM_CHANGELOG.md`, so “direction/backlog” and “what changed” were not co-located.
- Multiple places referenced the old model (plugin text, autolearn prompt, installer, sync allowlist), causing drift.

## What Didn't Work

**Attempted solution:** Delete or stop reading `LOOM_PROJECT.md` / `LOOM_CHANGELOG.md` in only one layer (docs/templates or plugin).
- **Why it failed:** Another layer would reintroduce the old files (bootstrap) or keep committing them (sync allowlist) or still instruct the model to edit them (autolearn prompt).

## Solution

Make the “core docs” model explicit and consistent everywhere:

1) Only two canonical docs exist:
- `AGENTS.md`
- `.loom/compound/ROADMAP.md` (includes a managed changelog block)

2) Update the OpenCode compound plugin (and its packaged mirror) to:
- stop bootstrapping `LOOM_PROJECT.md` and `LOOM_CHANGELOG.md`
- stop syncing `LOOM_PROJECT.md`
- append changelog entries into `.loom/compound/ROADMAP.md` in a managed block (`compound:changelog-entries`)

```ts
// .opencode/plugins/compound_engineering.ts

// ensureBootstrap(): stop creating LOOM_PROJECT.md / LOOM_CHANGELOG.md
// roadmapSkeleton(): includes `<!-- BEGIN:compound:changelog-entries -->`
// appendChangelog(): writes to .loom/compound/ROADMAP.md (bounded + deduped)
```

3) Update the Python installer to only ensure fences in `.loom/compound/ROADMAP.md`:

```py
# src/agent_loom/compound/install.py

doc_specs = [
  (".loom/compound/ROADMAP.md", ["roadmap-backlog", "roadmap-ai-notes", "changelog-entries"]),
]
```

4) Update compound sync to stop committing removed docs:

```py
# src/agent_loom/compound/sync.py

pathspecs = [
  "AGENTS.md",
  ".loom/compound/ROADMAP.md",
  ".opencode/agents",
  ".opencode/memory",
  ".opencode/skills",
  ".claude/agents",
  ".claude/skills",
]
```

5) Update prompts/docs/skills to match the new model:
- `.opencode/compound/prompts/autolearn.md` (and mirror)
- `src/agent_loom/compound/opencode/README.md`

6) Update tests to lock the new contract:
- `tests/test_compound_install.py` asserts:
  - installer creates `.loom/compound/ROADMAP.md`
  - installer does NOT create `LOOM_PROJECT.md` / `LOOM_CHANGELOG.md`
  - `.loom/compound/ROADMAP.md` contains `compound:changelog-entries`

7) (Repo) Move existing changelog entries into `.loom/compound/ROADMAP.md` and delete old root docs:
- delete `LOOM_PROJECT.md`
- delete `LOOM_CHANGELOG.md`

## Why This Works
- One canonical place for always-on context (`AGENTS.md`) and one canonical place for direction + deltas (`.loom/compound/ROADMAP.md`) reduces drift.
- The plugin, installer template, sync allowlist, and autolearn constraints now agree on the same file surface.
- The changelog append logic remains bounded and deduped, but now lives where agents also read direction/backlog.

## Prevention
- Treat the compound scaffold as a contract:
  - keep `.opencode/plugins/compound_engineering.ts` mirrored with `src/agent_loom/compound/opencode/.opencode/plugins/compound_engineering.ts`
  - keep `.opencode/compound/prompts/autolearn.md` mirrored with `src/agent_loom/compound/opencode/.opencode/compound/prompts/autolearn.md`
- Add a “forbidden references” test (or CI grep) to ensure no scaffold files mention `LOOM_PROJECT.md` or `LOOM_CHANGELOG.md`.
- Add/keep contract tests ensuring `.loom/compound/ROADMAP.md` contains `changelog-entries` fences after install.

## Related Issues
No related issues documented yet.

## References
- `.opencode/plugins/compound_engineering.ts`
- `src/agent_loom/compound/opencode/.opencode/plugins/compound_engineering.ts`
- `src/agent_loom/compound/install.py`
- `src/agent_loom/compound/sync.py`
- `src/agent_loom/compound/opencode/.loom/compound/ROADMAP.md`
- `tests/test_compound_install.py`
