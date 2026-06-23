Status: open
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/research/2026-06-23-skill-autoresearch-run.md
Depends-On:

# Increase Autoresearch Throughput

## Scope

Increase the rate of useful `SKILL.md` autoresearch experiments without adding a
run-loop controller or state-management layer.

Included:

- Define a simple operating pattern for preparing the next hypothesis while a
  live subject experiment is running.
- Prefer parallel MICRO experiments when hypotheses, scenarios, output roots,
  and candidate overlays are independent.
- Use subagents for bounded babysitting tasks when the task can be specified
  without judgment transfer: run a registered experiment, regenerate report,
  inspect required artifacts, and report exact paths/results.
- Preserve parent-agent ownership of promotion decisions, canonical `SKILL.md`
  edits, commits, pushes, and cross-record coherence.
- Identify whether any minimal harness/documentation changes are needed to make
  parallel execution safer.

Excluded:

- Reintroducing a persistent loop controller.
- Building a queue, scheduler, database, state machine, or experiment daemon.
- Delegating canonical `SKILL.md` promotion authority to subagents.
- Running overlapping experiments that write to the same output directory,
  candidate file, research record, or results ledger row.

## Acceptance Criteria

- AC-001: A written operating rule exists for concurrent hypothesis preparation
  and independent live MICRO execution.
- AC-002: Subagent babysitting instructions are documented with exact
  boundaries, required evidence, and forbidden authority.
- AC-003: Any code/docs changes are minimal and do not add a loop controller.
- AC-004: At least one subsequent research cycle uses the pattern or records why
  it was not applicable.
- AC-005: Parent-agent review still records evidence before any `SKILL.md`
  promotion.

## Progress and Notes

- 2026-06-23: Opened after operator recommended parallelizing experiments and
  hypotheses, preparing the next hypothesis while one experiment runs, and
  potentially using subagents to babysit bounded experiment completion.
- 2026-06-23: Spawned two read-only explorer subagents:
  - `Pauli`: inspect current `SKILL.md` and prior results, propose next
    high-value independent hypotheses.
  - `Leibniz`: inspect autoresearch harness/docs and propose minimal throughput
    improvements without loop-controller complexity.

## Blockers

None.
