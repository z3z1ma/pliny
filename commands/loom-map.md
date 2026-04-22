---
name: loom-map
description: "Create or update a Loom codebase atlas using wiki, research, and evidence records without creating a new truth layer."
arguments: "<repository | module path | topic>"
category: support
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-codebase-atlas
  - loom-wiki
  - loom-research
---

# /loom-map

You are running **Loom Map**.

Map target:
`$ARGUMENTS`

This command creates orientation artifacts for a repository or module.
It does not create a new canonical layer.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-codebase-atlas`
- `loom-wiki`
- `loom-research`

## Goals

- reduce future orientation and packet-compilation cost
- preserve scan evidence when it matters
- promote accepted structure into wiki pages
- keep behavior, policy, and live execution in their owner layers

## Procedure

1. Confirm repository root and map scope.
2. Search existing wiki, research, specs, plans, and evidence for prior maps.
3. Inspect the codebase with native tools.
4. Record uncertain interpretation or rejected readings in research.
5. Record important scan commands or observations as evidence.
6. Create or update wiki atlas pages for accepted structure.
7. If path-local context adapters are requested, make them point to Loom owner
   records and state that they are not truth owners.

## Native Tools To Prefer

- `git rev-parse --show-toplevel`
- `find . -maxdepth 3 -type f | sort`
- `rg -n '<entry point or module name>'`
- `git grep -n '<term>'`
- `date -u +"%Y-%m-%dT%H:%M:%SZ"`

## Required Output

- atlas wiki pages created or updated
- research and evidence records created or updated, if any
- source records and last-verified date
- boundaries or risky areas discovered
- recommended next command
