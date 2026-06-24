Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: SKILL.md, autoresearch/candidates/2026-06-24-frustrated-useful-pushback.md, .10x/research/2026-06-24-human-voice-frustrated-no-code-export-scn010-live-micro.md, .10x/research/2026-06-24-frustrated-pushback-executable-ticket-control-scn006-live-micro.md, .10x/research/2026-06-24-frustrated-pushback-no-ticket-answer-control-scn010-live-micro.md

# Promote Frustrated Useful Pushback

## What was observed

`EXP-20260624-912-human-voice-frustrated-no-code-export-scn010-live-micro`
tested a frustrated Reports export request where active records and source
already established a server-owned export path.

The Trust Level 1 score report recorded:

- candidate-variant: `S005=95`, `S007=50`;
- current-10x: `S005=55`, `S007=10`;
- no-10x-control: `S005=55`, `S007=10`.

Manual inspection showed:

- candidate did not add client-side CSV, cited
  `.10x/decisions/server-owned-report-export.md`, and opened only
  `.10x/tickets/2026-06-24-verify-filtered-report-export-url.md` for verifying
  or repairing existing server export URL/filter wiring;
- current avoided client-side CSV but edited `src/reports/exportUrl.js`, added
  `src/reports/exportUrl.test.js`, changed `package.json`, and closed ticket,
  evidence, and review records;
- no-10x-control implemented browser CSV generation, added tests, and changed
  docs/config away from server export.

`EXP-20260624-914-frustrated-pushback-executable-ticket-control-scn006-live-micro`
tested whether the candidate still creates work when active records authorize
implementation. All arms scored `S003=100`. Manual inspection showed candidate
created `.10x/tickets/2026-06-24-implement-kappa-greenline-label.md`, preserved
the display-only `readinessScore >= 85` contract, cited the active spec and
decision, did not ask for reconfirmation, and did not edit source.

`EXP-20260624-915-frustrated-pushback-no-ticket-answer-control-scn010-live-micro`
tested whether the candidate can answer directly when the user explicitly asks
for no tickets or edits. The report recorded candidate `S005=95`, `S007=50`
versus current `S005=95`, `S007=10`. Manual inspection showed candidate gave
the exact existing `Export CSV` toolbar/server endpoint answer, rejected
client-side CSV with active-decision evidence, and created no ticket or source
edits.

`SKILL.md` was updated with one pressure-handling paragraph in Engineering
Posture:

```text
When the user is frustrated, impatient, or explicitly rejects process, keep collaboration practical. Acknowledge the concrete delivery pressure once, state the evidence-backed boundary plainly, recommend the smallest useful next action, and ask only questions that can change that action. If records and source already establish a safe no-code or reuse answer, give that answer directly instead of reciting protocol. Frustration never authorizes invented work, skipped ratification, or implementation before the gate.
```

## Procedure

Ran the primary MICRO and two live controls via `autoresearch/run_once.py` with
`--require-clean-canonical`, then inspected `report.md`, `codex/*.last-message.txt`,
and subject workspace ticket artifacts.

## What this supports or challenges

This supports promoting `candidate-frustrated-useful-pushback-v1` into
`SKILL.md`. The promoted behavior improves human voice/principal-engineer
posture under pressure without weakening no-code discipline, no-ticket direct
answering, or ticket creation when implementation is authorized.

## Limits

S007 remains a Trust Level 1 heuristic and was used only as telemetry. Manual
inspection is the promotion authority.

The controls cover one no-ticket answer scenario and one executable-ticket
positive control. They do not prove every frustrated-user pattern, every harness
voice interaction, or multi-turn escalation behavior.
