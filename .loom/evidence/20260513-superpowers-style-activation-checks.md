# Superpowers-Style Activation Checks

ID: evidence:20260513-superpowers-style-activation-checks
Type: Evidence Dossier
Status: recorded
Created: 2026-05-13
Updated: 2026-05-14
Observed: 2026-05-13 to 2026-05-14

## Summary

Validation dossier for `ticket:20260513-superpowers-style-activation-doctrine`. It groups source scans, package checks, script syntax checks, and live OpenCode activation tests showing that the Superpowers-style bootstrap, language, red flags, trigger-description checks, and invocation tests are present and passing.

## Observations

- Observation: Core smoke passed with OpenCode first-user-message bootstrap and activation checks enabled.
  - Procedure/source: `npm --prefix loom-core run smoke` from repository root after the activation edits.
  - Actual result: command exited successfully and printed `"ok": true`, `instructionCount: 0`, `doesNotUseConfigInstructionsForBootstrap: true`, `bootstrapInjectionPartCount: 1`, `bootstrapInjectionIsDeduped: true`, `usingLoomResult` describing `experimental.chat.messages.transform`, `activationChecks.ok: true`, `missingPhrases: []`, and `triggerDescriptionFailures: []`.

- Observation: Playbooks smoke passed with trigger-description checks enabled.
  - Procedure/source: `npm --prefix loom-playbooks run smoke` from repository root after the activation edits.
  - Actual result: command exited successfully and printed `"ok": true`, `activationChecks.ok: true`, and `triggerDescriptionFailures: []`.

- Observation: Core package dry-run check passed.
  - Procedure/source: `npm --prefix loom-core run pack:check` from repository root.
  - Actual result: smoke passed, `npm pack --dry-run` completed, and the tarball contents included `skills/using-loom/references/activation-discipline.md`.

- Observation: Playbooks package dry-run check passed.
  - Procedure/source: `npm --prefix loom-playbooks run pack:check` from repository root.
  - Actual result: smoke passed and `npm pack --dry-run` completed with the 25 playbook skills included.

- Observation: Markdown/whitespace diff check passed for tracked diffs.
  - Procedure/source: `git diff --check` from repository root after edits.
  - Actual result: command exited successfully with no output.

- Observation: Final bootstrap-validation pass succeeded after the ticket scope wording was corrected.
  - Procedure/source: `git diff --check`, `npm --prefix loom-core run smoke`, `npm --prefix loom-playbooks run smoke`, `gemini extensions validate "$PWD"`, `gemini extensions validate "$PWD/loom-core"`, and `gemini extensions validate "$PWD/loom-playbooks"` from repository root on 2026-05-14.
  - Actual result: `git diff --check` exited successfully with no output. Core smoke printed `"ok": true`, `instructionCount: 0`, `doesNotUseConfigInstructionsForBootstrap: true`, `bootstrapInjectionPartCount: 1`, `bootstrapInjectionIsDeduped: true`, and `activationChecks.ok: true`. Playbooks smoke printed `"ok": true` and `activationChecks.ok: true`. All three Gemini extension validation commands reported successful validation.

- Observation: Product-surface cleanup removed meta activation prose from shipped Core skills.
  - Procedure/source: targeted scans under `loom-core/skills` for `Adapter mechanics`, `Package smoke`, `Skill descriptions are`, `Skill registration alone`, `registered skill directory`, `description preferences`, and `trigger-oriented shape`; targeted scan of `loom-core/skills/using-loom/references/activation-discipline.md` for `adapter`, `package`, `smoke`, `skill descriptions`, `registered skill`, `registration`, and `trigger-oriented`; `npm --prefix loom-core run smoke`; `npm --prefix loom-playbooks run smoke`; `npm --prefix loom-core run pack:check`; `git diff --check`.
  - Actual result: both targeted shipped-skill scans returned no matches. Core smoke passed with `activationChecks.ok: true`, `requiredPhraseCount: 18`, and `missingPhrases: []`. Playbooks smoke passed with `activationChecks.ok: true`. Core package check passed and included the 3.0 kB `activation-discipline.md` in the dry-run package. `git diff --check` exited successfully with no output.

- Observation: Activation test scripts have valid Bash syntax.
  - Procedure/source: `bash -n tests/skill-triggering/run-test.sh && bash -n tests/skill-triggering/run-all.sh && bash -n tests/explicit-skill-requests/run-test.sh && bash -n tests/explicit-skill-requests/run-all.sh`.
  - Actual result: command exited successfully with no output.

- Observation: The Superpowers-style acceptance prompt triggered Loom idea refinement in a live OpenCode test.
  - Procedure/source: `bash tests/skill-triggering/run-test.sh loom-idea-refine tests/skill-triggering/prompts/loom-idea-refine.txt 3`.
  - Actual result: command exited successfully and printed `PASS: skill 'loom-idea-refine' was triggered`; log path `/tmp/loom-tests/1778771862/skill-triggering/loom-idea-refine/opencode-output.json`.

- Observation: Natural-prompt skill triggering tests passed in live OpenCode runs.
  - Procedure/source: `npm run test:skill-triggering`.
  - Actual result: command exited successfully. Prompts triggered `loom-idea-refine`, `loom-debugging-and-error-recovery`, `loom-tickets`, and `loom-ralph`; logs were written under `/tmp/loom-tests/1778771929/skill-triggering/` and sibling timestamped directories reported by the script.

- Observation: Explicit skill request tests passed in live OpenCode runs with no non-skill tool before the first skill tool call.
  - Procedure/source: `npm run test:explicit-skill-requests`.
  - Actual result: command exited successfully. Requests triggered `loom-tickets`, `loom-ralph`, `loom-evidence`, and `loom-audit`; each run printed `OK: no non-skill tool invocation before first skill tool call` and `PASS`; logs were written under `/tmp/loom-tests/1778771930/explicit-skill-requests/` and sibling timestamped directories reported by the script.

- Observation: Targeted activation scan found the exact Superpowers-style enforcement phrases, first-action ordering, red flags, OpenCode transform path, and skills-path registration.
  - Procedure/source: repository content search for `If you think there is even a 1% chance a skill might apply`, `IF A SKILL APPLIES TO YOUR TASK`, `clarifying questions`, `code exploration`, `quick checks`, `this is simple`, `I need more context first`, `I'll just do this one thing first`, `experimental.chat.messages.transform`, and `config.skills.paths`.
  - Actual result: matches appeared in `loom-core/skills/using-loom/SKILL.md`, `loom-core/skills/using-loom/references/activation-discipline.md`, `loom-core/loom-core.mjs`, docs, `AGENTS.md`, the ticket, and research.

- Observation: Trigger-description scans found no shipped Core or Playbooks skill descriptions outside the accepted activation prefixes.
  - Procedure/source: repository content search for `^description: "(?!Always activate|Use when|Use before|Use after)` under `loom-core/skills` and `^description: "(?!Use when|Use before|Use after)` under `loom-playbooks/skills`.
  - Actual result: no matches found.

## Artifacts

- Command output: `npm --prefix loom-core run smoke` - passed with activation checks enabled and no missing phrases or trigger-description failures.
- Command output: `npm --prefix loom-playbooks run smoke` - passed with trigger-description checks enabled and no description failures.
- Command output: `npm --prefix loom-core run pack:check` - passed and included `activation-discipline.md` in the dry-run package.
- Command output: `npm --prefix loom-playbooks run pack:check` - passed.
- Command output: `bash -n ...` over the four activation test scripts - passed.
- Command output: `bash tests/skill-triggering/run-test.sh loom-idea-refine tests/skill-triggering/prompts/loom-idea-refine.txt 3` - passed.
- Command output: `npm run test:skill-triggering` - passed live OpenCode skill-triggering tests.
- Command output: `npm run test:explicit-skill-requests` - passed live OpenCode explicit-skill tests with no premature non-skill tools.
- Command output: `git diff --check` - passed with no output.
- Command output: final 2026-05-14 bootstrap-validation pass - `git diff --check`, Core smoke, Playbooks smoke, and root/Core/Playbooks Gemini extension validation all passed.
- Command output: final product-surface cleanup pass - targeted shipped-skill scans found no package-smoke, adapter-mechanics, registered-skill-directory, or skill-description-preference language in `activation-discipline.md` or Core shipped skills; Core smoke, Playbooks smoke, Core pack check, and `git diff --check` passed.
- Source paths: `loom-core/skills/using-loom/SKILL.md`, `loom-core/skills/using-loom/references/activation-discipline.md`, `loom-core/loom-core.mjs`, `loom-playbooks/loom-playbooks.mjs`, `tests/skill-triggering/**`, `tests/explicit-skill-requests/**`, `CLAUDE.md`, `evals/activation/loom-activation-scenarios.md`, `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, `INSTALL.md`, `loom-core/README.md`, `loom-playbooks/README.md`.

## What This Shows

- `ticket:20260513-superpowers-style-activation-doctrine#ACC-001` - supports - Core smoke and source inspection show OpenCode uses `config.skills.paths` plus first-user-message `experimental.chat.messages.transform`, not `config.instructions`, and dedupes injection. The final bootstrap-validation pass also shows the Gemini extension surfaces validate after adding the activation reference.
- `ticket:20260513-superpowers-style-activation-doctrine#ACC-002` - supports - exact Superpowers-style enforcement phrases are present in model-visible Core doctrine and statically checked by Core smoke.
- `ticket:20260513-superpowers-style-activation-doctrine#ACC-003` - supports - first-action ordering before clarifying questions, code exploration, quick checks, edits, tickets, Ralph, evidence, audit, and closure is present in doctrine and bootstrap text.
- `ticket:20260513-superpowers-style-activation-doctrine#ACC-004` - supports - requested red-flag rationalizations are present in `using-loom` and the activation reference.
- `ticket:20260513-superpowers-style-activation-doctrine#ACC-005` - supports - Core and Playbooks smoke checks and targeted scans show trigger-oriented descriptions with no prefix failures.
- `ticket:20260513-superpowers-style-activation-doctrine#ACC-006` - supports - Superpowers-modeled natural prompt and explicit request scripts exist and pass live OpenCode runs.
- `ticket:20260513-superpowers-style-activation-doctrine#ACC-007` - supports - `CLAUDE.md` includes the `Let's make a react todo list` acceptance test, and the live `loom-idea-refine` run passed for that prompt.

## What This Does Not Show

This evidence shows live OpenCode behavior for the new activation scripts, but it does not show live behavior in Claude Code, Cursor, Codex, Gemini, or Copilot. The tests detect skill invocation and premature non-skill tool use for explicit requests; they do not prove every loaded skill followed its full procedure after activation. `git diff --check` was run against tracked diffs; package checks covered package-visible files, including the new Core activation reference.

## Related Records

- `ticket:20260513-superpowers-style-activation-doctrine` - ticket whose acceptance this dossier supports.
- `research:20260513-superpowers-skill-activation` - source investigation behind the changes.
