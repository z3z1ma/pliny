Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/specs/10x-autoresearch-loop.md, .10x/decisions/autoresearch-initial-implementation-defaults.md, .10x/decisions/superseded/autoresearch-initial-loop-deferrals.md

# Implement 10x Autoresearch Loop

## Scope

This parent ticket coordinates implementation of the active 10x autoresearch
specification. It exists because the work spans multiple independent closure
claims: static contracts, validators, offline scoring, MICRO execution, Codex
FULL integration, reporting, and first calibration evidence.

Included:

- Create reusable implementation assets under top-level `autoresearch/`.
- Keep durable conclusions and evidence in `.10x/`.
- Implement the loop in stages from static contracts to FULL harness runs.
- Preserve no-10x control isolation for harnesses that normally load
  `AGENTS.md`, `CLAUDE.md`, or equivalent files.
- Use standard-library-first tooling unless a child ticket records a concrete
  need for a dependency.

Excluded:

- Changing canonical 10x instruction text based on uncalibrated scores.
- Adding dashboard polish before score artifacts and record flow work.
- Integrating Claude Code, OpenCode, or oh-my-pi as FULL harnesses in the first
  implementation sequence.
- Learning score weights automatically.
- Granting non-human Trust Level 3 scorer approval.

## Child Tickets

- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md`
- `.10x/tickets/done/2026-06-23-autoresearch-contract-validator.md`
- `.10x/tickets/done/2026-06-23-autoresearch-offline-tracer.md`
- `.10x/tickets/done/2026-06-23-autoresearch-score-coverage.md`
- `.10x/tickets/2026-06-23-autoresearch-micro-runner.md`
- `.10x/tickets/done/2026-06-23-autoresearch-reporting.md`
- `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md`
- `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md`
- `.10x/tickets/done/2026-06-23-codex-home-isolation.md`
- `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md`

## Acceptance Criteria

- Every child ticket is closed, cancelled, or explicitly out of scope with reason.
- The active spec's acceptance criteria AC-001 through AC-015 are satisfied or
  explicitly deferred by a new decision/spec amendment.
- Evidence records support validator behavior, scoring behavior, no-10x control
  isolation, MICRO execution, and at least one Codex FULL harness run.
- A review record challenges the first calibration campaign before any canonical
  10x instruction change is proposed.
- Any discovered follow-up work is recorded in tickets instead of remaining only
  in chat or child-ticket notes.

## Progress And Notes

- 2026-06-23: Parent ticket opened after operator accepted initial harness,
  control, and budget defaults.
- 2026-06-23: Static contract child ticket completed with evidence at
  `.10x/evidence/2026-06-23-autoresearch-static-contracts.md`. Next child:
  `.10x/tickets/done/2026-06-23-autoresearch-contract-validator.md`.
- 2026-06-23: Contract validator child ticket completed with evidence at
  `.10x/evidence/2026-06-23-autoresearch-contract-validator.md`. Next child:
  `.10x/tickets/done/2026-06-23-autoresearch-offline-tracer.md`.
- 2026-06-23: Offline tracer child ticket completed with evidence at
  `.10x/evidence/2026-06-23-autoresearch-offline-tracer.md`. Next child:
  `.10x/tickets/done/2026-06-23-autoresearch-score-coverage.md`.
- 2026-06-23: Score coverage child ticket completed with evidence at
  `.10x/evidence/2026-06-23-autoresearch-score-coverage.md`. Next child tickets
  now unblocked: `.10x/tickets/2026-06-23-autoresearch-micro-runner.md` and
  `.10x/tickets/done/2026-06-23-autoresearch-reporting.md`.
- 2026-06-23: MICRO runner child ticket completed with evidence at
  `.10x/evidence/2026-06-23-autoresearch-micro-runner.md`. Next child tickets
  now unblocked: `.10x/tickets/done/2026-06-23-autoresearch-reporting.md` and
  `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md`.
- 2026-06-23: Reporting child ticket completed with evidence at
  `.10x/evidence/2026-06-23-autoresearch-reporting.md`. Remaining implementation
  children: `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md` and
  `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md`.
- 2026-06-23: Codex FULL dry-run/fixture-smoke harness child ticket completed
  with evidence at
  `.10x/evidence/2026-06-23-autoresearch-codex-full-harness.md`. Follow-up
  ticket `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md` opened because
  live Codex no-10x isolation is represented but not proven. Remaining children:
  `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md` and
  `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md`.
- 2026-06-23: Live Codex no-10x isolation smoke completed with evidence at
  `.10x/evidence/2026-06-23-codex-live-isolation-smoke.md`. Follow-up
  `.10x/tickets/done/2026-06-23-codex-home-isolation.md` opened because
  `--ignore-user-config` did not prevent CODEX_HOME plugin/skill loader
  warnings. Remaining children:
  `.10x/tickets/done/2026-06-23-codex-home-isolation.md` and
  `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md`.
- 2026-06-23: Codex home isolation child ticket completed with evidence at
  `.10x/evidence/2026-06-23-codex-home-isolation.md`. Remaining child:
  `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md`.
- 2026-06-23: First calibration campaign child ticket completed with evidence at
  `.10x/evidence/2026-06-23-first-autoresearch-calibration-campaign.md` and
  review at
  `.10x/reviews/2026-06-23-first-autoresearch-calibration-campaign.md`. Parent
  ticket status set to done. Promotion-grade requirements not satisfied by the
  first implementation are explicitly deferred by
  `.10x/decisions/superseded/autoresearch-initial-loop-deferrals.md` and tracked in
  follow-up tickets with `Parent: none`.

## Blockers

None.
