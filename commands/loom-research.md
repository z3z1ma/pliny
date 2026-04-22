---
name: loom-research
description: "Create or refine a durable investigation when evidence, comparison, or discovery is needed before commitment."
arguments: "<question | tradeoff | topic | decision>"
category: support
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-research
  - loom-initiatives
  - loom-plans
  - loom-specs
  - loom-wiki
---

# /loom-research

You are running **Loom Research**.

Research question or topic:
`$ARGUMENTS`

This command creates durable discovery.
Use it when the project needs evidence before committing to a behavior, strategy, or implementation path.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-research`
- `loom-initiatives`
- `loom-plans`
- `loom-specs`
- `loom-wiki`

## Goals

- frame the investigation clearly
- recall prior evidence before inventing new investigation
- gather and synthesize evidence, separating it from inference
- capture rejected options and null results so future agents inherit the dead ends
- route the result to the correct downstream owner

## Procedure

1. **Anchor the question.**
   - Determine what decision, uncertainty, or tradeoff `$ARGUMENTS` refers to.
   - Link the research to any relevant initiative, plan, spec, or ticket.

2. **Read what already exists.**
   - Search prior research, accepted wiki pages, decision records, specs, ticket journals, and evidence records.
   - Reuse prior investigation where it remains valid.

3. **Gather evidence.**
   - Use repository evidence, experiments, or external sources as appropriate.
   - If current outside facts matter and the harness can browse, gather and cite those sources.
   - Keep raw evidence separate from conclusions.

4. **Write the research record.**
   - Cover question, why it matters, method, sources, evidence, rejected options, null results, conclusions, recommendations, and open questions.
   - Make conclusions proportional to the evidence.

5. **Route the result.**
   - Behavior clarified → spec.
   - Sequencing changed → plan.
   - Accepted explanation → wiki.
   - Durable direction changed → initiative or constitution, often via `/loom-decide`.

## Native tools to prefer

- `rg -n '<term>' .loom/{research,specs,plans,tickets,wiki,evidence} --glob '*.md'`
- `find .loom/{research,evidence,wiki} -type f -name '*.md' | sort`
- `git grep -n '<term>'`
- inline Python only when it is materially clearer than shell for local synthesis

## Guardrails

- Do not present speculation as settled evidence.
- Do not let research become the behavior contract if a spec should own that truth.
- Do not bury the downstream recommendation.
- Do not discard rejected options or null results; they are durable.

## Required output

- research record path and ID
- key conclusions and confidence
- rejected options or null results captured, if any
- downstream implications
- recommended next command
