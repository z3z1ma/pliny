# Loom Weaver Agent Implementation Packet

ID: packet:20260514T223622Z-loom-weaver-agent-implementation
Type: Packet
Status: consumed
Created: 2026-05-14 22:36 UTC
Updated: 2026-05-14 22:59 UTC
Target: ticket:20260514-loom-weaver-agent
Packet Kind: Ralph
Mode: execution
Context Style: live-reference
Worker: manual handoff - current session will execute from this packet
Branch: main
Worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
Iteration: 1
Risk: high - model-visible prompt and cross-harness adapter surfaces
Verification Posture: observation-first
Change Class: new optional Core agent persona and docs

## Mission

Implement the smallest complete Core Loom Weaver agent surface described by `ticket:20260514-loom-weaver-agent` and `spec:loom-weaver-agent`.

The run should add a canonical Loom Weaver prompt/agent source, expose it honestly through supported Core harness surfaces where current docs and repository shape support it, update package inclusion and human-facing invocation docs, gather validation evidence, and leave the ticket ready for audit/review rather than closed.

## Context Bundle

Records:

- `ticket:20260514-loom-weaver-agent` - executable scope, acceptance criteria, risk, and validation expectations.
- `spec:loom-weaver-agent` - behavior contract: `.loom/`-only writes, shaping-first, adversarial challenge, option recommendations, correct Loom record routing, and product-surface leakage constraints.
- `research:20260514-direct-interactive-agent-surfaces` - source-backed harness support matrix and invocation semantics.
- `AGENTS.md` - repository constraints for package shape, product-surface leakage, and validation commands.
- `INSTALL.md` - user-facing install matrix that may need invocation notes.

Evidence Or Artifacts:

- None yet. Create evidence after implementation observations and command outputs are available.

Files, Diffs, Or External References:

- `loom-core/loom-core.mjs` - OpenCode Core entrypoint and smoke inspection behavior.
- `loom-core/package.json` - Core package artifacts include list.
- `loom-core/.claude-plugin/plugin.json` - Claude plugin surface.
- `loom-core/.cursor-plugin/plugin.json` - Cursor plugin surface.
- `loom-core/.codex-plugin/plugin.json` - Codex plugin surface.
- `loom-core/gemini-extension.json` and `loom-core/gemini-bootstrap.md` - Gemini Core extension surface.
- Official harness docs named by `research:20260514-direct-interactive-agent-surfaces` when exact agent/rule/profile file shapes need confirmation.

## Read Scope

- `.loom/tickets/20260514-loom-weaver-agent.md`
- `.loom/specs/loom-weaver-agent.md`
- `.loom/research/20260514-direct-interactive-agent-surfaces.md`
- `AGENTS.md`
- `INSTALL.md`
- `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, and package READMEs if documentation updates require alignment.
- `loom-core/loom-core.mjs`
- `loom-core/package.json`
- `loom-core/.claude-plugin/**`
- `loom-core/.cursor-plugin/**`
- `loom-core/.codex-plugin/**`
- `loom-core/gemini-extension.json`
- `loom-core/gemini-bootstrap.md`
- Official OpenCode, Claude Code, Cursor, Codex, and Gemini docs only as source material for exact adapter shapes.

## Write Scope

Records Or Artifacts:

- `.loom/tickets/20260514-loom-weaver-agent.md` - update status/current state/journal when material progress, evidence, or review state changes.
- `.loom/specs/loom-weaver-agent.md` - update only if implementation reveals a behavior contract mismatch that does not require operator decision.
- `.loom/research/20260514-direct-interactive-agent-surfaces.md` - update Codex conclusions only for the operator clarification that Codex must not require manual profile copying.
- `.loom/evidence/**` - create evidence for command output, source inspections, and validation results.
- this packet - fill `## Worker Output` and update `Status:` when the run output is recorded.

Source Paths:

- `loom-core/**` - Core agent prompt/adapter/package changes only.
- `INSTALL.md`, `README.md`, package READMEs, `PROTOCOL.md`, or `ARCHITECTURE.md` - human-facing invocation/docs alignment only when necessary.
- Do not change `loom-playbooks/**` unless the implementation proves a direct docs cross-reference is necessary.

## Source Snapshot

- Branch: `main`.
- Worktree before this packet: `git status --short` produced no output.
- Existing Core package currently ships only `loom-core.mjs` and `skills/` in NPM `files`.
- Existing repository has no `agents/`, `rules/`, or prompt directory.
- Existing Core OpenCode entrypoint registers skills and first-user-message bootstrap only; no custom agent registration yet.
- Existing native plugin manifests expose skills/hooks only; no Loom Weaver agent surface yet.

## Scope Amendment

- 2026-05-14 22:55 UTC: Operator clarified Codex must not require manual profile copying and should use first-class plugin support where available. This packet may update `research:20260514-direct-interactive-agent-surfaces` and `spec:loom-weaver-agent` only to preserve that Codex plugin-surface decision and source recheck.

## Task

Implement the ticket inside the write scope.

Required outcomes:

- Add one canonical Loom Weaver behavior source that is model-visible to agent surfaces and satisfies `spec:loom-weaver-agent`.
- Expose Loom Weaver through OpenCode as the strongest direct agent surface available without breaking existing skills/bootstrap behavior.
- Expose or document Claude, Gemini, Cursor, and Codex Loom Weaver support only to the extent supported by current source-backed docs and repository adapter shapes.
- Update package metadata so new shippable agent/prompt artifacts are included in relevant package artifacts.
- Update human-facing docs with exact harness-specific invocation semantics.
- Run validation appropriate to touched files.
- Create evidence for observations and command outputs.
- Move the ticket to `review` if implementation and verification appear complete but audit remains required.

Non-goals:

- Do not make Loom Weaver a default startup persona automatically.
- Do not edit product source outside the ticket write scope.
- Do not add runtime infrastructure, helper CLIs, daemons, databases, or dashboards.
- Do not duplicate full `using-loom` doctrine in Loom Weaver instructions.
- Do not claim universal `@<agent>` support.

## Launch

Current session executes this packet. Read this packet first, stay inside it, and fill the output contract before the ticket relies on the result.

## Evidence, Review, Or Verification Expectations

- Source inspection and targeted grep must show the canonical Loom Weaver prompt includes `.loom/`-only write boundary, shaping-first behavior, adversarial challenge, options/recommendations, Loom surface routing, skill invocation where supported, and honest evidence/audit limits.
- Core smoke and Core pack check must pass after package changes.
- `git diff --check` must pass.
- If Claude plugin manifest or structure changes, run `claude plugin validate "$PWD/loom-core"` when the CLI is available.
- If Gemini manifest/extension changes, run `gemini extensions validate "$PWD/loom-core"`; run root/playbooks validation only if those surfaces are touched.
- Create a Loom evidence record summarizing command outputs and source inspection evidence.

## Stop Conditions

- Stop and escalate if exact adapter file shapes conflict with the research or are not source-verifiable enough to implement honestly.
- Stop and route to specs/operator if the implementation requires changing Loom Weaver from explicit-only into default startup behavior.
- Stop if write scope must expand to `loom-playbooks/**` or non-doc root files for reasons not named in the ticket.
- Stop if package validation reveals a broader packaging architecture change is needed.
- Stop if the `.loom/`-only boundary cannot be represented honestly for a target harness; document the limitation instead of pretending enforcement exists.

## Output Contract

The worker must update this packet or return output with:

- outcome: `continue`, `stop`, `blocked`, or `escalate`
- files changed
- records changed
- evidence, review findings, validation output, or observations gathered
- what was not verified or reviewed
- blockers, risks, or assumptions discovered
- recommended next move for the consuming surface

If this run supports closure, acceptance, evidence, audit, research, knowledge, or future recovery, preserve this output in the packet or in a cited durable record; do not leave it only in transient launch output.

## Worker Output

Outcome: stop.

Files changed:

- `loom-core/agents/loom-weaver.md`
- `loom-core/skills/loom-weaver/SKILL.md`
- `loom-core/loom-core.mjs`
- `loom-core/package.json`
- `loom-core/.claude-plugin/plugin.json`
- `loom-core/.codex-plugin/plugin.json`
- `loom-core/.cursor-plugin/plugin.json`
- `AGENTS.md`
- `INSTALL.md`
- `README.md`
- `loom-core/README.md`

Records changed:

- `.loom/tickets/20260514-loom-weaver-agent.md`
- `.loom/specs/loom-weaver-agent.md`
- `.loom/research/20260514-direct-interactive-agent-surfaces.md`
- `.loom/evidence/20260514-loom-weaver-implementation-validation.md`
- `.loom/packets/ralph/20260514T223622Z-loom-weaver-agent-implementation.md`

Evidence, review findings, validation output, or observations gathered:

- Created `evidence:20260514-loom-weaver-implementation-validation`.
- Rechecked Codex official docs and found plugins document bundled skills, apps, MCP servers, hooks, and default prompts, but not plugin-shipped custom agents or plugin-shipped profiles.
- `npm --prefix loom-core run smoke` passed with `ok: true`, `agentNames: ["loom-weaver"]`, `loomWeaverPromptBodiesMatch: true`, `loomWeaverOpenCodeMode: "all"`, and `.loom/**` edit allowlist over default edit deny.
- `npm --prefix loom-core run pack:check` passed and the dry-run tarball included `agents/loom-weaver.md` and `skills/loom-weaver/SKILL.md`.
- `claude plugin validate "$PWD/loom-core"` initially failed on a directory-valued `agents` manifest field, then passed after changing it to `["./agents/loom-weaver.md"]`.
- `gemini extensions validate "$PWD/loom-core"` passed.
- `git diff --check` passed after the final manifest correction.

What was not verified or reviewed:

- No live runtime invocation was tested inside OpenCode, Claude Code, Codex, Cursor, or Gemini CLI.
- No Cursor plugin validator was run or available.
- OpenCode permission enforcement was inspected through generated config and smoke output, not exercised in a live OpenCode session.
- Audit/review for `ACC-009` has not run.

Blockers, risks, or assumptions discovered:

- Current Codex plugin docs do not support plugin-shipped profiles or custom agents, so Codex first-class support is through the bundled `loom-weaver` skill and natural-language plugin use, not a plugin-provided `--profile` path.
- Claude plugin validation requires the `agents` manifest field to identify the agent file, not the `agents/` directory string used initially.
- Cursor support remains source-doc-based and unvalidated by a local plugin validator.

Recommended next move:

- Run a fresh audit/review packet over the diff, `evidence:20260514-loom-weaver-implementation-validation`, and the ticket acceptance criteria before closure.
