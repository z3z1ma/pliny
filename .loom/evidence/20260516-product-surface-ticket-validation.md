# Product Surface Follow-up Ticket Validation

Status: recorded
Created: 2026-05-16
Updated: 2026-05-16
Observed: 2026-05-16

## Summary

This dossier records final validation observations for the four product-surface
follow-up tickets created from `.loom/research/20260516-product-surface-scan.md`. It groups
source inspections, targeted searches, package checks, explicit skill request tests,
and formatting checks used by ticket review and closure.

## Observations

- Observation: Playbook package smoke passed after command-description generation changes.
  - Procedure/source: `npm --prefix loom-playbooks run smoke` from repository root.
  - Actual result: command exited successfully. Smoke reported `ok: true`,
    `commandCount: 25`, `macroCount: 25`, `registeredPlaybookSkillPaths: []`,
    `playbookSkillPathsRegistered: false`, and
    `explicitDescriptionPrefixFailures: []`.

- Observation: Playbook dry-run package check passed after command-description generation changes.
  - Procedure/source: `npm --prefix loom-playbooks run pack:check` from repository root.
  - Actual result: command exited successfully. It reran smoke successfully and `npm pack --dry-run` completed for `@z3z1ma/open-loom-playbooks@0.3.0` with 53 files.

- Observation: Generated Playbook command descriptions match source Playbook frontmatter descriptions after parsing quoted YAML frontmatter.
  - Procedure/source: Node one-liner compared every `loom-playbooks/playbooks/*/SKILL.md` `description:` field with the matching `loom-playbooks/commands/*.toml` `description`.
  - Actual result: `matched 25 command descriptions`.

- Observation: No generated command description retains the forbidden generic prefix.
  - Procedure/source: content search for `Explicit optional workflow macro for` under `loom-playbooks/commands/*.toml`.
  - Actual result: no files found.

- Observation: The activation scenario fixture no longer contains the stale natural-prompt Playbook expectation patterns checked during review.
  - Procedure/source: content search under `evals/activation/*.md` for `likely workflow route`, `agent invokes \`loom-debugging-and-error-recovery\``, and `auto-trigger`.
  - Actual result: no files found.

- Observation: Docs/source search for Playbook raw exposure and natural autoactivation wording returned remaining intentional or qualified references.
  - Procedure/source: content search over Markdown for `loom-playbooks/playbooks`, `auto-load`, `auto-trigger`, `natural prompt`, `natural-language`, `autoactivation`, and `auto-activation`.
  - Actual result: source-doc references in `INSTALL.md` and `loom-playbooks/README.md` now qualify raw `loom-playbooks/playbooks` exposure as explicit-only or deliberate-invocation setup. Other matches include Loom tickets, specs, research, knowledge, and existing architecture/README explanations of Core-first natural routing.

- Observation: Explicit Loom skill request tests passed with the stricter first-action failure logic.
  - Procedure/source: `bash tests/explicit-skill-requests/run-all.sh` from repository root with a 300-second command timeout.
  - Actual result: all four cases passed: `loom-tickets`, `loom-ralph`, `loom-evidence`, and `loom-audit`. Each reported `OK: no non-skill tool invocation before first skill tool call` and detected the requested skill. An earlier 120-second local rerun timed out during the `loom-audit` case before completion; the later 300-second run supersedes that incomplete observation.

- Observation: Controlled parser probe fails when the wrong skill is first and the requested skill appears later.
  - Procedure/source: `bash tests/explicit-skill-requests/run-test.sh loom-audit --check-log tests/explicit-skill-requests/wrong-skill-first-requested-later.jsonl` from repository root, wrapped to expect exit code `1`.
  - Actual result: the runner printed `FAIL: first skill tool invocation was not 'loom-audit'`, showed first payload `{"tool":"skill","skill":"loom-tickets"}`, listed both skills mentioned in the log, and the wrapper printed `expected failure observed`.

- Observation: Explicit Loom skill request tests passed after the wrong-skill-first parser probe was added.
  - Procedure/source: `bash tests/explicit-skill-requests/run-all.sh` from repository root with a 300-second command timeout.
  - Actual result: the parser probe failed the wrong-skill-first/requested-skill-later fixture as expected, then all four live cases passed. Each live case reported `PASS: explicit skill '<skill>' was triggered first`.

- Observation: The wrong-skill-first parser probe was tightened and the explicit request suite still passed.
  - Procedure/source: source inspection of `tests/explicit-skill-requests/run-all.sh`, followed by `bash tests/explicit-skill-requests/run-all.sh` from repository root with a 300-second command timeout.
  - Actual result: `run-all.sh` now captures parser-probe output and requires exit status `1` plus the message `FAIL: first skill tool invocation was not 'loom-audit'`; the suite printed `PASS: parser probe failed wrong-skill-first/requested-skill-later log` and all four live cases passed with the requested skill triggered first.

- Observation: Markdown/generated-file whitespace check passed.
  - Procedure/source: `git diff --check` from repository root.
  - Actual result: command exited successfully with no output.

- Observation: Final reconciliation checks passed after audit records and ticket closures were updated.
  - Procedure/source: reran `npm --prefix loom-playbooks run smoke`, `npm --prefix loom-playbooks run pack:check`, the parsed command-description comparison Node one-liner, `bash tests/explicit-skill-requests/run-all.sh`, and `git diff --check` from repository root.
  - Actual result: Playbooks smoke and pack checks passed, generated descriptions still matched all 25 source descriptions, explicit skill request suite passed with the tightened parser probe and all four live cases, and `git diff --check` exited successfully with no output.

## Artifacts

- Command excerpts are summarized above. No separate raw log artifact was persisted.
those temp logs were not copied into `.loom/evidence/.storage/`.

## What This Shows

- `.loom/tickets/done/20260516-activation-scenarios-core-first-playbooks.md#ACC-001` - supports - targeted fixture search found no stale `loom-idea-refine` natural-prompt expectation pattern checked during review.
- `.loom/tickets/done/20260516-activation-scenarios-core-first-playbooks.md#ACC-002` - supports - targeted fixture search found no stale debugging Playbook invocation expectation pattern checked during review.
- `.loom/tickets/done/20260516-activation-scenarios-core-first-playbooks.md#ACC-003` - supports - `git diff --check` passed; search results show wording remains framed around Core-first natural routing and no Playbook auto-load.
- `.loom/tickets/done/20260516-playbook-command-descriptions-source.md#ACC-001` - supports - source helper now emits source descriptions, and generated comparison matched all 25 descriptions.
- `.loom/tickets/done/20260516-playbook-command-descriptions-source.md#ACC-002` - supports - generated command descriptions matched all 25 source descriptions and no generated command description contained the forbidden prefix.
- `.loom/tickets/done/20260516-playbook-command-descriptions-source.md#ACC-003` - supports - smoke showed Playbooks still register as commands, with no registered Playbook skill paths.
- `.loom/tickets/done/20260516-playbook-command-descriptions-source.md#ACC-004` - supports - `git diff --check` passed.
- `.loom/tickets/done/20260516-generic-playbook-install-safety.md#ACC-001` - supports - source-doc search and inspection showed generic raw Playbook exposure is now qualified.
- `.loom/tickets/done/20260516-generic-playbook-install-safety.md#ACC-002` - supports - fallback wording search/inspection showed Core-first natural routing remains explicit.
- `.loom/tickets/done/20260516-generic-playbook-install-safety.md#ACC-003` - supports - docs still describe explicit Playbook surfaces without changing package entrypoints or generated command mechanics.
- `.loom/tickets/done/20260516-generic-playbook-install-safety.md#ACC-004` - supports - `git diff --check` passed.
- `.loom/tickets/done/20260516-explicit-skill-test-first-action-failures.md#ACC-001` - supports - strict runner logic now fails the controlled wrong-skill-first fixture and the passing suite shows no premature non-skill tools before first skill call.
- `.loom/tickets/done/20260516-explicit-skill-test-first-action-failures.md#ACC-002` - supports - the runner now requires the first skill payload to match the requested skill in live cases; source inspection covers the no-skill branch.
- `.loom/tickets/done/20260516-explicit-skill-test-first-action-failures.md#ACC-003` - supports - review diff removed the previous `todowrite` exemption from the pre-first-skill check.
- `.loom/tickets/done/20260516-explicit-skill-test-first-action-failures.md#ACC-004` - supports - explicit request suite passed under OpenCode and `git diff --check` passed.

## What This Does Not Show

- This evidence does not by itself accept or close any ticket; ticket closure and audit disposition remain ticket-owned.
- The controlled parser probe proves the wrong-skill-first/requested-skill-later branch, but no separate fixture in this dossier proves the no-skill branch or a non-skill-tool-before-skill branch; those remain source-inspection-backed.
- The docs search does not prove every possible third-party harness honors explicit-only metadata; it only supports that project docs now qualify raw Playbook exposure and keep Core-first natural routing.
- The package checks cover Playbooks package smoke/pack behavior, not Core package smoke/pack behavior.
- Temp logs under `/tmp/loom-tests/` may expire; re-run the commands if fresh raw logs are needed.

## Related Records

- `.loom/research/20260516-product-surface-scan.md` - source of the follow-up recommendations.
- `.loom/specs/playbook-explicit-macros.md` - expected Playbook explicit macro behavior and command-description requirement.
- `.loom/tickets/done/20260516-activation-scenarios-core-first-playbooks.md` - activation fixture ticket.
- `.loom/tickets/done/20260516-playbook-command-descriptions-source.md` - generated command description ticket.
- `.loom/tickets/done/20260516-generic-playbook-install-safety.md` - install/docs safety ticket.
- `.loom/tickets/done/20260516-explicit-skill-test-first-action-failures.md` - explicit skill request test hardening ticket.
