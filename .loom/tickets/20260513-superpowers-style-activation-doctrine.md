# Superpowers-Style Activation Doctrine

ID: ticket:20260513-superpowers-style-activation-doctrine
Type: Ticket
Status: closed
Created: 2026-05-13
Updated: 2026-05-14
Risk: medium - changes Core session-entry doctrine and package-visible activation guidance, but remains prose/static-check work.

## Summary

Implement the activation lessons from `research:20260513-superpowers-skill-activation` in Loom's shipped surfaces. The closure claim is that Core now uses the Superpowers-style OpenCode bootstrap path, teaches near-explicit Superpowers activation language, preserves anti-rationalization pressure, and ships tests that check actual skill invocation.

## Related Records

- `research:20260513-superpowers-skill-activation` - source investigation and recommendations this ticket implements.
- `research:20260510-loom-loop-failure-analysis` - prior analysis of premature execution and worker-handoff bypasses.
- `ticket:20260513-mandatory-shaping-doctrine` - recent closed ticket strengthening ambiguity shaping doctrine.
- `loom-core/skills/using-loom/SKILL.md` - owns session-entry doctrine and activation posture.
- `loom-core/loom-core.mjs` - owns OpenCode preload and smoke inspection behavior.

## Scope

May change:

- Core `using-loom` skill and ordered references.
- Core OpenCode bootstrap mechanics, package smoke output, and package scripts when needed for activation checks.
- Existing Core preload surfaces for Claude/Cursor/Gemini when needed to add the new ordered activation reference without changing their transport mechanics.
- Human-facing docs that restate bootstrap or activation behavior.
- Test fixtures and scripts that validate skill-triggering behavior.
- This ticket, new evidence, and the completed research record.

Must not change:

- Non-OpenCode adapter transport mechanics beyond adding the new ordered activation reference to existing Core preload surfaces.
- Playbook behavior beyond documentation that reinforces Core routing.
- Historical `.loom` records except this ticket, the linked research created for this work, and new evidence.
- Runtime assumptions such as daemons, databases, dashboards, CLIs, or helper-script requirements.

## Acceptance

- ACC-001: OpenCode Core registers `loom-core/skills` through `config.skills.paths` and injects stripped `using-loom` doctrine plus ordered references into the first user message through `experimental.chat.messages.transform`, with duplicate-injection protection and no `config.instructions` bootstrap.
  - Evidence: source inspection plus Core smoke output showing `instructionCount: 0`, `doesNotUseConfigInstructionsForBootstrap: true`, `bootstrapInjectionPartCount: 1`, and `bootstrapInjectionIsDeduped: true`.
  - Audit: command and source evidence are sufficient for this adapter-mechanics criterion.

- ACC-002: `using-loom` and its activation reference include the exact Superpowers-style enforcement language: `If you think there is even a 1% chance a skill might apply, you ABSOLUTELY MUST invoke the skill.` and `IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.`
  - Evidence: source inspection plus targeted scan for the exact enforcement phrases.
  - Audit: separate audit is not required for this text criterion if the phrases are present in model-visible Core doctrine.

- ACC-003: Skill invocation is explicitly required before clarifying questions, code exploration, quick checks, edits, ticket creation, Ralph launches, evidence claims, audit claims, or closure.
  - Evidence: source inspection plus targeted scan for first-action language in `using-loom`, `activation-discipline.md`, and the OpenCode bootstrap string.
  - Audit: separate audit is not required for this text/static-check criterion.

- ACC-004: `using-loom` includes a red-flags table naming common rationalizations like `this is simple`, `I need more context first`, `I need to inspect first`, `I'll create the ticket after`, `I'll ask the worker directly`, `evidence can wait`, `audit is overkill`, and `I'll just do this one thing first`.
  - Evidence: source inspection plus targeted scan for the named rationalizations.
  - Audit: separate audit is not required for this text/static-check criterion.

- ACC-005: Core and Playbooks skill descriptions remain trigger-focused enough that static smoke checks fail on descriptions outside the accepted activation prefixes.
  - Evidence: Core smoke, Playbooks smoke, and targeted description scans.
  - Audit: command evidence is sufficient for this static assertion claim.

- ACC-006: Activation tests modeled on Superpowers exist and pass for natural prompts and explicit skill requests: natural prompts look for skill tool calls, explicit requests warn if non-skill tools run before the first skill call, and root package scripts expose both suites.
  - Evidence: source inspection of `tests/skill-triggering/**`, `tests/explicit-skill-requests/**`, and live `npm run test:skill-triggering` plus `npm run test:explicit-skill-requests` output.
  - Audit: live OpenCode integration output is sufficient for this test-existence and pass/fail criterion.

- ACC-007: `CLAUDE.md` includes a harness integration acceptance test requiring `Let's make a react todo list` to auto-trigger `using-loom` and route to `loom-idea-refine` before code is written.
  - Evidence: source inspection of `CLAUDE.md` plus live `loom-idea-refine` activation test output.
  - Audit: separate audit is not required for this human-facing acceptance text criterion.

## Evidence

- `evidence:20260513-superpowers-style-activation-checks` - source scans, Core smoke, Playbooks smoke, package dry-runs, and diff check supporting the acceptance criteria.

## Current State

Closed. OpenCode Core now registers `loom-core/skills` through `config.skills.paths` and injects stripped `using-loom` doctrine plus ordered references into the first user message with `experimental.chat.messages.transform`. Core `using-loom` now includes the exact 1% and no-choice Superpowers-style enforcement language, first-action ordering before clarifying questions/code exploration/quick checks, and a red-flags table with the requested rationalizations. Core descriptions were tuned to trigger-oriented phrasing, smoke checks enforce activation and description posture outside the model-visible skill prose, Superpowers-style activation scripts exist and pass live OpenCode runs, and `CLAUDE.md` records the `Let's make a react todo list` harness acceptance test adapted to `loom-idea-refine`.

Evidence `evidence:20260513-superpowers-style-activation-checks` supports the acceptance criteria. Separate audit was not performed because the criteria are adapter/static-text/test-output claims with direct command evidence.

## Journal

- 2026-05-13: Created ticket from operator instruction to implement as much of the Superpowers activation research as possible, including the recommendations and the directly transferable findings.
- 2026-05-13: Added activation doctrine, red flags, trigger-description checks, doc alignment, and natural-prompt activation scenarios. Core and Playbooks smoke checks pass after the activation assertions were added.
- 2026-05-13: Recorded `evidence:20260513-superpowers-style-activation-checks` after source scans, Core smoke, Playbooks smoke, Core pack check, Playbooks pack check, and `git diff --check` passed. Closed the ticket with no separate audit per the acceptance audit posture.
- 2026-05-13: Reopened implementation after operator feedback that the first pass did not follow Superpowers closely enough. Switched OpenCode Core from `config.instructions` bootstrap to first-user-message injection, added exact Superpowers enforcement language, added activation test scripts, added `CLAUDE.md` harness acceptance guidance, ran live activation tests, reran package checks, updated evidence, and left the ticket closed with the stronger closure claim.
- 2026-05-14: Final review corrected the scope note to match the implementation and repository instruction that `using-loom` ordered references stay aligned across existing preload surfaces. The implementation still does not change non-OpenCode transport mechanics.
- 2026-05-14: Operator feedback identified product-surface leakage in `activation-discipline.md`: package-smoke guidance, adapter-mechanics explanation, skill-description preference prose, and self-justification. Removed those sections from shipped skill prose, removed the matching smoke-required phrases, and kept the activation reference focused on agent-facing behavior.
