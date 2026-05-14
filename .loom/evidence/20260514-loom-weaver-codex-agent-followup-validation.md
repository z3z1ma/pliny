# Loom Weaver Codex Agent Follow-up Validation

ID: evidence:20260514-loom-weaver-codex-agent-followup-validation
Type: Evidence Dossier
Status: recorded
Created: 2026-05-14
Updated: 2026-05-14
Observed: 2026-05-14 23:14 UTC

## Summary

This dossier records validation after revising Codex support for
`ticket:20260514-loom-weaver-agent` from a bundled Core skill to a documented
Codex custom-agent TOML install under `~/.codex/agents/`.

## Observations

- Observation: The Core `loom-weaver` skill surface was removed.
  Procedure/source: Source tree inspection through `git status --short` and absence of `loom-core/skills/loom-weaver/SKILL.md` after the follow-up patch.
  Actual result: The Loom Weaver behavior no longer ships as a Core skill. Core smoke reported `skillCount: 11`, matching the pre-Loom-Weaver Core record skill count.

- Observation: Codex custom-agent TOML exists and matches the canonical Loom Weaver agent prompt.
  Procedure/source: Source inspection of `loom-core/codex/agents/loom-weaver.toml`, `loom-core/agents/loom-weaver.md`, and revised Core smoke output.
  Actual result: The TOML defines `name = "loom-weaver"`, `description`, `sandbox_mode = "workspace-write"`, and `developer_instructions`. Core smoke reported `codexLoomWeaverAgentPath: "codex/agents/loom-weaver.toml"`, `codexLoomWeaverHasDeveloperInstructions: true`, `codexLoomWeaverHasWriteBoundary: true`, and `codexLoomWeaverPromptMatchesAgent: true`.

- Observation: `AGENTS.md` audit `FIND-001` was addressed.
  Procedure/source: Source inspection of `AGENTS.md` after the follow-up patch.
  Actual result: Contributor guidance now includes `loom-core/agents/` and `loom-core/codex/agents/` wherever it names model-visible product behavior surfaces and product-surface leakage scan targets.

- Observation: Codex installation docs use the requested custom-agent install shape.
  Procedure/source: Source inspection of `INSTALL.md` after the follow-up patch.
  Actual result: Docs include `mkdir -p ~/.codex/agents` and `curl -fsSL https://raw.githubusercontent.com/z3z1ma/agent-loom/main/loom-core/codex/agents/loom-weaver.toml -o ~/.codex/agents/loom-weaver.toml`, plus a local copy alternative. Docs describe natural-language use of the `loom-weaver` custom agent and `/agent` thread management, and do not claim `@<agent>` custom-agent invocation.

- Observation: Core smoke passed after the Codex custom-agent revision.
  Procedure/source: Ran `npm --prefix loom-core run smoke` from `/Users/alexanderbutler/code_projects/personal/agent-loom`.
  Actual result: The first follow-up smoke run failed because the smoke parser kept the TOML multiline string's leading newline, making `codexLoomWeaverPromptMatchesAgent: false`. After fixing the parser, the command passed with `ok: true`, `skillCount: 11`, `agentCount: 1`, `codexLoomWeaverPromptMatchesAgent: true`, and `loomWeaverOpenCodeMode: "all"`.

- Observation: Core package dry-run passed and includes the Codex custom-agent artifact.
  Procedure/source: Ran `npm --prefix loom-core run pack:check` from `/Users/alexanderbutler/code_projects/personal/agent-loom`.
  Actual result: Command exited successfully. The dry-run tarball included `agents/loom-weaver.md`, `codex/agents/loom-weaver.toml`, `loom-core.mjs`, `package.json`, and Core skills. It did not include a `skills/loom-weaver/SKILL.md` file.

- Observation: Adapter and whitespace validation passed after the follow-up patch.
  Procedure/source: Ran `git diff --check`, `claude plugin validate "$PWD/loom-core"`, and `gemini extensions validate "$PWD/loom-core"` from `/Users/alexanderbutler/code_projects/personal/agent-loom`.
  Actual result: `git diff --check` exited with no output. Claude plugin validation passed. Gemini extension validation passed.

## Artifacts

- `loom-core/codex/agents/loom-weaver.toml` - Codex custom-agent definition intended to be installed under `~/.codex/agents/loom-weaver.toml`.
- `loom-core/agents/loom-weaver.md` - canonical Loom Weaver agent prompt body matched by the Codex TOML developer instructions.
- `loom-core/loom-core.mjs` - smoke inspection now verifies Codex TOML presence, write boundary, developer instructions, and prompt-body match.
- `INSTALL.md` - contains GitHub raw `curl` and local copy installation paths for Codex.
- `AGENTS.md` - includes `loom-core/codex/agents/` in model-visible product-surface guidance.

## What This Shows

- `ticket:20260514-loom-weaver-agent#ACC-001` - supports - Loom Weaver behavior remains in canonical agent prompt and Codex TOML developer instructions with prompt-body match verified by smoke.
- `ticket:20260514-loom-weaver-agent#ACC-002` - supports - OpenCode registration still reports `loomWeaverOpenCodeMode: "all"` and the `.loom/**` write-boundary prompt/permission shape in smoke output.
- `ticket:20260514-loom-weaver-agent#ACC-003` - supports - Claude plugin validation passed with the agent file manifest shape.
- `ticket:20260514-loom-weaver-agent#ACC-004` - partially supports - Gemini extension validation passed with `agents/loom-weaver.md` present, but live `@loom-weaver` runtime invocation was not tested.
- `ticket:20260514-loom-weaver-agent#ACC-006` - supports - Codex now ships a ready custom-agent TOML and docs show installation under `~/.codex/agents/`; docs avoid `@<agent>` and plugin-shipped profile/custom-agent claims.
- `ticket:20260514-loom-weaver-agent#ACC-007` - supports - docs describe harness-specific invocation and avoid universal syntax claims.
- `ticket:20260514-loom-weaver-agent#ACC-008` - supports - Core smoke, Core pack dry-run, Claude validation, Gemini validation, and `git diff --check` passed after the follow-up patch.

## What This Does Not Show

- This evidence does not prove live runtime invocation inside Codex, OpenCode, Claude Code, Cursor, or Gemini CLI.
- This evidence does not prove Codex will automatically spawn the custom agent for every natural-language request; Codex docs say custom agents are spawned when explicitly asked.
- This evidence does not validate Cursor plugin behavior with a local validator.
- This evidence does not replace the required fresh audit/review pass after the follow-up changes.

## Related Records

- `ticket:20260514-loom-weaver-agent` - consuming ticket and acceptance criteria.
- `spec:loom-weaver-agent` - behavior contract and Codex custom-agent decision.
- `research:20260514-direct-interactive-agent-surfaces` - source-backed harness capability research.
- `packet:20260514T230546Z-loom-weaver-codex-agent-followup` - follow-up implementation packet.
- `evidence:20260514-loom-weaver-implementation-validation` - prior evidence record, superseded for the Codex bundled-skill path by this dossier.
