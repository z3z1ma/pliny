# Loom Weaver Implementation Validation

ID: evidence:20260514-loom-weaver-implementation-validation
Type: Evidence Dossier
Status: recorded
Created: 2026-05-14
Updated: 2026-05-14
Observed: 2026-05-14 22:55 UTC

## Summary

This dossier records source inspection, source-doc recheck, package checks, and
adapter validation for `ticket:20260514-loom-weaver-agent` after adding the Loom
Weaver agent and Codex bundled skill path.

Freshness note: the Codex bundled-skill observations in this dossier were
superseded by `evidence:20260514-loom-weaver-codex-agent-followup-validation`
after the operator chose a Codex custom-agent TOML install path instead of a Core
skill. Non-Codex observations remain historical evidence for the earlier
implementation slice.

## Observations

- Observation: Codex official docs were rechecked for plugin, subagent, config, and CLI support.
  Procedure/source: Fetched `https://developers.openai.com/codex/plugins`, `https://developers.openai.com/codex/plugins/build`, `https://developers.openai.com/codex/subagents`, `https://developers.openai.com/codex/config-reference`, and `https://developers.openai.com/codex/cli/reference` on 2026-05-14.
  Actual result: Codex plugin docs describe bundled `skills`, `apps`, `mcpServers`, `hooks`, `interface.defaultPrompt`, and plugin/skill `@` use. Custom agents are documented as standalone TOML under `~/.codex/agents/` or `.codex/agents/`. Profiles and `--profile` are config/CLI surfaces. The fetched docs did not document plugin-shipped custom agents, plugin-shipped profiles, or `@<agent>` custom-agent invocation.

- Observation: Loom Weaver behavior exists in both Core agent and skill surfaces with synchronized prompt bodies.
  Procedure/source: Source inspection of `loom-core/agents/loom-weaver.md`, `loom-core/skills/loom-weaver/SKILL.md`, and Core smoke output.
  Actual result: Both files include the `.loom/` write boundary, non-source-edit refusal, adversarial shaping posture, two-or-three-options guidance, Loom surface routing, skill-use instruction where supported, evidence/audit honesty, and handoff to ticket/Ralph for implementation. Core smoke reported `loomWeaverPromptBodiesMatch: true`.

- Observation: OpenCode Core smoke passed after adding Loom Weaver.
  Procedure/source: Ran `npm --prefix loom-core run smoke` from `/Users/alexanderbutler/code_projects/personal/agent-loom`.
  Actual result: Command exited successfully with `ok: true`, `skillCount: 12`, `agentCount: 1`, `agentNames: ["loom-weaver"]`, `loomWeaverOpenCodeMode: "all"`, `loomWeaverPromptHasWriteBoundary: true`, and `loomWeaverEditPermission: {"*":"deny",".loom/**":"allow"}`.

- Observation: Core package dry-run passed and includes Loom Weaver package artifacts.
  Procedure/source: Ran `npm --prefix loom-core run pack:check` from `/Users/alexanderbutler/code_projects/personal/agent-loom`.
  Actual result: Command exited successfully. The dry-run tarball included `agents/loom-weaver.md`, `skills/loom-weaver/SKILL.md`, `loom-core.mjs`, `package.json`, and Core skills. It did not include the removed `codex/loom-weaver-profile.toml` path.

- Observation: Claude plugin validation initially rejected the manifest agent path shape and then passed after correction.
  Procedure/source: Ran `claude plugin validate "$PWD/loom-core"` from `/Users/alexanderbutler/code_projects/personal/agent-loom`.
  Actual result: Validation first failed with `agents: Invalid input` while the manifest used a directory string. After changing `loom-core/.claude-plugin/plugin.json` to `"agents": ["./agents/loom-weaver.md"]`, validation passed.

- Observation: Gemini Core extension validation passed with the bundled `agents/` directory present.
  Procedure/source: Ran `gemini extensions validate "$PWD/loom-core"` from `/Users/alexanderbutler/code_projects/personal/agent-loom`.
  Actual result: Command exited successfully with `Extension /Users/alexanderbutler/code_projects/personal/agent-loom/loom-core has been successfully validated.`

- Observation: Markdown/diff whitespace check passed after the final manifest correction.
  Procedure/source: Ran `git diff --check` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after the final Claude manifest edit.
  Actual result: Command exited successfully with no output.

## Artifacts

- `loom-core/agents/loom-weaver.md` - Core agent prompt surface for OpenCode, Claude, Cursor, and Gemini-compatible agent directories.
- `loom-core/skills/loom-weaver/SKILL.md` - Core bundled skill surface used for Codex plugin-native Loom Weaver support and as a synchronized behavior copy.
- `loom-core/loom-core.mjs` smoke output - reported `ok: true`, agent registration, skill registration, prompt-body match, and OpenCode edit permission shape.
- `loom-core/.claude-plugin/plugin.json` - validated after changing `agents` to a file array.
- `loom-core/.codex-plugin/plugin.json` - names plugin-native Loom Weaver use through the bundled skill and natural language, not profile copying.
- `INSTALL.md`, `README.md`, `loom-core/README.md`, and `AGENTS.md` - updated human-facing and contributor-facing guidance for shipped agent surfaces.

## What This Shows

- `ticket:20260514-loom-weaver-agent#ACC-001` - supports - source inspection and smoke output show the Loom Weaver prompt/skill bodies contain the required write boundary, shaping posture, challenge language, option recommendation guidance, Loom routing, and proof-honesty constraints.
- `ticket:20260514-loom-weaver-agent#ACC-002` - supports - Core smoke shows OpenCode registers `loom-weaver` with `mode: "all"`, prompt content, and `.loom/**` edit allowlist over default edit deny.
- `ticket:20260514-loom-weaver-agent#ACC-003` - supports - Claude plugin validation passed after the manifest named the agent file with the schema-supported `agents` array shape.
- `ticket:20260514-loom-weaver-agent#ACC-004` - partially supports - Gemini extension validation passed with `agents/loom-weaver.md` present, supporting package structure validity but not live `@loom-weaver` runtime invocation.
- `ticket:20260514-loom-weaver-agent#ACC-006` - supports - Codex docs and source inspection support the plugin-native bundled skill route and the decision not to ship or document manual profile copying as the default path.
- `ticket:20260514-loom-weaver-agent#ACC-007` - supports - human-facing docs now describe harness-specific invocation semantics and avoid claiming universal `@<agent>` support.
- `ticket:20260514-loom-weaver-agent#ACC-008` - supports - Core smoke, Core pack dry-run, Claude plugin validation, Gemini extension validation, and `git diff --check` passed.

## What This Does Not Show

- This evidence does not prove live runtime invocation inside OpenCode, Claude Code, Codex, Cursor, or Gemini CLI; it records source inspection, docs support, and available package/manifest validation.
- This evidence does not prove OpenCode's permission schema enforces `.loom/**` exactly at runtime; it records the configured permission shape and smoke inspection.
- This evidence does not validate Cursor plugin behavior with a harness validator; no Cursor validator was run or available in this session.
- This evidence does not replace the required audit/review pass for `ticket:20260514-loom-weaver-agent#ACC-009`.

## Related Records

- `ticket:20260514-loom-weaver-agent` - consuming ticket and acceptance criteria.
- `spec:loom-weaver-agent` - behavior contract for Loom Weaver.
- `research:20260514-direct-interactive-agent-surfaces` - source-backed harness capability research, amended for the Codex plugin-native skill route.
- `packet:20260514T223622Z-loom-weaver-agent-implementation` - implementation packet that produced these observations.
