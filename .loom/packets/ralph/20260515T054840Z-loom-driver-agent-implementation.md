# Loom Driver Agent Implementation Packet

ID: packet:20260515T054840Z-loom-driver-agent-implementation
Type: Packet
Status: consumed
Created: 2026-05-15 05:48 UTC
Updated: 2026-05-15 05:58 UTC
Target: ticket:20260515-loom-driver-agent
Packet Kind: Ralph
Mode: execution
Context Style: live-reference
Worker: manual handoff
Branch: main
Worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
Risk: high - model-visible agent persona and adapter exposure changes.
Verification Posture: observation-first
Change Class: Core named agent prompt surface

## Mission

Implement the smallest complete Loom Driver agent surface that satisfies `spec:loom-driver-agent` and `ticket:20260515-loom-driver-agent` acceptance for shipped Core package behavior.

## Context Bundle

Records:

- `spec:loom-driver-agent` - behavior contract for the new inner-loop agent persona.
- `ticket:20260515-loom-driver-agent` - executable scope, acceptance, evidence, and audit posture for this implementation.
- `spec:loom-weaver-agent` - precedent for named Loom agent behavior contract and prompt quality bar.
- `ticket:20260514-loom-weaver-agent` - implementation precedent for Core agent files, Codex TOML, manifests, docs, evidence, and audit.
- `research:20260514-direct-interactive-agent-surfaces` - harness invocation constraints and supported agent exposure patterns.

Evidence Or Artifacts:

- None yet - this packet should be followed by fresh validation evidence after implementation.

Files, Diffs, Or External References:

- `loom-core/agents/loom-weaver.md` - canonical prompt structure and tone precedent.
- `loom-core/codex/agents/loom-weaver.toml` - Codex custom-agent TOML precedent.
- `loom-core/loom-core.mjs` - OpenCode registration, smoke, and package inspection logic.
- `loom-core/.claude-plugin/plugin.json` - Claude plugin agent exposure.
- `loom-core/.cursor-plugin/plugin.json` - Cursor plugin agent directory exposure.
- `loom-core/.codex-plugin/plugin.json` - Codex plugin install-surface prompt language.
- `INSTALL.md`, `README.md`, `loom-core/README.md` - human-facing docs that may restate named agent availability.
- `AGENTS.md` - contributor-only constraints, especially product-surface leakage and validation commands.

## Read Scope

- `.loom/specs/loom-driver-agent.md`
- `.loom/tickets/20260515-loom-driver-agent.md`
- `.loom/specs/loom-weaver-agent.md`
- `.loom/tickets/20260514-loom-weaver-agent.md`
- `.loom/research/20260514-direct-interactive-agent-surfaces.md`
- `loom-core/agents/loom-weaver.md`
- `loom-core/codex/agents/loom-weaver.toml`
- `loom-core/loom-core.mjs`
- `loom-core/.claude-plugin/plugin.json`
- `loom-core/.cursor-plugin/plugin.json`
- `loom-core/.codex-plugin/plugin.json`
- `INSTALL.md`
- `README.md`
- `loom-core/README.md`
- `AGENTS.md`

## Write Scope

Records Or Artifacts:

- `.loom/tickets/20260515-loom-driver-agent.md` - update status, current state, related records, and journal as implementation progresses.
- `.loom/evidence/20260515-loom-driver-agent-validation.md` - create after verification to preserve validation observations.
- this packet - fill `## Worker Output` and update `Status:` when appropriate.

Source Paths:

- `loom-core/agents/loom-driver.md` - add canonical prompt.
- `loom-core/codex/agents/loom-driver.toml` - add Codex custom-agent TOML aligned with canonical prompt.
- `loom-core/loom-core.mjs` - update registration, inspection, and smoke checks for multiple shipped agents.
- `loom-core/.claude-plugin/plugin.json` - expose Loom Driver agent if needed.
- `loom-core/.cursor-plugin/plugin.json` - only if needed; it already points at the agent directory.
- `loom-core/.codex-plugin/plugin.json` - update human-facing Codex install prompt language if useful.
- `INSTALL.md` - update named-agent invocation and Codex custom-agent install docs.
- `README.md` - update high-level named-agent mention.
- `loom-core/README.md` - update package summary and boundary wording.

Read-only high-authority records:

- `.loom/constitution/**`, `.loom/specs/**`, `.loom/plans/**`, `.loom/research/**` - do not mutate in this packet. Escalate if the behavior contract or direction proves wrong.

## Source Snapshot

Before this packet was compiled, `git status --short` was clean, the current branch was `main`, and the existing shipped agent surface consisted of `loom-core/agents/loom-weaver.md` plus `loom-core/codex/agents/loom-weaver.toml`. OpenCode registration and smoke checks were Weaver-specific in `loom-core/loom-core.mjs`.

## Task

Implement Loom Driver as a named Core agent surface using the existing Weaver implementation shape as precedent, but do not copy Weaver's outer-loop behavior. The Driver prompt must be inner-loop focused: shaped-target gate, packet-first execution, bounded source edits, safe parallelization, evidence, audit, ticket reconciliation, and high-authority Loom record read-only boundary.

Keep the prompt product-visible and generic for installed workspaces. Do not include repository dogfood details, package smoke explanations, adapter self-justification, or contributor workflow prose in model-visible agent instructions.

Prefer minimal code changes. If `loom-core/loom-core.mjs` can be safely generalized to register all Markdown agents and inspect matching Codex TOML files, do that instead of adding duplicate Weaver/Driver branches. Preserve existing Loom Weaver behavior and smoke output coverage.

## Evidence, Review, Or Verification Expectations

After implementation, run or record:

- Source inspection or grep showing Driver prompt includes inner-loop, Ralph packet, high-authority record boundary, parallelization, evidence/audit, and ticket reconciliation language.
- Source inspection showing Codex TOML developer instructions match canonical Driver prompt.
- `npm --prefix loom-core run smoke`.
- `npm --prefix loom-core run pack:check`.
- `git diff --check`.
- Claude/Gemini validators only if their manifest or extension files change and the commands are available.

Create `.loom/evidence/20260515-loom-driver-agent-validation.md` with observations and limits.

## Stop Conditions

- Stop and escalate if Driver's intended behavior needs a change to `spec:loom-driver-agent`.
- Stop and escalate if implementing Driver requires changing constitution, specs, plans, research synthesis, or `using-loom` doctrine.
- Stop if harness exposure requires new source-backed research beyond `research:20260514-direct-interactive-agent-surfaces`.
- Stop if OpenCode permissions cannot represent a safe inner-loop agent boundary without making the surface misleading.
- Stop if validation cannot be run or interpreted enough to support the ticket acceptance story.

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

Outcome: `stop`

Files changed:

- Added `loom-core/agents/loom-driver.md` as the canonical Loom Driver prompt.
- Added `loom-core/codex/agents/loom-driver.toml` aligned with the canonical prompt.
- Updated `loom-core/loom-core.mjs` to register both named agents, inspect both Codex TOMLs, and smoke-check Driver registration, permissions, and prompt parity.
- Updated `loom-core/.claude-plugin/plugin.json` to expose the Driver agent.
- Updated `loom-core/.codex-plugin/plugin.json`, `INSTALL.md`, `README.md`, `loom-core/README.md`, and `ARCHITECTURE.md` to describe named Core agents and Driver install/invocation where appropriate.

Records changed:

- Created `spec:loom-driver-agent`.
- Created and activated `ticket:20260515-loom-driver-agent`.
- Created this packet and consumed it.
- Created `evidence:20260515-loom-driver-agent-validation`.

Evidence gathered:

- `npm --prefix loom-core run smoke` passed.
- `npm --prefix loom-core run pack:check` passed and dry-run package contents included Driver Markdown and TOML files.
- `git diff --check` passed.
- `claude plugin validate "$PWD/loom-core"` passed after the Claude manifest update.
- Grep inspection found required Driver inner-loop, packet, high-authority boundary, parallelization, evidence, audit, and ticket language in both model-visible Driver surfaces, with no contributor-process leakage beyond generic execution vocabulary noted in the evidence record.

What was not verified or reviewed:

- Live runtime invocation was not tested in OpenCode, Claude Code, Codex, Cursor, or Gemini.
- OpenCode permission matching behavior for high-authority record deny rules was not runtime-tested.
- Fresh Ralph-backed audit is still required before closure.

Blockers, risks, or assumptions discovered:

- No blocker discovered. Residual risk remains around live harness invocation and runtime permission enforcement.

Recommended next move:

- Compile and run a Ralph review packet for audit of the Driver prompt, adapter exposure, evidence sufficiency, and product-surface leakage before closing `ticket:20260515-loom-driver-agent`.
