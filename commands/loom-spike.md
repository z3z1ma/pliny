---
name: loom-spike
description: "Run a bounded Loom spike as a research variant with experiment matrix, throwaway scope, evidence, conclusions, null results, and downstream route."
arguments: "<question | experiment | uncertainty>"
category: support
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-spike
  - loom-research
  - loom-wiki
  - loom-specs
---

# /loom-spike

You are running **Loom Spike**.

Spike question:
`$ARGUMENTS`

The spike route is:

`question -> experiment matrix -> bounded throwaway write_scope -> evidence -> conclusions/null results -> downstream route`

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-spike`
- `loom-research`
- `loom-wiki`
- `loom-specs`

## Goals

- answer a bounded technical or product question
- keep throwaway work clearly scoped
- preserve evidence, rejected paths, and null results
- route accepted conclusions to the right owner layer

## Procedure

1. Frame the question and success criteria.
2. Search prior research, evidence, specs, and wiki pages.
3. Define the experiment matrix and throwaway write scope.
4. Run only the smallest useful experiment.
5. Capture evidence and observations.
6. Record conclusions, null results, and rejected paths in research.
7. Route behavior to spec, explanation to wiki, and execution to tickets.

## Guardrails

- Do not let throwaway code become production by accident.
- Do not overstate weak evidence.
- Do not skip null results; they are often the most reusable output.

## Required Output

- research record path and ID
- evidence records or artifacts
- conclusion and confidence
- null results or rejected paths
- downstream owner recommendation
