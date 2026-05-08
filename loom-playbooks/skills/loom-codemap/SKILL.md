---
name: loom-codemap
description: "Map repository or module structure. Use when unfamiliar code, architecture, ownership, call paths, module boundaries, or repeated packet context discovery needs an accepted atlas, research note, or evidence-backed map."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-codemap

Codebase atlas work makes repository structure easier to recover.

It routes accepted structure into wiki, investigation into research, and scan
observations into evidence.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- codebase map workflow
- module atlas workflow
- safe path-scoped context adapter guidance
- source/version and documentation conflict surfacing
- edit-oriented context packing for future tickets or packets
- routing scan results into wiki, research, and evidence

## Use This Skill When

- future packet compilation keeps rediscovering the same repository structure
- a large codebase needs an accepted orientation page
- a module boundary needs a durable explanation
- path-local instruction files should point at Loom records without owning truth

## Do Not Use This Skill When

- the question is one small implementation detail
- the intended behavior belongs in a spec
- live work state belongs in a ticket
- the requested output would define policy in a wiki page

## Default Procedure

1. confirm the repository root and scope
2. inspect existing wiki, research, evidence, specs, and plans for prior maps
3. collect deterministic structure before synthesis: manifests, package files,
   build/test/CI entry points, source roots, tests, docs, recent commits, and
   relevant ownership or hotspot signals when the scope warrants it
4. for edit-oriented orientation, read the target files, related tests, one nearby
   example of the pattern to follow, and shared interfaces or types before
   recommending an implementation route
5. scan structure with native tools
6. when dependency versions, official docs, project examples, or accepted owner
   records disagree, preserve the conflict in research/spec/ticket instead of
   silently choosing the convenient source
7. note architectural friction when mapping a module: shallow wrappers, unclear
   seams, missing test surfaces, coupling that spreads one concept across many
   files, or repeated path rediscovery by packets
8. write research when discovery, uncertainty, or rejected interpretations matter
9. write evidence for scan commands, file lists, screenshots, or observations
10. write or update wiki pages for accepted structure
11. if generating path-local context adapters, make them point to Loom records only
12. record last verified date and source records on every atlas page

Do not synthesize from a file-tree glance alone when the map will guide future
execution. Deterministic collection keeps the atlas from becoming a confident but
stale story about the wrong files.

## Source Conflict Rule

When a map or context pack depends on framework, library, platform, external API,
or generated behavior, identify the relevant version or source state before
synthesis. Prefer current project code and accepted owner records for project
truth; use official docs or source examples for external behavior. If docs,
current code, generated files, and owner records disagree, route the conflict to
research, spec, ticket, or critique instead of choosing silently.

For packet or ticket preparation, a useful context pack is not every related file.
It is the smallest set that lets a fresh worker see the target files, nearby
pattern, relevant tests, shared interfaces, owner records, and known conflicts.

## Atlas Page Shape

Atlas page shape is owned by `loom-wiki`.

When accepted repository or module structure should persist, write or update a
wiki atlas page using the core `loom-wiki` page-types reference and atlas-page
template. This codemap workflow owns the mapping route: scan structure, preserve
observations in evidence when useful, route uncertainty or rejected
interpretations to research, and promote accepted structure into the wiki-owned
atlas shape.

## Context Adapter Rule

Path-local instruction files may improve retrieval. They may not define
independent project truth.

Safe adapter shape:

```md
# <Path> Context

This file is a context adapter, not a truth owner.

Read:
- wiki:<module-page>
- spec:<behavior-contract>
- decision:<decision-id>
- plan:<plan-id>
```

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "A file tree dump is a code map." | A useful atlas explains structure, boundaries, and retrieval paths, with evidence when needed. |
| "I can infer architecture from names." | First collect manifests, tests, docs, source roots, and current code paths; then synthesize. |
| "I know this framework pattern from memory." | Detect project versions and inspect official docs or project examples when correctness depends on current framework behavior. |
| "Uncertain interpretation can go straight into wiki." | Uncertainty belongs in research until accepted. Wiki explains settled structure. |
| "Path-local instructions can teach local truth." | Path adapters may point to Loom owners; they do not own independent truth. |
| "Structure is obvious, so no evidence is needed." | If the map will be reused, preserve enough scan/source context to know when it must be rechecked. |
| "Official docs always beat local code." | Docs explain external behavior; local code and owner records still define project implementation reality and intended behavior. |
| "More files make a better context pack." | Context packs should include the smallest relevant source set plus conflicts and owner records, not a transcript dump. |

## Red Flags

- atlas page lacks source records, last-verified date, or scope boundary
- atlas page was written from a file list without checking build/test/docs/source
  entry points relevant to the scope
- wiki page mixes accepted structure with unresolved investigation
- generated adapter gives imperative instructions beyond owner-record pointers
- map ignores repository boundaries or nested workspaces
- repeated packet compilation still rediscovers paths after the codemap pass
- source, docs, generated files, or owner records conflict without a routed disposition
- context pack omits the nearby pattern, tests, or shared interface that would prevent guessing

## Verification

- [ ] Repository scope and map boundary are explicit.
- [ ] Accepted structure is in wiki; uncertainty and rejected interpretations are in research.
- [ ] Scan observations or file lists are evidence when the map depends on them.
- [ ] Source/version conflicts are routed instead of silently resolved.
- [ ] Edit-oriented context packs include target files, nearby patterns, tests, interfaces, and owner records.
- [ ] Path-local adapters, if created, point to owner records and do not own truth.

## Done Means

- accepted structure is in wiki
- scan or inspection artifacts are in evidence when they matter
- uncertain interpretation is in research, not hidden in wiki
- generated path-local guidance points to owner records
- live execution state remains in tickets

## Read In This Order

Read immediately for atlas work:

1. the core `loom-workspace` workspace-tree reference when the repository
   structure or ownership boundary is not yet clear.

Then read conditionally:

2. the core `loom-research` skill when scan results include uncertainty,
   rejected interpretations, or null results.
3. `skills/loom-source-grounding/SKILL.md` when external docs, dependency versions,
   or framework/source behavior constrain the map.
4. `skills/loom-context-engineering/SKILL.md` when the codemap result should become
   a task-specific context pack or handoff.
5. the core `loom-evidence` skill when scan commands or observed structure should
   be preserved as evidence.
6. the core `loom-wiki` skill when accepted structure should become a reusable
   atlas or module page.
