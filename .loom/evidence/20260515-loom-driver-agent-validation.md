# Loom Driver Agent Validation

ID: evidence:20260515-loom-driver-agent-validation
Type: Evidence Dossier
Status: recorded
Created: 2026-05-15
Updated: 2026-05-15
Observed: 2026-05-15 05:58 UTC

## Summary

This dossier records validation observations for `ticket:20260515-loom-driver-agent` after adding the Loom Driver prompt, Codex TOML, OpenCode registration, Claude manifest exposure, and human-facing docs.

## Observations

- Observation: Core smoke check passed.
  - Procedure/source: Ran `npm --prefix loom-core run smoke` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after the implementation edits.
  - Actual result: Command exited successfully with `ok: true`, `agentCount: 2`, agent names `loom-driver` and `loom-weaver`, Driver OpenCode mode `all`, Driver task permission `allow`, Driver high-authority prompt check true, and Driver Codex developer instructions matching the canonical Markdown prompt.

- Observation: Core dry package check passed.
  - Procedure/source: Ran `npm --prefix loom-core run pack:check` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after the implementation edits.
  - Actual result: Command exited successfully. The dry-run tarball contents included `agents/loom-driver.md` and `codex/agents/loom-driver.toml`, along with the existing Core package files.

- Observation: Markdown and diff whitespace check passed.
  - Procedure/source: Ran `git diff --check` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after the implementation edits.
  - Actual result: Command exited successfully with no output.

- Observation: Claude Core plugin manifest validation passed.
  - Procedure/source: Ran `claude plugin validate "$PWD/loom-core"` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after adding `loom-driver` to the Claude plugin agent list.
  - Actual result: Command exited successfully and reported validation passed for `loom-core/.claude-plugin/plugin.json`.

- Observation: Prompt-surface grep found required Driver behavior language.
  - Procedure/source: Searched `loom-core/agents/loom-driver.md` and `loom-core/codex/agents/loom-driver.toml` for `inner loop`, `Ralph packet`, `high-authority`, `Parallelize`, `evidence`, `audit`, and `ticket`.
  - Actual result: Both model-visible Driver surfaces contained the expected inner-loop, packet, high-authority boundary, parallelization, evidence, audit, and ticket reconciliation language.

- Observation: Product-surface leakage scan over agent prompts found no smoke, dogfood, repository workflow, npm, pack-check, or contributor-process terms in the new Driver prompt.
  - Procedure/source: Searched `loom-core/agents/*.md` and `loom-core/codex/agents/*.toml` for package, smoke, adapter, dogfood, repository workflow, contributor, npm, pack-check, Git, and worktree terms.
  - Actual result: Driver matches were limited to generic execution vocabulary: `worktree` as part of Ralph packet source snapshot guidance and `package` in the generic phrase about prompt, manifest, package, or record shape. Existing Weaver matches remained unchanged. The scan did not find package-smoke, dogfood, repository workflow, npm, pack-check, or contributor-process leakage in Driver model-visible instructions.

## Artifacts

- `npm --prefix loom-core run smoke` output - shows Core bundle inspection with both named agents, Driver OpenCode registration, and Driver Codex prompt parity.
- `npm --prefix loom-core run pack:check` output - shows Core smoke plus dry package contents containing the new Driver Markdown and TOML files.
- `git diff --check` output - no output, indicating no whitespace errors in the diff.
- `claude plugin validate "$PWD/loom-core"` output - reports Claude plugin validation passed after manifest update.
- Grep results for Driver behavior and leakage terms - show required behavior terms present and no contributor-process leakage beyond generic execution vocabulary.

## What This Shows

- `ticket:20260515-loom-driver-agent#ACC-001` - supports - canonical Driver prompt and Codex TOML contain inner-loop execution, packet-first, parallelization, evidence, audit, ticket reconciliation, and high-authority record boundary language.
- `ticket:20260515-loom-driver-agent#ACC-002` - supports - Core smoke observed OpenCode registration for `loom-driver` with mode `all`, high-authority prompt check true, and task permission `allow`.
- `ticket:20260515-loom-driver-agent#ACC-003` - partially supports - Claude manifest validation passed, Cursor agent directory exposure remained manifest-backed, Codex TOML exists and matches the canonical prompt, and Gemini continues to package agents through the Core agent directory; live runtime invocation was not tested.
- `ticket:20260515-loom-driver-agent#ACC-004` - supports - docs were updated while model-critical behavior remained in `loom-core/agents/loom-driver.md` and `loom-core/codex/agents/loom-driver.toml`; grep did not find contributor-process leakage in Driver instructions.
- `ticket:20260515-loom-driver-agent#ACC-005` - supports - Core smoke, Core dry pack check, `git diff --check`, and Claude plugin validation passed.

## What This Does Not Show

This evidence does not prove live runtime invocation in OpenCode, Claude Code, Codex, Cursor, or Gemini. It does not prove that OpenCode permission matching enforces the high-authority record deny rules in every runtime path. It does not prove ticket closure because `ticket:20260515-loom-driver-agent#ACC-006` still requires a fresh Ralph-backed audit pass.

## Related Records

- `ticket:20260515-loom-driver-agent` - consuming ticket for these observations.
- `spec:loom-driver-agent` - behavior contract these observations support.
- `packet:20260515T054840Z-loom-driver-agent-implementation` - implementation packet that requested this validation evidence.
