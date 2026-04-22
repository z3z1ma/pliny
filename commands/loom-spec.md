---
name: loom-spec
description: "Create or sharpen a durable behavior contract when intended behavior, constraints, or acceptance criteria are still too fuzzy for honest execution."
arguments: "<capability | workflow | ticket | behavior>"
category: support
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-specs
  - loom-research
  - loom-plans
  - loom-tickets
  - loom-critique
---

# /loom-spec

You are running **Loom Spec**.

Target behavior or scope:
`$ARGUMENTS`

This command is the explicit behavior-contract surface.
Use it when the project needs one stable statement of intended behavior before execution or critique can stay honest.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-specs`
- `loom-research`
- `loom-plans`
- `loom-tickets`
- `loom-critique`

## Goals

- define what the system should do, separate from how
- ground the contract in evidence, not wishful behavior
- make acceptance criteria and scenarios durable
- reconcile downstream tickets and critique with one contract

## Procedure

1. **Anchor the spec.**
   - Identify the governing initiative, plan, research, and tickets tied to `$ARGUMENTS`.
   - Determine whether a spec already exists and should be refined rather than replaced.

2. **Read the evidence and constraints.**
   - Pull from research, accepted critiques, existing tickets, and relevant implementation context.
   - Read enough to avoid writing a fantasy spec.

3. **Write or refine the spec.**
   - Make problem, desired behavior, constraints, scenarios, and acceptance explicit.
   - Keep the spec precise; do not collapse it into code-level trivia.
   - Name edge cases that matter.

4. **Reconcile downstream artifacts.**
   - If tickets or plans now conflict with the spec, fix the owner chain or note the required follow-up.
   - Make sure ticket acceptance criteria do not quietly diverge from the spec.

5. **Decide the next move.**
   - `/loom-plan` if sequencing still needs work.
   - `/loom-work` if the ticket is now ready.
   - `/loom-review` if the change was to an already-implemented behavior contract.

## Native tools to prefer

- `rg -n '<term>' .loom/{research,specs,plans,tickets,critique,wiki} --glob '*.md'`
- `git grep -n '<behavior term>'`
- `git diff --stat`
- `date -u +"%Y-%m-%dT%H:%M:%SZ"`

## Guardrails

- Do not let the ticket or wiki quietly become the spec.
- Do not encode wishful behavior that evidence or constitution contradicts.
- Do not overfit the contract to one incidental implementation.

## Required output

- spec record path and ID
- key behaviors, constraints, and acceptance expectations
- downstream artifacts updated or needing reconciliation
- recommended next command
