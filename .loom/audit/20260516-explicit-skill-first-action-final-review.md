# Explicit Skill First-Action Final Review

ID: audit:20260516-explicit-skill-first-action-final-review
Type: Audit
Status: recorded
Created: 2026-05-16
Updated: 2026-05-16
Audited: 2026-05-16
Target: ticket:20260516-explicit-skill-test-first-action-failures

## Summary

A bounded Ralph final review rechecked the explicit skill request runner after the
prior audit finding and a follow-up parser-probe finding were fixed. The review
found no material findings and judged the ticket closeable within the reviewed
scope.

## Target

The target was `ticket:20260516-explicit-skill-test-first-action-failures` and the
current changes to:

- `tests/explicit-skill-requests/run-test.sh`
- `tests/explicit-skill-requests/run-all.sh`
- `tests/explicit-skill-requests/wrong-skill-first-requested-later.jsonl`

The review specifically challenged whether prior
`audit:20260516-product-surface-ticket-review#FIND-001` was resolved and whether
the follow-up Ralph review concern about accepting arbitrary nonzero probe failures
was also resolved.

## Audit Scope And Lenses

The Ralph review inspected the target ticket, prior audit, evidence dossier, the
three changed test files, and current scoped diff/status. It also reran/inspected
the controlled parser probe result: exit status `1` with the intended failure
message present.

Lenses used:

- parser false-pass risk
- evidence exactness for the controlled probe
- ACC-001 through ACC-004 satisfaction
- scope boundary and residual risk

Out of scope: proving future OpenCode log formats, preserving raw `/tmp` logs, and
adding additional synthetic fixtures for every failure branch.

## Context And Evidence Reviewed

- Ralph review run: final explicit-skill runner review launched from the target
  ticket, prior audit, evidence dossier, changed files, and current diff/status.
- `audit:20260516-product-surface-ticket-review#FIND-001` - prior finding that a
  wrong first skill followed by the requested skill could pass.
- `evidence:20260516-product-surface-ticket-validation` - includes the targeted
  wrong-skill-first parser probe, tightened `run-all.sh` behavior, passing explicit
  skill request suite, and `git diff --check` observations.
- `tests/explicit-skill-requests/run-test.sh` - first skill payload is validated
  against `$SKILL_NAME`; no-skill and wrong/missing requested skill are failures.
- `tests/explicit-skill-requests/run-all.sh` - parser probe requires exit status
  `1` and the exact intended failure message.
- `tests/explicit-skill-requests/wrong-skill-first-requested-later.jsonl` - fixture
  with `loom-tickets` first and requested `loom-audit` later.

## Findings

None - no material findings within audited scope.

Prior finding disposition:

- `audit:20260516-product-surface-ticket-review#FIND-001` is resolved. The runner
  now validates the first skill payload itself, so wrong-skill-first/requested-later
  no longer passes merely because the requested skill appears somewhere in the log.
- Follow-up review concern `FIND-002` is resolved. `run-all.sh` no longer accepts
  arbitrary nonzero probe failure as success; it rejects exit `0`, non-`1` exits,
  and exit `1` without `FAIL: first skill tool invocation was not 'loom-audit'`.

## Verdict

`clear` within the reviewed scope. ACC-001 through ACC-004 are supported by source
inspection and evidence, and the ticket is closeable if the ticket owner accepts
the residual parser/log-shape limitations.

## Required Follow-up

None before closure for the reviewed scope.

## Residual Risk

- The parser remains line-oriented around the current OpenCode JSON log shape.
- The evidence dossier summarizes live harness logs rather than preserving raw logs.
- No separate fixture evidence was added for no-skill or non-skill-before-skill
  branches, but the final Ralph review judged source inspection sufficient for this
  narrow ticket.

## Related Records

- `ticket:20260516-explicit-skill-test-first-action-failures` - consuming ticket.
- `audit:20260516-product-surface-ticket-review` - prior combined closure review.
- `evidence:20260516-product-surface-ticket-validation` - validation dossier.
