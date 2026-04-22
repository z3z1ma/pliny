---
name: loom-codemap
description: "Map a repository or module into Loom wiki, research, and evidence without creating a new truth layer. Use when orientation cost is high, packet compilation keeps rediscovering structure, or path-local context adapters need safe source records."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: workflow
---

# loom-codemap

Codebase atlas work makes repository structure easier to recover.

It does not create a new canonical layer. Accepted structure belongs in wiki,
investigation belongs in research, and scan proof belongs in evidence.

## What This Skill Owns

- codebase map workflow
- module atlas workflow
- safe path-scoped context adapter guidance
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
3. scan structure with native tools
4. write research when discovery, uncertainty, or rejected interpretations matter
5. write evidence for scan commands, file lists, screenshots, or observations
6. write or update wiki pages for accepted structure
7. if generating path-local context adapters, make them point to Loom records only
8. record last verified date and source records on every atlas page

## Atlas Page Shape

Recommended sections:

- Summary
- Major Modules
- Important Entry Points
- Test Surface
- Build / Validation Commands
- Data / Persistence Boundaries
- Risky Areas
- Source Records
- Last Verified

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

## Done Means

- accepted structure is in wiki
- scan or inspection proof is in evidence when it matters
- uncertain interpretation is in research, not hidden in wiki
- generated path-local guidance points to owner records
- live execution state remains in tickets

## Read In This Order

Read immediately for atlas work:

1. `skills/loom-workspace/references/workspace-tree.md` when the repository
   structure or ownership boundary is not yet clear.

Then read conditionally:

2. `skills/loom-research/SKILL.md` when scan results include uncertainty,
   rejected interpretations, or null results.
3. `skills/loom-records/templates/evidence.md` when scan commands or observed
   structure should be preserved as proof.
4. `skills/loom-wiki/SKILL.md` when accepted structure should become a
   reusable atlas or module page.
