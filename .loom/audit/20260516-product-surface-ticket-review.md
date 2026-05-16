# Product Surface Follow-up Ticket Review

ID: audit:20260516-product-surface-ticket-review
Type: Audit
Status: recorded
Created: 2026-05-16
Updated: 2026-05-16
Audited: 2026-05-16
Target: ticket:20260516-product-surface-followups

## Summary

A bounded Ralph review challenged the four product-surface follow-up tickets, their
diffs, and validation evidence before closure. The review found the activation
fixture, command-description, and install-safety tickets closeable, but identified
one material gap in the explicit-skill request test hardening ticket.

## Target

The audit target was the closure readiness of these tickets and their current
worktree changes:

- `ticket:20260516-activation-scenarios-core-first-playbooks`
- `ticket:20260516-playbook-command-descriptions-source`
- `ticket:20260516-generic-playbook-install-safety`
- `ticket:20260516-explicit-skill-test-first-action-failures`

The reviewed file set included activation scenarios, Playbook command generation
and generated TOML, install docs, Playbook README wording, and the explicit skill
request runner.

## Audit Scope And Lenses

The Ralph review inspected ticket acceptance, changed source/docs/tests, current
diff context, and `evidence:20260516-product-surface-ticket-validation`.

Lenses used:

- claim and evidence exactness
- ticket acceptance satisfaction
- scope and surface boundary
- generated-file and tooling drift
- docs safety around explicit-only Playbook setup
- explicit-skill test parser false-pass risk and failure-path coverage

Out of scope: proving behavior in every third-party harness, re-running package
checks beyond the existing evidence, and reviewing unrelated worktree changes or
older Playbook explicit-macro tickets.

## Context And Evidence Reviewed

- Ralph review run: bounded review launched from the four target tickets, related
  records, evidence dossier, and changed file set; returned `changes-needed` with
  one material finding.
- `evidence:20260516-product-surface-ticket-validation` - package checks, generated
  description comparison, targeted searches, explicit skill request suite, and
  `git diff --check` observations.
- `spec:playbook-explicit-macros` - expected Core-first natural routing and source
  description behavior for generated Playbook command metadata.
- `research:20260516-product-surface-scan` - source of the four follow-up tickets.
- `evals/activation/loom-activation-scenarios.md` - activation fixture wording.
- `loom-playbooks/loom-playbooks.mjs` and `loom-playbooks/commands/*.toml` - command
  description generation and generated metadata.
- `INSTALL.md` and `loom-playbooks/README.md` - generic/fallback install safety
  wording.
- `tests/explicit-skill-requests/run-test.sh` - first-action explicit skill request
  runner logic.

## Findings

### FIND-001: Explicit Skill Runner Can Pass When The Wrong Skill Is First

The reviewer found that `tests/explicit-skill-requests/run-test.sh` identifies the
first skill tool call as the first occurrence of any skill tool, then separately
checks whether the requested skill appears anywhere later in the log. A transcript
that invokes `loom-tickets` first and only later invokes the requested `loom-audit`
skill could pass if no non-skill tool appears before the first skill.

This challenges `ticket:20260516-explicit-skill-test-first-action-failures`, whose
summary says the tests should pass when the requested skill is first and fail on
premature action before the first requested skill. The ticket should either make
the first skill tool call payload match the requested `$SKILL_NAME`, or explicitly
narrow the closure claim to “any Loom skill first, requested skill eventually
appears” if that is the intended behavior.

## Verdict

`changes-needed` for the combined target because `FIND-001` blocks closure of
`ticket:20260516-explicit-skill-test-first-action-failures`.

Within the reviewed scope, the other three tickets are closure-ready:

- `ticket:20260516-activation-scenarios-core-first-playbooks` - closeable.
- `ticket:20260516-playbook-command-descriptions-source` - closeable.
- `ticket:20260516-generic-playbook-install-safety` - closeable.

The audit verdict is not ticket closure; each ticket must still disposition this
audit in its own state.

## Required Follow-up

- Fix or disposition `FIND-001` in `ticket:20260516-explicit-skill-test-first-action-failures` before closing that ticket.
- Prefer a controlled parser probe or fixture log for the “wrong skill first,
  requested skill later” shape so the failure branch is proven instead of only
  source-inspected.

## Residual Risk

- Evidence for live OpenCode behavior is summarized in the dossier, not backed by
  persisted raw logs.
- Generic Playbook install safety depends on third-party harness behavior; docs now
  qualify raw exposure, but this audit does not prove external harness semantics.
- After `FIND-001` is fixed, the explicit skill runner should be reviewed again
  narrowly for parser false-pass risk.

## Related Records

- `evidence:20260516-product-surface-ticket-validation` - validation dossier.
- `ticket:20260516-activation-scenarios-core-first-playbooks` - closeable per audit.
- `ticket:20260516-playbook-command-descriptions-source` - closeable per audit.
- `ticket:20260516-generic-playbook-install-safety` - closeable per audit.
- `ticket:20260516-explicit-skill-test-first-action-failures` - blocked by `FIND-001` until fixed or dispositioned.
