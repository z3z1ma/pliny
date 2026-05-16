# Activation Scenarios Core-First Playbooks

ID: ticket:20260516-activation-scenarios-core-first-playbooks
Type: Ticket
Status: closed
Created: 2026-05-16
Updated: 2026-05-16
Risk: low - narrow fixture/documentation correction for activation scenario expectations.
Priority: high - removes stale guidance that contradicts current Playbook explicit-macro behavior.

## Summary

Update the activation eval scenarios so representative natural prompts expect Core
Loom routing or shaping, not implicit Playbook activation. The single closure claim
is that `evals/activation/loom-activation-scenarios.md` no longer teaches natural
prompts to auto-load Playbooks while preserving the failure signals around premature
implementation, ticket creation, worker launch, and unsupported closure.

## Related Records

- `research:20260516-product-surface-scan` - identified the stale activation scenario drift.
- `spec:playbook-explicit-macros` - defines Playbooks as explicit workflow macros rather than natural-prompt activation owners.
- `knowledge:playbook-activation-tests-procedure` - explains the negative activation-test posture for natural prompts.
- `CLAUDE.md` - contributor-facing acceptance guidance already expects Core-first natural routing.

## Scope

May change:

- `evals/activation/loom-activation-scenarios.md`
- nearby activation-eval wording only if it directly contradicts Core-first natural routing
- this ticket, evidence, and audit records as needed

Must not change:

- Playbook invocation mechanics
- Core activation doctrine
- package entrypoints, generated command files, or test runners
- unrelated eval fixtures outside the activation scenarios

Durable execution context for the first Ralph run: read this ticket, the related
records, and `evals/activation/loom-activation-scenarios.md`; write only the
activation scenario fixture and any required Loom execution records. Stop if the
fix appears to require changing Playbook invocation behavior rather than stale
fixture wording.

## Acceptance

- ACC-001: Scenario 1 no longer says `loom-idea-refine` is the likely route when
  Playbooks are installed; it expects Core routing/shaping and explicitly says
  Playbooks must not auto-load from the natural prompt.
  - Evidence: source inspection of Scenario 1 and targeted search for stale
    `loom-idea-refine` natural-prompt expectation in the activation scenario file.
  - Audit: separate audit is not required unless implementation changes more than
    the scenario fixture wording.

- ACC-002: Scenario 2 no longer says the agent should invoke
  `loom-debugging-and-error-recovery` merely because Playbooks are installed; it
  expects Core reproduction/evidence/ticket routing and allows a debugging Playbook
  only when explicitly invoked or recommended after Core routing.
  - Evidence: source inspection of Scenario 2 and targeted search for stale
    `loom-debugging-and-error-recovery` natural-prompt expectation.
  - Audit: separate audit is not required unless implementation changes more than
    the scenario fixture wording.

- ACC-003: Activation scenario wording remains consistent with the explicit
  Playbook macro contract and does not introduce a new universal harness claim.
  - Evidence: source inspection against `spec:playbook-explicit-macros` and
    `CLAUDE.md`; `git diff --check` passes.
  - Audit: separate audit would not add useful trust for this narrow docs fixture
    if the diff is limited to expectation wording.

## Current State

Closed. Ralph worker updated only `evals/activation/loom-activation-scenarios.md`
so Scenario 1 and Scenario 2 now expect Core Loom routing/shaping for natural
prompts and explicitly say Playbooks must not auto-load merely because Playbooks
are installed. Source inspection of both scenarios matched ACC-001 and ACC-002.
Targeted search found only the intended no-auto-load references to
`loom-idea-refine`, `loom-debugging-and-error-recovery`, and `With Playbooks
installed`; stale `likely workflow route`, `agent invokes
loom-debugging-and-error-recovery`, and `auto-trigger` wording was not found.
`git diff --check` passed with no output, recorded in
`evidence:20260516-product-surface-ticket-validation`. Ralph review
`audit:20260516-product-surface-ticket-review` found this ticket closeable with no
material findings. Residual risk is limited to the fixture nature of the change;
no live harness eval was run.

## Journal

- 2026-05-16: Created ticket from operator disposition of `research:20260516-product-surface-scan` recommendation 1.
- 2026-05-16: Set Status `active` before launching the first ticket-owned Ralph worker run.
- 2026-05-16: Ralph worker updated Scenario 1 and Scenario 2 activation fixture
  expectations to keep natural prompts in Core routing/shaping and reject
  Playbook autoactivation. Validation: source-inspected both scenarios, ran
  targeted stale-wording searches, and ran `git diff --check` successfully. Moved
  ticket to `review`; ready for closure if coordinator accepts the narrow diff.
- 2026-05-16: Recorded validation dossier
  `evidence:20260516-product-surface-ticket-validation` and Ralph review
  `audit:20260516-product-surface-ticket-review`; audit found this ticket
  closeable. Closed with ACC-001 through ACC-003 satisfied and no follow-up.
