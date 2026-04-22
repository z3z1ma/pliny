---
name: loom-map
description: "Create or update a Loom codebase atlas using wiki, research, and evidence records without creating a new truth layer."
arguments: "<repository | module path | topic>"
category: support
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-codemap
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
- `loom-codemap`
- `loom-wiki`
- `loom-research`

## Goals

- reduce future orientation and packet-compilation cost
- preserve scan evidence when it matters
- promote accepted structure into wiki pages
- keep behavior, policy, and live execution in their owner layers

## Canonical Procedure

Use `skills/loom-codemap/SKILL.md` as the procedure.

In short:

1. confirm repository root and map scope
2. inspect existing atlas/wiki/research/evidence
3. scan structure with native tools
4. route uncertainty to research and proof to evidence
5. update wiki for accepted structure
6. keep path-local adapters as pointers to owner records

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
