# Mill Inter-Iteration Summary

ID: ticket:20260525-mill-iteration-summary
Type: Ticket
Status: closed
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - lightweight model call or deterministic summarizer; no durable record writes without explicit promotion.
Depends On: ticket:20260525-mill-workstation-engine, ticket:20260525-mill-pipeline-ui

## Summary

After a subprocess exits or an iteration boundary is detected, Mill runs a summarization pass and surfaces it in the dashboard. The summary tells the operator what appears to have changed this iteration: files modified, records updated, tests run, commands executed. Labeled as visibility output, not evidence or acceptance proof.

## Related Records

- `plan:20260525-factory-floor-mvp` - parent plan, Unit 8.
- `spec:loom-mill-factory-floor-mvp` REQ-008 - inter-iteration summary requirement.
- `research:20260524-loom-mill-software-factory` Finding 6 - inter-iteration processes table.

## Scope

Read scope:
- Workstation state and subprocess output from Unit 5.
- Git diff/log since iteration start.
- Record state changes detected by watcher (Unit 3).

Write scope:
- `loom-mill/src/loom_mill/processes/summarize.py` (or similar) - summarization logic.
- `loom-mill/frontend/src/` - summary display component in dashboard.
- `.mill/summaries/` - ephemeral summary storage (not in `.loom/`).

Non-goals:
- No automatic evidence or knowledge record creation. Summaries are visibility only unless the operator explicitly promotes them.
- No complex NLP or embedding. A deterministic diff/change summary is acceptable for MVP; model-generated summary is a stretch goal.
- No backpressure analysis (Unit 9).

Stop conditions:
- Stop if iteration boundary detection is ambiguous for a given harness (route to harness-specific research).

## Acceptance

- ACC-001: After a subprocess exits, Mill produces a summary containing: files changed (count + paths), records changed (IDs + what field changed), and subprocess exit status.
  Evidence: integration test with a configured command that modifies files; summary contains correct change list.

- ACC-002: Summary is displayed in the Factory Floor dashboard associated with the relevant workstation/iteration.
  Evidence: screenshot or Playwright snapshot showing summary panel after a completed iteration.

- ACC-003: Summary is clearly labeled as "iteration summary" / visibility output, not as evidence, audit, or acceptance.
  Evidence: UI shows distinct styling/label; summary storage is in `.mill/`, not `.loom/`.

## Current State

Not started. Blocked on workstation engine (Unit 5) and pipeline UI (Unit 4).

## Journal

- 2026-05-25: Created from `plan:20260525-factory-floor-mvp` Unit 8.
