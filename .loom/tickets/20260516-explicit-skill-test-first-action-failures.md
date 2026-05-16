# Explicit Skill Test First-Action Failures

ID: ticket:20260516-explicit-skill-test-first-action-failures
Type: Ticket
Status: closed
Created: 2026-05-16
Updated: 2026-05-16
Risk: medium - live OpenCode log parsing may be noisy, but the test currently tolerates a doctrine violation.
Priority: medium - operator approved trying the stricter test posture.

## Summary

Change explicit Loom skill request tests so non-skill tool invocation before the
first requested skill is a failure rather than a warning. The single closure claim
is that tests claiming first-action skill discipline fail when the transcript shows
premature non-skill tool use, while still passing or skipping honestly when the
requested skill is first or OpenCode is unavailable.

## Related Records

- `research:20260516-product-surface-scan` - identified the warning-vs-failure gap.
- `loom-core/skills/using-loom/references/01-activation-discipline.md` - owns first-action skill invocation doctrine.
- `knowledge:playbook-activation-tests-procedure` - related activation-test procedure for negative Playbook checks.
- `ticket:20260513-superpowers-style-activation-doctrine` - historical activation-test strengthening context.

## Scope

May change:

- `tests/explicit-skill-requests/run-test.sh`
- `tests/explicit-skill-requests/run-all.sh` only if needed for stricter failure behavior
- prompt fixtures only if the current fixtures cause unavoidable false positives unrelated to first-action behavior
- related docs or knowledge only if needed to explain the stricter test posture
- this ticket, evidence, and audit records as needed

Must not change:

- Core activation doctrine
- natural-prompt Playbook negative tests under `tests/skill-triggering/` except to note a blocker
- package entrypoints, Playbook command generation, or install docs
- test semantics that hide premature non-skill tool use by broadening allowed exceptions without evidence

Durable execution context for the first Ralph run: read this ticket,
`tests/explicit-skill-requests/run-test.sh`, and the activation discipline reference.
Treat log parsing changes as test behavior, not product doctrine. Stop if OpenCode
log shape prevents reliable detection and record the blocker instead of weakening
the check silently.

## Acceptance

- ACC-001: `tests/explicit-skill-requests/run-test.sh` exits nonzero when a
  non-skill tool invocation appears before the first skill tool call in a test that
  expects explicit skill activation.
  - Evidence: source inspection of the runner logic; if practical, a fixture or
    controlled log probe showing the failure path.
  - Audit: review should challenge whether the parser can still false-pass on
    premature tools.

- ACC-002: The runner still fails when no skill tool invocation is found or when the
  requested skill is not detected.
  - Evidence: source inspection and, if practical, existing test run output.
  - Audit: included in closure review if tests change materially.

- ACC-003: Allowed exceptions before the first skill call are either removed or
  justified narrowly in comments with evidence from OpenCode log shape; `todowrite`
  should not remain silently exempt if it represents a material non-skill tool
  action.
  - Evidence: source inspection of exception list and comments.
  - Audit: review should challenge whether exceptions undermine first-action
    discipline.

- ACC-004: Relevant checks pass or skip honestly.
  - Evidence: `bash tests/explicit-skill-requests/run-all.sh` when OpenCode is
    available, or recorded skip output when unavailable; `git diff --check` passes.
  - Audit: separate audit may be waived if this remains a narrow test-runner change,
    but residual live-harness log-shape risk should be explicit.

## Current State

Closed after narrow follow-up review. After resolving
`audit:20260516-product-surface-ticket-review#FIND-001` and the follow-up Ralph
review `FIND-002`. `run-test.sh` now factors log validation into
`validate_skill_log`, fails when no skill tool invocation is found, fails when any
non-skill tool-shaped log line appears before the first skill tool call, and
requires the first skill tool payload itself to match the requested `$SKILL_NAME`.
The wrong-skill-first/requested-skill-later fixture remains
`tests/explicit-skill-requests/wrong-skill-first-requested-later.jsonl`.

`run-all.sh` now treats the controlled parser probe as passing only when
`run-test.sh loom-audit --check-log wrong-skill-first-requested-later.jsonl` exits
with status `1` and output contains `FAIL: first skill tool invocation was not
'loom-audit'`. Exit `0`, exit `2`, missing fixture usage failures, or any other
nonzero failure output now fail the suite instead of satisfying the probe.

Validation run after the `FIND-002` fix:

- Targeted wrapper around `bash tests/explicit-skill-requests/run-test.sh loom-audit --check-log tests/explicit-skill-requests/wrong-skill-first-requested-later.jsonl` observed exit `1`, output containing `FAIL: first skill tool invocation was not 'loom-audit'`, and printed `PASS: intended wrong-skill-first parser failure observed`.
- `bash tests/explicit-skill-requests/run-all.sh` passed; the tightened parser probe failed the wrong-skill-first/requested-skill-later log for the intended reason, then all four live OpenCode explicit request cases passed with the requested skill triggered first.
- `git diff --check` passed with no output.

Final Ralph review `audit:20260516-explicit-skill-first-action-final-review` found
no material findings, marked `FIND-001` and follow-up `FIND-002` resolved, and
recommended closure. Residual risk remains that the parser is line-oriented around
the current OpenCode JSON log shape and raw live logs are not persisted; this is
accepted for this narrow test-runner ticket. No product doctrine changes were
needed.

## Journal

- 2026-05-16: Created ticket from operator disposition of `research:20260516-product-surface-scan` recommendation 4; operator approved trying the stricter failure posture.
- 2026-05-16: Set Status `active` before launching the first ticket-owned Ralph worker run.
- 2026-05-16: Updated `tests/explicit-skill-requests/run-test.sh` so premature non-skill tool invocation before the first skill tool call is a hard failure with log path output; removed the silent `todowrite` exemption.
- 2026-05-16: Ran `bash tests/explicit-skill-requests/run-all.sh`; all explicit skill request cases passed under OpenCode. Ran `git diff --check`; passed with no output. Set Status `review` for acceptance/audit review.
- 2026-05-16: Recorded validation dossier
  `evidence:20260516-product-surface-ticket-validation` and Ralph review
  `audit:20260516-product-surface-ticket-review`. Audit returned
  `changes-needed` for this ticket: `FIND-001` says the runner can false-pass when
  the wrong skill is first and the requested skill appears later. Set Status back
  to `active` for a bounded fix.
- 2026-05-16: Resolved `FIND-001` by requiring the first skill tool payload to
  match the requested `$SKILL_NAME`; missing skill tool calls and premature
  non-skill tools remain hard failures. Added
  `tests/explicit-skill-requests/wrong-skill-first-requested-later.jsonl` and a
  `run-all.sh` parser probe proving the wrong-skill-first/requested-skill-later
  shape fails. Ran the targeted parser probe, `bash tests/explicit-skill-requests/run-all.sh`,
  and `git diff --check`; all behaved as expected. Set Status `review` for a
  narrow follow-up review before closure.
- 2026-05-16: Resolved follow-up review `FIND-002` by tightening the `run-all.sh`
  controlled parser probe to require exit status `1` and the exact intended
  failure message `FAIL: first skill tool invocation was not 'loom-audit'`. Ran a
  targeted wrapper proving the intended wrong-skill-first failure, reran
  `bash tests/explicit-skill-requests/run-all.sh`, and reran `git diff --check`;
  all passed. Kept Status `review` for follow-up audit/acceptance instead of
  closing from the worker run.
- 2026-05-16: Recorded final Ralph review
  `audit:20260516-explicit-skill-first-action-final-review`; it found no material
  findings, confirmed `FIND-001` and follow-up `FIND-002` resolved, and judged the
  ticket closeable. Closed with ACC-001 through ACC-004 satisfied and parser
  log-shape risk recorded as residual.
- 2026-05-16: Retrospective identified a reusable prevention note: explicit skill
  parser probes should assert the intended failure reason, not merely any nonzero
  exit. Attempted knowledge promotion was blocked by current workspace permissions,
  which allow `.loom/tickets`, `.loom/evidence`, and `.loom/audit` edits but deny
  `.loom/knowledge` edits.
